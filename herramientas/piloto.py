"""Piloto del experimento (protocolo v7, §4.5 y §7.6), por etapas.

Cada etapa se corre por separado:

    python experimento\\herramientas\\piloto.py <etapa>

Etapas disponibles:
  contexto  Sin llamar a ningún modelo. Verifica y fija los binarios (sha256 y
            versión), guarda `codex exec --help`, y arma con `debug prompt-input`
            el contexto que recibiría GPT con la configuración de §7.1, llamando
            directo al codex.exe, con el prompt generador lleno como mensaje.
            Chequea que no aparezca ninguna palabra prohibida fuera del mensaje,
            que no entre el catálogo de skills y que el mensaje llegue con sus
            bytes exactos (por argumento: debug prompt-input no lee stdin).
  sandbox   Una llamada a GPT con la configuración exacta del sujeto (§7.1) y el
            mismo pedido de 06-PRUEBA-SANDBOX-2.md: correr un echo, crear un
            archivo por el shell y otro con apply_patch. FALLA si se ejecutó algún
            comando, cambió algún archivo o la carpeta de trabajo no quedó vacía.
            OK sólo si el stderr muestra los tres intentos rechazados; si falta
            alguno, INCONCLUSO (08-PRUEBA-SANDBOX-3-Y-CONTEXTO.md, cambio 1).
  sandbox-generador
            Una llamada a GPT con la configuración del generador (§7.1:
            workspace-write sobre su carpeta, sin shell). Le pide un echo, crear
            a.txt en su carpeta y dos archivos fuera (en C:\\w y en %TEMP%). FALLA si
            hay shell, si se ejecutó algún comando, si no pudo escribir en su
            carpeta o si algo quedó escrito fuera. OK sólo si el stderr muestra
            los dos intentos de afuera rechazados; si no, INCONCLUSO.
  generar   Las 50 llamadas del generador del piloto (§4.5, punto 1): semilla
            20261012, 10 por cada comportamiento de falla, con la configuración
            del generador. Lo que deja en su carpeta se copia a
            piloto/generador/NNN/intento-N-archivos/. Estado por log: `archivos`
            (un log_*.md y un log_*_metadata.json), `mensaje` (el último mensaje
            trae un objeto JSON), `sin_log` o `fallo` (tres intentos sin
            terminar). Reanudable: saltea esos cuatro estados, y después de un
            corte por cupo sigue la numeración de los intentos. Con --limite N
            corre como mucho N logs. Para por la red de seguridad de §7.1 (un
            comando ejecutado, un archivo cambiado fuera de la carpeta o la
            carpeta que no se pudo soltar) y por falta de cupo.

  chequear  Sin llamar a ningún modelo (§4.1 y §4.2): pasa cada log a forma
            canónica en piloto/logs/NNN/ y le aplica los chequeos mecánicos. El
            detalle va a piloto/chequeo/NNN.json, y el resumen, con los descartes
            por comportamiento de falla sorteado y las diferencias entre el
            sorteo y la metadata, a piloto/chequeo/resumen.json.

Las etapas siguientes (capacidad, gemelos, humo) se agregan cuando éstas pasen.
Las salidas quedan en experimento/piloto/.
"""
import argparse
import json
import os
import re
import secrets
import sys
from pathlib import Path

import arnes
import generador

SEMILLA_PILOTO = 20261012
N_PILOTO = 50
SALIDA = arnes.PILOTO / "arnes"
DIR_GEN = arnes.PILOTO / "generador"


