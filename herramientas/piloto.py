"""Piloto del experimento (protocolo v5, §4.5 y §7.6), por etapas.

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
  generar   Las 50 llamadas del generador del piloto (§4.5, punto 1): semilla
            20261012, 10 por cada comportamiento de falla. Reanudable: saltea las
            que ya terminaron bien. Con --limite N corre como mucho N llamadas.
            Para por la red de seguridad de §7.1 (un comando ejecutado, un archivo
            cambiado o la carpeta de trabajo no vacía) y por falta de cupo.

Las etapas siguientes (chequear, capacidad, gemelos, humo) se agregan cuando
éstas pasen. Las salidas quedan en experimento/piloto/arnes/ y
experimento/piloto/generador/.
"""
import argparse
import json
import os
import sys

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


def una_llamada_gpt(fijado, mensaje, carpeta, prefijo):
    """Una llamada de §7.1, con la red de seguridad. Devuelve el registro del intento."""
    arnes.verificar_sha(fijado, "codex")
    trabajo = arnes.carpeta_trabajo()
    ultimo = carpeta / f"{prefijo}-ultimo-mensaje.md"
    try:
        r = arnes.correr(arnes.comando_codex_exec(fijado["codex_exe"], ultimo), mensaje=mensaje,
                         cwd=trabajo, env=arnes.entorno_codex(), timeout=1800)
    except Exception as exc:  # noqa: BLE001 - un corte por tiempo cuenta como llamada que no terminó
        r = {"inicio": arnes.ahora(), "duracion_s": None, "codigo": None,
             "stdout": b"", "stderr": repr(exc).encode("utf-8")}
    (carpeta / f"{prefijo}-eventos.jsonl").write_bytes(r["stdout"])
    (carpeta / f"{prefijo}-stderr.txt").write_bytes(r["stderr"])
    ev = arnes.revisar_eventos(r["stdout"])
    se = arnes.revisar_stderr(r["stderr"])
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
        "termino": termino, "mensaje_md5": arnes.md5_bytes(mensaje),
        "carpeta_trabajo": str(trabajo), "restos_en_carpeta": restos,
        "uso": ev["uso"], "mensajes_agente": ev["mensajes_agente"],
        "turno_fallido": ev["turno_fallido"], "errores": ev["errores"],
        "comandos_ejecutados": ev["comandos_ejecutados"], "archivos_cambiados": ev["archivos_cambiados"],
        "otras_acciones": ev["otras_acciones"],
        "shell_rechazados": len(se["shell_rechazados"]), "parches_rechazados": len(se["parches_rechazados"]),
        "otros_errores_herramienta": len(se["otros_errores_herramienta"]),
    }
    registro["red_de_seguridad"] = bool(ev["comandos_ejecutados"] or ev["archivos_cambiados"] or not vacia)
    falla_texto = r["stderr"].decode("utf-8", errors="replace") + " " + str(ev["turno_fallido"] or "") + " " + " ".join(map(str, ev["errores"]))
    registro["sin_cupo"] = (not termino) and bool(arnes.RE_SIN_CUPO.search(falla_texto))
    return registro


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
        if resumen_f.exists() and leer_json(resumen_f)["estado"] in ("ok", "fallo"):
            continue
        if args.limite is not None and hechas >= args.limite:
            break
        carpeta.mkdir(exist_ok=True)
        texto = generador.llenar(prompt, ejemplos, sorteado)
        mensaje = texto.encode("utf-8")
        resumen = {"log": k, "semilla": SEMILLA_PILOTO, "sorteo": sorteado,
                   "valores": generador.valores(ejemplos, sorteado),
                   "mensaje_md5": arnes.md5_bytes(mensaje), "intentos": []}
        estado = "fallo"
        for intento in range(1, 4):
            reg = una_llamada_gpt(fijado, mensaje, carpeta, f"intento-{intento}")
            resumen["intentos"].append(reg)
            if reg["red_de_seguridad"]:
                resumen["estado"] = "PARADA"
                escribir_json(resumen_f, resumen)
                sys.exit(f"{k:03d}: RED DE SEGURIDAD (comando ejecutado, archivo cambiado o carpeta no vacia). "
                         f"El arnes para (§7.1). Ver {carpeta}")
            if reg["termino"]:
                estado = "ok"
                (carpeta / "ultimo-mensaje.md").write_bytes(
                    (carpeta / f"intento-{intento}-ultimo-mensaje.md").read_bytes())
                break
            if reg["sin_cupo"]:
                resumen["estado"] = "sin_cupo"
                escribir_json(resumen_f, resumen)
                sys.exit(f"{k:03d}: sin cupo. Es reanudable: volve a correr la etapa mas tarde.")
        resumen["estado"] = estado
        escribir_json(resumen_f, resumen)
        hechas += 1
        u = resumen["intentos"][-1]["uso"] or {}
        print(f"{k:03d} {estado} | intentos {len(resumen['intentos'])} | "
              f"{resumen['intentos'][-1]['duracion_s']} s | entrada {u.get('input_tokens')} "
              f"(cache {u.get('cached_input_tokens')}) salida {u.get('output_tokens')} "
              f"(razonamiento {u.get('reasoning_output_tokens')}) | rechazos shell "
              f"{resumen['intentos'][-1]['shell_rechazados']} apply_patch "
              f"{resumen['intentos'][-1]['parches_rechazados']}", flush=True)
    agregar_generar()


def agregar_generar():
    """Resumen de todo lo generado hasta ahora: estados, tokens, tiempo y rechazos."""
    estados, usos, tiempos, shell, parches = {}, [], [], 0, 0
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
        if r["estado"] == "ok":
            ultimo = r["intentos"][-1]
            usos.append(ultimo["uso"] or {})
            tiempos.append(ultimo["duracion_s"] or 0)

    def prom(clave):
        vals = [u.get(clave, 0) or 0 for u in usos]
        return round(sum(vals) / len(vals)) if vals else None

    total = {"estados": estados, "llamadas_ok": len(usos),
             "promedio_por_llamada_ok": {"entrada": prom("input_tokens"), "cache": prom("cached_input_tokens"),
                                         "salida": prom("output_tokens"),
                                         "razonamiento": prom("reasoning_output_tokens"),
                                         "segundos": round(sum(tiempos) / len(tiempos), 1) if tiempos else None},
             "rechazos_en_todos_los_intentos": {"shell": shell, "apply_patch": parches}}
    escribir_json(DIR_GEN / "resumen.json", total)
    print("estados:", estados)
    print("promedio por llamada ok:", total["promedio_por_llamada_ok"])
    print("rechazos en todos los intentos:", total["rechazos_en_todos_los_intentos"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("etapa", choices=["contexto", "sandbox", "generar"])
    ap.add_argument("--limite", type=int, default=None, help="generar: como mucho N llamadas en esta corrida")
    a = ap.parse_args()
    {"contexto": etapa_contexto, "sandbox": etapa_sandbox, "generar": etapa_generar}[a.etapa](a)


if __name__ == "__main__":
    main()