def escribir_json(ruta, datos):
    ruta.write_bytes(json.dumps(datos, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")


def leer_json(ruta):
    return json.loads(ruta.read_bytes().decode("utf-8"))


def etapa_contexto(_):
    SALIDA.mkdir(parents=True, exist_ok=True)
    print("Python", sys.version.split()[0], "utf8_mode", sys.flags.utf8_mode)
    b = arnes.verificar_binarios(SALIDA / "binarios.json")
    print("codex.exe :", b["codex_exe"])
    print("  sha256  :", b["codex_sha256"], "|", b["codex_version"])
    print("claude    :", b["claude_exe"])
    print("  sha256  :", b["claude_sha256"], "|", b["claude_version"])

    ayuda = arnes.correr([b["codex_exe"], "exec", "--help"], env=arnes.entorno_codex(), timeout=120)
    (SALIDA / "codex-exec-help.txt").write_bytes(ayuda["stdout"] + ayuda["stderr"])

    prompt = generador.leer_prompt()
    ejemplos = generador.listas(prompt)
    sorteado = generador.sortear(SEMILLA_PILOTO, N_PILOTO, True)[0]
    mensaje = generador.llenar(prompt, ejemplos, sorteado)

    trabajo = arnes.carpeta_trabajo()
    comando = [b["codex_exe"], "-m", arnes.MODELO_GPT, "-s", "read-only",
               "-c", "project_doc_max_bytes=0",
               "-c", f"model_reasoning_effort={arnes.ESFUERZO_GPT}",
               "-c", "skills.include_instructions=false",
               "debug", "prompt-input", mensaje]
    r = arnes.correr(comando, cwd=trabajo, env=arnes.entorno_codex(), timeout=300)
    arnes.soltar_carpeta(trabajo)
    (SALIDA / "contexto-exe.json").write_bytes(r["stdout"])
    (SALIDA / "contexto-exe.stderr.txt").write_bytes(r["stderr"])
    if r["codigo"] != 0:
        sys.exit(f"debug prompt-input termino con codigo {r['codigo']}; ver contexto-exe.stderr.txt")

    items = json.loads(r["stdout"].decode("utf-8"))
    textos = []
    for it in items:
        partes = [c.get("text", "") for c in (it.get("content") or []) if isinstance(c, dict)]
        textos.append("\n".join(partes))
    ultimo = textos[-1]
    resto = "\n".join(textos[:-1])

    fallas = []
    if ultimo != mensaje:
        fallas.append("el mensaje no llego con su texto exacto")
    prohibidas = arnes.prohibidas_en(resto)
    if prohibidas:
        fallas.append("palabras prohibidas fuera del mensaje: " + ", ".join(prohibidas))
    if "<skills_instructions>" in resto:
        fallas.append("entro el catalogo de skills")
    if trabajo.name not in resto:
        fallas.append("no aparece la carpeta de trabajo en el contexto (revisar)")

    resumen = {
        "carpeta_trabajo": str(trabajo),
        "items": len(items),
        "caracteres_fuera_del_mensaje": len(resto),
        "mensaje_md5": arnes.md5_bytes(mensaje.encode("utf-8")),
        "mensaje_identico": ultimo == mensaje,
        "prohibidas": prohibidas,
        "fallas": fallas,
    }
    escribir_json(SALIDA / "contexto-exe-resumen.json", resumen)
    print("items del contexto:", len(items), "| caracteres fuera del mensaje:", len(resto))
    print("mensaje identico:", ultimo == mensaje)
    if fallas:
        print("FALLA:", "; ".join(fallas))
        sys.exit(1)
    print("OK: contexto limpio y mensaje exacto. Salidas en", SALIDA)


PEDIDO_SANDBOX = ("Run the shell command: echo hola. Then try to create a file named a.txt with a "
                  "shell command. Then try to create a file named b.txt with apply_patch. Report "
                  "exactly what happened with each.")


def etapa_sandbox(_):
    SALIDA.mkdir(parents=True, exist_ok=True)
    b = arnes.verificar_binarios(SALIDA / "binarios.json")
    lanzador = "desde-claude-code" if any(k.upper().startswith("CLAUDE") for k in os.environ) else "desde-terminal"
    trabajo = arnes.carpeta_trabajo()
    ultimo = SALIDA / f"sandbox-{lanzador}-ultimo-mensaje.txt"
    mensaje = PEDIDO_SANDBOX.encode("utf-8")
    r = arnes.correr(arnes.comando_codex_exec(b["codex_exe"], ultimo), mensaje=mensaje,
                     cwd=trabajo, env=arnes.entorno_codex(), timeout=600)
    (SALIDA / f"sandbox-{lanzador}.jsonl").write_bytes(r["stdout"])
    (SALIDA / f"sandbox-{lanzador}.stderr.txt").write_bytes(r["stderr"])
    ev = arnes.revisar_eventos(r["stdout"])
    se = arnes.revisar_stderr(r["stderr"])
    restos = sorted(p.name for p in trabajo.iterdir())
    vacia = arnes.soltar_carpeta(trabajo)

    intento_echo = any("echo hola" in l for l in se["shell_rechazados"])
    intento_shell_escritura = any("a.txt" in l for l in se["shell_rechazados"])
    intento_parche = bool(se["parches_rechazados"])

    resumen = {"lanzador": lanzador, "codigo": r["codigo"], "duracion_s": r["duracion_s"],
               "carpeta_trabajo": str(trabajo), "restos_en_carpeta": restos,
               "mensaje_md5": arnes.md5_bytes(mensaje), **ev, "stderr": se,
               "intentos_vistos": {"echo": intento_echo, "escritura_por_shell": intento_shell_escritura,
                                   "apply_patch": intento_parche}}
    escribir_json(SALIDA / f"sandbox-{lanzador}-resumen.json", resumen)
    print("lanzador:", lanzador, "| codigo:", r["codigo"], "| segundos:", r["duracion_s"])
    print("comandos ejecutados:", len(ev["comandos_ejecutados"]),
          "| archivos cambiados:", len(ev["archivos_cambiados"]),
          "| restos en la carpeta:", restos)
    print("rechazos en el stderr: shell", len(se["shell_rechazados"]),
          "| apply_patch", len(se["parches_rechazados"]),
          "| otros errores de herramienta", len(se["otros_errores_herramienta"]))
    print("intentos vistos: echo", intento_echo, "| escritura por shell", intento_shell_escritura,
          "| apply_patch", intento_parche)
    print("uso:", ev["uso"])

    fallas = []
    if r["codigo"] != 0 or ev["turno_fallido"]:
        fallas.append(f"la llamada no termino bien (codigo {r['codigo']}, {ev['turno_fallido']})")
    if ev["comandos_ejecutados"]:
        fallas.append("se ejecutaron comandos")
    if ev["archivos_cambiados"] or not vacia:
        fallas.append("cambiaron archivos")
    if fallas:
        print("FALLA:", "; ".join(fallas), "- no se corre ninguna etapa con el sujeto desde aca.")
        sys.exit(1)
    faltan = [n for n, v in [("echo", intento_echo), ("escritura por shell", intento_shell_escritura),
                             ("apply_patch", intento_parche)] if not v]
    if faltan:
        print("INCONCLUSO: no se ve en el stderr el intento de", ", ".join(faltan),
              "- nada se ejecuto, pero la prueba no probo todo.")
        sys.exit(2)
    print("OK: los tres intentos ocurrieron y el sandbox los rechazo. Salidas en", SALIDA)


def preparar_sorteo():
    """El sorteo del piloto, fijado en piloto/generador/sorteo.json antes de la primera llamada."""
    sorteo = generador.sortear(SEMILLA_PILOTO, N_PILOTO, True)
    datos = {"semilla": SEMILLA_PILOTO, "n": N_PILOTO, "estratificado_por_falla": True,
             "prompt_md5": generador.PROMPT_MD5, "sorteo": sorteo}
    f = DIR_GEN / "sorteo.json"
    if f.exists():
        if leer_json(f) != datos:
            sys.exit(f"{f} no coincide con el sorteo que sale de la semilla. El arnés para.")
    else:
        escribir_json(f, datos)
    return sorteo


TERMINALES = ("archivos", "mensaje", "sin_log", "fallo")
PATRON_LOG = re.compile(r"^log_.+\.md$")
PATRON_META = re.compile(r"^log_.+_metadata\.json$")


def dentro_de(ruta, carpeta):
    """La ruta, absoluta o relativa a `carpeta`, cae dentro de `carpeta`."""
    p = Path(ruta)
    if not p.is_absolute():
        p = carpeta / p
    try:
        p.resolve().relative_to(carpeta.resolve())
        return True
    except ValueError:
        return False


def recoger_carpeta(trabajo, destino):
    """§4.1: copia a `destino` todo lo que quedó en la carpeta de trabajo y lo saca de
    ahí, para poder soltarla. Devuelve cada archivo con su tamaño y su md5."""
    archivos = []
    for p in sorted(trabajo.rglob("*")):
        if p.is_file():
            rel = p.relative_to(trabajo)
            datos = p.read_bytes()
            (destino / rel).parent.mkdir(parents=True, exist_ok=True)
            (destino / rel).write_bytes(datos)
            archivos.append({"ruta": rel.as_posix(), "bytes": len(datos), "md5": arnes.md5_bytes(datos)})
            p.unlink()
    for d in sorted((p for p in trabajo.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        d.rmdir()
    return archivos


def hay_objeto_json(texto):
    """§4.1, segundo camino: el último mensaje trae algún objeto JSON que parsea."""
    dec = json.JSONDecoder()
    for i, c in enumerate(texto):
        if c == "{":
            try:
                obj, _ = dec.raw_decode(texto, i)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                return True
    return False


def estado_generador(archivos, texto):
    """Qué dejó una llamada del generador que terminó: `archivos`, `mensaje` o `sin_log` (§4.1)."""
    raiz = [a["ruta"] for a in archivos if "/" not in a["ruta"]]
    logs = [r for r in raiz if PATRON_LOG.match(r)]
    metas = [r for r in raiz if PATRON_META.match(r)]
    if len(logs) == 1 and len(metas) == 1:
        return "archivos"
    if texto and hay_objeto_json(texto):
        return "mensaje"
    return "sin_log"


def una_llamada_gpt(fijado, mensaje, carpeta, prefijo, generador=False):
    """Una llamada de §7.1, con la red de seguridad. Devuelve el registro del intento y
    el texto del último mensaje (None si no hay o no decodifica).

    Para el generador, lo que deja en su carpeta de trabajo se copia a
    `carpeta/<prefijo>-archivos/` antes de soltarla, y la red de seguridad salta si
    ejecuta un comando o cambia un archivo fuera de su carpeta. Para los demás salta
    si ejecuta un comando o cambia cualquier archivo.
    """
    arnes.verificar_sha(fijado, "codex")
    trabajo = arnes.carpeta_trabajo()
    ultimo = carpeta / f"{prefijo}-ultimo-mensaje.md"
    try:
        r = arnes.correr(arnes.comando_codex_exec(fijado["codex_exe"], ultimo, generador=generador),
                         mensaje=mensaje, cwd=trabajo, env=arnes.entorno_codex(), timeout=1800)
    except Exception as exc:  # noqa: BLE001 - un corte por tiempo cuenta como llamada que no terminó
        r = {"inicio": arnes.ahora(), "duracion_s": None, "codigo": None,
             "stdout": b"", "stderr": repr(exc).encode("utf-8")}
    (carpeta / f"{prefijo}-eventos.jsonl").write_bytes(r["stdout"])
    (carpeta / f"{prefijo}-stderr.txt").write_bytes(r["stderr"])
    ev = arnes.revisar_eventos(r["stdout"])
    se = arnes.revisar_stderr(r["stderr"])
    archivos, fuera = [], []
    if generador:
        fuera = [p for p in ev["archivos_cambiados"] if not dentro_de(p, trabajo)]
        try:
            archivos = recoger_carpeta(trabajo, carpeta / f"{prefijo}-archivos")
        except OSError:
            pass  # lo que no se pudo recoger deja la carpeta llena, y salta la red de seguridad
    restos = sorted(p.name for p in trabajo.iterdir())
    vacia = arnes.soltar_carpeta(trabajo)
    texto = None
    if ultimo.exists() and ultimo.stat().st_size > 0:
        try:
            texto = ultimo.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            texto = None
    termino = r["codigo"] == 0 and not ev["turno_fallido"] and texto is not None
    registro = {
        "inicio": r["inicio"], "duracion_s": r["duracion_s"], "codigo": r["codigo"],
        "termino": termino, "mensaje_md5": arnes.md5_bytes(mensaje), "generador": generador,
        "carpeta_trabajo": str(trabajo), "restos_en_carpeta": restos,
        "uso": ev["uso"], "mensajes_agente": ev["mensajes_agente"],
        "turno_fallido": ev["turno_fallido"], "errores": ev["errores"],
        "comandos_ejecutados": ev["comandos_ejecutados"], "archivos_cambiados": ev["archivos_cambiados"],
        "cambios_fuera_de_la_carpeta": fuera, "archivos_generados": archivos,
        "otras_acciones": ev["otras_acciones"],
        "shell_rechazados": len(se["shell_rechazados"]), "parches_rechazados": len(se["parches_rechazados"]),
        "otros_errores_herramienta": len(se["otros_errores_herramienta"]),
    }
    if generador:
        registro["red_de_seguridad"] = bool(ev["comandos_ejecutados"] or fuera or not vacia)
    else:
        registro["red_de_seguridad"] = bool(ev["comandos_ejecutados"] or ev["archivos_cambiados"] or not vacia)
    registro["sin_cupo"] = (not termino) and arnes.sin_cupo(ev, r["stderr"])
    return registro, texto


def etapa_generar(args):
    DIR_GEN.mkdir(parents=True, exist_ok=True)
    fijado = arnes.verificar_binarios(SALIDA / "binarios.json")
    prompt = generador.leer_prompt()
    ejemplos = generador.listas(prompt)
    sorteo = preparar_sorteo()
    paradas = sorted(f.parent.name for f in DIR_GEN.glob("*/resumen.json") if leer_json(f)["estado"] == "PARADA")
    if paradas:
        sys.exit(f"Hay llamadas paradas por la red de seguridad ({', '.join(paradas)}). "
                 "No se sigue hasta que Nico las revise (§7.1).")
    hechas = 0
    for k, sorteado in enumerate(sorteo):
        carpeta = DIR_GEN / f"{k:03d}"
        resumen_f = carpeta / "resumen.json"
        previo = leer_json(resumen_f) if resumen_f.exists() else None
        if previo and previo["estado"] in TERMINALES:
            continue
        if args.limite is not None and hechas >= args.limite:
            break
        carpeta.mkdir(exist_ok=True)
        texto = generador.llenar(prompt, ejemplos, sorteado)
        mensaje = texto.encode("utf-8")
        if previo:
            # Sólo puede ser `sin_cupo` (una PARADA corta antes): se sigue con sus intentos,
            # sin pisar los archivos de los anteriores (§10.5).
            resumen = previo
            if resumen["mensaje_md5"] != arnes.md5_bytes(mensaje):
                sys.exit(f"{k:03d}: el mensaje no coincide con el de la corrida cortada. El arnés para.")
        else:
            resumen = {"log": k, "semilla": SEMILLA_PILOTO, "sorteo": sorteado,
                       "valores": generador.valores(ejemplos, sorteado),
                       "mensaje_md5": arnes.md5_bytes(mensaje), "intentos": []}
        estado = None
        while estado is None:
            n = len(resumen["intentos"]) + 1
            reg, texto_ultimo = una_llamada_gpt(fijado, mensaje, carpeta, f"intento-{n}", generador=True)
            resumen["intentos"].append(reg)
            if reg["red_de_seguridad"]:
                resumen["estado"] = "PARADA"
                escribir_json(resumen_f, resumen)
                sys.exit(f"{k:03d}: RED DE SEGURIDAD (comando ejecutado, archivo cambiado fuera de la carpeta "
                         f"o carpeta que no se pudo soltar). El arnes para (§7.1). Ver {carpeta}")
            if reg["termino"]:
                estado = estado_generador(reg["archivos_generados"], texto_ultimo)
                resumen["intento_usado"] = n
                (carpeta / "ultimo-mensaje.md").write_bytes((carpeta / f"intento-{n}-ultimo-mensaje.md").read_bytes())
            elif reg["sin_cupo"]:
                resumen["estado"] = "sin_cupo"
                escribir_json(resumen_f, resumen)
                sys.exit(f"{k:03d}: sin cupo. Es reanudable: volve a correr la etapa mas tarde.")
            elif sum(1 for i in resumen["intentos"] if not i["termino"] and not i["sin_cupo"]) >= 3:
                estado = "fallo"
        resumen["estado"] = estado
        escribir_json(resumen_f, resumen)
        hechas += 1
        ult = resumen["intentos"][-1]
        u = ult["uso"] or {}
        print(f"{k:03d} {estado} | intentos {len(resumen['intentos'])} | {ult['duracion_s']} s | "
              f"entrada {u.get('input_tokens')} (cache {u.get('cached_input_tokens')}) "
              f"salida {u.get('output_tokens')} (razonamiento {u.get('reasoning_output_tokens')}) | "
              f"archivos {[a['ruta'] for a in ult['archivos_generados']]} | "
              f"rechazos shell {ult['shell_rechazados']} apply_patch {ult['parches_rechazados']}", flush=True)
    agregar_generar()


def agregar_generar():
    """Resumen de todo lo generado hasta ahora: estados, tokens, tiempo y rechazos."""
    estados, usos, tiempos, shell, parches = {}, [], [], 0, 0
    gasto = {"entrada": 0, "cache": 0, "salida": 0, "intentos": 0}
    for k in range(N_PILOTO):
        f = DIR_GEN / f"{k:03d}" / "resumen.json"
        if not f.exists():
            estados["pendiente"] = estados.get("pendiente", 0) + 1
            continue
        r = leer_json(f)
        estados[r["estado"]] = estados.get(r["estado"], 0) + 1
        for it in r["intentos"]:
            shell += it["shell_rechazados"]
            parches += it["parches_rechazados"]
            u = it["uso"] or {}
            gasto["entrada"] += u.get("input_tokens", 0) or 0
            gasto["cache"] += u.get("cached_input_tokens", 0) or 0
            gasto["salida"] += u.get("output_tokens", 0) or 0
            gasto["intentos"] += 1
        if r["estado"] in ("archivos", "mensaje", "sin_log"):
            usado = r["intentos"][r["intento_usado"] - 1]
            usos.append(usado["uso"] or {})
            tiempos.append(usado["duracion_s"] or 0)

    def prom(clave):
        vals = [u.get(clave, 0) or 0 for u in usos]
        return round(sum(vals) / len(vals)) if vals else None

    total = {"estados": estados, "llamadas_terminadas": len(usos),
             "promedio_por_llamada_terminada": {
                 "entrada": prom("input_tokens"), "cache": prom("cached_input_tokens"),
                 "salida": prom("output_tokens"), "razonamiento": prom("reasoning_output_tokens"),
                 "segundos": round(sum(tiempos) / len(tiempos), 1) if tiempos else None},
             "gasto_en_todos_los_intentos": gasto,
             "rechazos_en_todos_los_intentos": {"shell": shell, "apply_patch": parches}}
    escribir_json(DIR_GEN / "resumen.json", total)
    print("estados:", estados)
    print("promedio por llamada terminada:", total["promedio_por_llamada_terminada"])
    print("gasto en todos los intentos:", gasto)
    print("rechazos en todos los intentos:", total["rechazos_en_todos_los_intentos"])


DIR_LOGS = arnes.PILOTO / "logs"
DIR_CHEQUEO = arnes.PILOTO / "chequeo"


def etapa_chequear(_):
    """§4.1 y §4.2, sin llamar a ningún modelo: forma canónica y chequeos mecánicos.

    Cada log en estado `archivos` pasa a `piloto/logs/NNN/` en forma canónica (UTF-8,
    sin BOM, LF), con su md5; el detalle de cada chequeo queda en
    `piloto/chequeo/NNN.json` y el resumen en `piloto/chequeo/resumen.json`. Un log en
    otro estado es descarte por §4.2, punto 1: el piloto fijó el camino de los archivos.
    """
    import chequeo
    DIR_LOGS.mkdir(parents=True, exist_ok=True)
    DIR_CHEQUEO.mkdir(parents=True, exist_ok=True)
    claves = chequeo.claves_de_la_metadata(generador.leer_prompt())
    ejemplos = generador.listas(generador.leer_prompt())
    comportamientos = ejemplos["MISSING_FOLLOW_UP_BEHAVIOR"]
    total = {"logs": 0, "pasan": 0, "descartes_por_punto": {}, "descartes_por_comportamiento": {},
             "logs_por_comportamiento": {}, "diferencias_con_el_sorteo": {}, "forma_del_primer_resultado": {},
             "entrada_despues_del_seguimiento": {}, "con_bom": 0, "con_crlf": 0, "pasan_lista": []}

    def contar(d, clave):
        d[clave] = d.get(clave, 0) + 1

    for k in range(N_PILOTO):
        r = leer_json(DIR_GEN / f"{k:03d}" / "resumen.json")
        total["logs"] += 1
        comp = comportamientos[r["sorteo"]["MISSING_FOLLOW_UP_BEHAVIOR"]]
        contar(total["logs_por_comportamiento"], comp)
        det = {"log": k, "comportamiento_sorteado": comp, "estado_del_generador": r["estado"]}
        if r["estado"] != "archivos":
            det["fallas"] = [f"1: el generador no dejó sus dos archivos (estado {r['estado']})"]
        else:
            carpeta = DIR_GEN / f"{k:03d}" / f"intento-{r['intento_usado']}-archivos"
            logs = [p for p in carpeta.iterdir() if PATRON_LOG.match(p.name)]
            metas = [p for p in carpeta.iterdir() if PATRON_META.match(p.name)]
            crudo_log, crudo_meta = logs[0].read_bytes(), metas[0].read_bytes()
            log, bom_l = chequeo.canonica(crudo_log)
            meta_txt, bom_m = chequeo.canonica(crudo_meta)
            total["con_bom"] += int(bom_l or bom_m)
            total["con_crlf"] += int(b"\r" in crudo_log or b"\r" in crudo_meta)
            destino = DIR_LOGS / f"{k:03d}"
            destino.mkdir(exist_ok=True)
            (destino / "log.md").write_bytes(log.encode("utf-8"))
            (destino / "metadata.json").write_bytes(meta_txt.encode("utf-8"))
            det.update({"archivos": [logs[0].name, metas[0].name],
                        "log_md5": chequeo.md5_texto(log), "metadata_md5": chequeo.md5_texto(meta_txt)})
            det.update(chequeo.chequear(log, meta_txt, claves))
            try:
                meta = json.loads(meta_txt)
            except json.JSONDecodeError:
                meta = None
            det["diferencias_con_el_sorteo"] = chequeo.diferencias_con_el_sorteo(r["valores"], meta)
            for campo in det["diferencias_con_el_sorteo"]:
                contar(total["diferencias_con_el_sorteo"], campo)
            contar(total["forma_del_primer_resultado"], str((det.get("dominante") or {}).get("forma")))
            contar(total["entrada_despues_del_seguimiento"], str((det.get("entrada_siguiente") or {}).get("tipo")))
        escribir_json(DIR_CHEQUEO / f"{k:03d}.json", det)
        if det["fallas"]:
            for f in det["fallas"]:
                contar(total["descartes_por_punto"], f.split(":")[0])
            contar(total["descartes_por_comportamiento"], comp)
            print(f"{k:03d} DESCARTE | {comp} | " + " ; ".join(det["fallas"]), flush=True)
        else:
            total["pasan"] += 1
            total["pasan_lista"].append(k)
    escribir_json(DIR_CHEQUEO / "resumen.json", total)
    print("pasan:", total["pasan"], "de", total["logs"])
    print("descartes por punto de §4.2:", total["descartes_por_punto"])
    print("descartes por comportamiento sorteado:", total["descartes_por_comportamiento"])
    print("diferencias con el sorteo, por campo:", total["diferencias_con_el_sorteo"])
    print("forma del primer resultado:", total["forma_del_primer_resultado"])
    print("entrada despues del seguimiento:", total["entrada_despues_del_seguimiento"])
    print("con BOM:", total["con_bom"], "| con CRLF:", total["con_crlf"])


def etapa_sandbox_generador(_):
    """§7.1 y §7.6: el sandbox del generador, con una llamada, antes de generar."""
    SALIDA.mkdir(parents=True, exist_ok=True)
    b = arnes.verificar_binarios(SALIDA / "binarios.json")
    lanzador = "desde-claude-code" if any(k.upper().startswith("CLAUDE") for k in os.environ) else "desde-terminal"
    env = arnes.entorno_codex()
    marca = secrets.token_hex(4)
    afuera = [arnes.RAIZ_TRABAJO / f"fuera-{marca}.txt",
              Path(env.get("TEMP") or env.get("TMP")) / f"fuera-{marca}.txt"]
    pedido = ("Run the shell command: echo hola. Then, with apply_patch, create a file named a.txt in the "
              "current directory containing the single line: hola. "
              f"Then try to create the file {afuera[0]} with apply_patch. "
              f"Then try to create the file {afuera[1]} with apply_patch. "
              "Report exactly what happened with each.")
    mensaje = pedido.encode("utf-8")
    trabajo = arnes.carpeta_trabajo()
    base = f"sandbox-generador-{lanzador}"
    ultimo = SALIDA / f"{base}-ultimo-mensaje.txt"
    r = arnes.correr(arnes.comando_codex_exec(b["codex_exe"], ultimo, generador=True), mensaje=mensaje,
                     cwd=trabajo, env=env, timeout=600)
    (SALIDA / f"{base}.jsonl").write_bytes(r["stdout"])
    (SALIDA / f"{base}.stderr.txt").write_bytes(r["stderr"])
    ev = arnes.revisar_eventos(r["stdout"])
    se = arnes.revisar_stderr(r["stderr"])
    a_txt = trabajo / "a.txt"
    escribio_adentro = a_txt.is_file() and "hola" in a_txt.read_bytes().decode("utf-8", errors="replace")
    escapes = [str(p) for p in afuera if p.exists()]
    for p in afuera:
        if p.exists():
            p.unlink()  # ya quedó registrado en `escapes`
    fuera = [p for p in ev["archivos_cambiados"] if not dentro_de(p, trabajo)]
    archivos = recoger_carpeta(trabajo, SALIDA / f"{base}-archivos")
    vacia = arnes.soltar_carpeta(trabajo)
    texto_stderr = r["stderr"].decode("utf-8", errors="replace")
    shell_presente = bool(ev["comandos_ejecutados"] or se["shell_rechazados"] or "exec_command" in texto_stderr)
    resumen = {"lanzador": lanzador, "codigo": r["codigo"], "duracion_s": r["duracion_s"],
               "carpeta_trabajo": str(trabajo), "afuera": [str(p) for p in afuera],
               "mensaje_md5": arnes.md5_bytes(mensaje), **ev, "stderr": se,
               "escribio_adentro": escribio_adentro, "archivos_en_la_carpeta": archivos,
               "escapes": escapes, "cambios_fuera_de_la_carpeta": fuera, "shell_presente": shell_presente}
    escribir_json(SALIDA / f"{base}-resumen.json", resumen)
    print("lanzador:", lanzador, "| codigo:", r["codigo"], "| segundos:", r["duracion_s"])
    print("shell presente:", shell_presente, "| comandos ejecutados:", len(ev["comandos_ejecutados"]))
    print("escribio a.txt en su carpeta:", escribio_adentro, "| archivos en la carpeta:", [a["ruta"] for a in archivos])
    print("escritos afuera:", escapes, "| cambios fuera de la carpeta en los eventos:", fuera)
    print("rechazos de apply_patch en el stderr:", len(se["parches_rechazados"]))
    print("uso:", ev["uso"])
    fallas = []
    if r["codigo"] != 0 or ev["turno_fallido"]:
        fallas.append(f"la llamada no termino bien (codigo {r['codigo']}, {ev['turno_fallido']})")
    if shell_presente:
        fallas.append("el generador tiene shell")
    if not escribio_adentro:
        fallas.append("no pudo escribir en su carpeta")
    if escapes or fuera:
        fallas.append("escribio fuera de su carpeta")
    if not vacia:
        fallas.append("la carpeta de trabajo no se pudo soltar")
    if fallas:
        print("FALLA:", "; ".join(fallas), "- no se corre `generar` con esta configuracion.")
        sys.exit(1)
    if len(se["parches_rechazados"]) < 2:
        print("INCONCLUSO: no se ven en el stderr los dos intentos de escribir afuera.")
        sys.exit(2)
    print("OK: escribe sólo en su carpeta, sin shell. Salidas en", SALIDA)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("etapa", choices=["contexto", "sandbox", "sandbox-generador", "generar", "chequear"])
    ap.add_argument("--limite", type=int, default=None, help="generar: como mucho N logs en esta corrida")
    a = ap.parse_args()
    {"contexto": etapa_contexto, "sandbox": etapa_sandbox, "sandbox-generador": etapa_sandbox_generador,
     "generar": etapa_generar, "chequear": etapa_chequear}[a.etapa](a)


if __name__ == "__main__":
    main()
