"""La corrida del experimento (protocolo v20, §0, pasos 4 a 7), por etapas.

**Se corre después de congelar el protocolo.** Semilla 20261013 (§4.1), carpetas en
`experimento/corrida/`, los mismos binarios fijados en el piloto. Cada etapa es
reanudable: lo que ya terminó se saltea, y un corte por cupo se retoma con el mismo
comando. Toda etapa que llama a un modelo pide el OK de Nico.

    python experimento\\herramientas\\corrida.py <etapa> [--limite N] [--objetivo N] [--sin-etiquetas]

Etapas, en orden:
  logs        Genera logs en el orden de la semilla (§4.1), los pasa a forma canónica y
              por §4.2, y a los que pasan les hace el chequeo de capacidad (§4.3). Para
              cuando --objetivo logs pasaron los dos (110 por defecto, y nunca menos) o
              con --limite. Al terminar aplica la regla de parada de §4.3 (código de
              salida 3).
  gemelos     Arma el gemelo de cada log que pasó §4.2 y §4.3 (§8.2), corre los
              automáticos de §4.4 y deja en corrida/gemelos/PARA-NICO.md lo que decide
              Nico, que lo anota en corrida/gemelos/decisiones.json.
  incluir     Con las decisiones de Nico, los primeros 100 pares en el orden de la
              semilla que pasan todo; congela la lista con su md5 (§4.4). Si faltan pares,
              dice cuántos, y se vuelve a `logs` con un --objetivo mayor.
  brazos      Las 400 llamadas de los brazos sobre los pares congelados, las cuatro de
              cada par seguidas en un orden sorteado (§7.7). Extrae el JSON (§6.1) y lo
              valida (§5.3). No imprime ni lee ninguna respuesta.
  juez        El juez de §6.2 sobre los 400 JSON, en un orden sorteado que mezcla brazos y
              condiciones.
  validacion  Arma corrida/pares.json y la planilla ciega de §8.1: los ítems decisivos y la
              muestra estratificada, con un id opaco, los textos libres que recibió el
              juez y la descripción de la consulta; sin su etiqueta, sin brazo ni
              condición.
  analizar    Con las etiquetas de Nico, el análisis de analisis.py y la frase de §9.
"""
import argparse
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

import arnes
import chequeo
import generador
import piloto

SEMILLA = 20261013
# Se sortea de una vez y se guarda. Es el máximo: si con 1.000 logs no se llega a 100 pares,
# se para y se informa (v19, hallazgo 15).
N_SORTEO = 1000
OBJETIVO_LOGS = 110     # logs que pasan §4.2 y §4.3 antes del primer `gemelos`
PARES = 100
BRAZOS = ("A2b", "A2")
CONDICIONES = ("pendiente", "limpio")
BINARIOS = arnes.PILOTO / "arnes" / "binarios.json"
DIR = arnes.EXPERIMENTO / "corrida"
# v20, hallazgo 8 de la cuarta revisión: un ítem cortado de golpe entre una llamada que terminó y
# el registro de su resultado es `interrumpido`, terminal, como `fallo`.
TERMINALES_GEN = piloto.TERMINALES + ("interrumpido",)
TERMINALES_CAP = ("si", "no", "fallo", "interrumpido")
TERMINALES_GEMELO = ("hecho", "fallo", "fallo_verificacion", "interrumpido")
TERMINALES_BRAZO = ("hecho", "fallo", "interrumpido")


def escribir(ruta, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    piloto.escribir_json(ruta, datos)


def leer(ruta):
    return piloto.leer_json(ruta)


def md5_archivo(ruta):
    return hashlib.md5(ruta.read_bytes()).hexdigest()


def gpt_con_reintentos(fijado, mensaje, carpeta, intentos, tipo, guardar, generador_=False):
    """§7.1 y §7.7: hasta que termina; tres intentos sin terminar es `fallo`, y un corte
    por cupo no cuenta. Devuelve (estado, registro, texto): `hecho`, `fallo`, `sin_cupo`,
    `PARADA` o `interrumpido`. Cada intento registra su `tipo` (v20, hallazgo 14).

    `guardar` se llama después de cada intento, así un corte abrupto del proceso no pierde la
    historia y reanudar no habilita intentos nuevos (v20, hallazgo 8 de la cuarta revisión).
    Si la historia ya tiene un intento terminado, el proceso se cortó entre la llamada y el
    registro de su resultado: `interrumpido`, terminal, sin volver a llamar."""
    carpeta.mkdir(parents=True, exist_ok=True)
    # v21, hallazgo 5 de la quinta revisión: la historia se revisa antes de llamar. Una red de
    # seguridad la hace falla de la llamada (§7.1); los límites alcanzados no habilitan otra.
    if piloto.cerrar_intentos_en_vuelo(intentos, carpeta):
        return "interrumpido", None, None
    if any(i["red_de_seguridad"] for i in intentos):
        return "fallo", None, None
    if any(i["termino"] for i in intentos):
        return "interrumpido", None, None
    if sum(1 for i in intentos if not i["termino"] and not i["sin_cupo"]) >= 3:
        return "fallo", None, None
    while True:
        n = len(intentos) + 1
        intentos.append(dict(piloto.INTENTO_EN_VUELO, en_vuelo=True, prefijo=f"intento-{n}", tipo=tipo))
        guardar()
        reg, texto = piloto.una_llamada_gpt(fijado, mensaje, carpeta, f"intento-{n}", generador=generador_, tipo=tipo)
        intentos[-1] = reg
        guardar()
        if reg["red_de_seguridad"]:
            return "PARADA", reg, None
        if reg["termino"]:
            return "hecho", reg, texto
        if reg["sin_cupo"]:
            return "sin_cupo", reg, None
        if sum(1 for i in intentos if not i["termino"] and not i["sin_cupo"]) >= 3:
            return "fallo", reg, None


def cortar(estado, quien, guardar):
    """Para la etapa ante la red de seguridad o un corte por cupo, después de guardar. La red
    de seguridad deja la marca `corrida/PARADA`: ninguna etapa sigue hasta que Nico la revise
    y la borre."""
    guardar()
    if estado == "PARADA":
        marca = DIR / "PARADA"
        marca.parent.mkdir(parents=True, exist_ok=True)
        marca.write_bytes(f"{quien}\n".encode("utf-8"))
        sys.exit(f"{quien}: RED DE SEGURIDAD. El arnés para (§7.1); no se sigue hasta que Nico lo revise.")
    sys.exit(f"{quien}: sin cupo. Es reanudable: volvé a correr la etapa más tarde.")


def sin_parada():
    if (DIR / "PARADA").exists():
        sys.exit(f"Hay una parada por la red de seguridad ({(DIR / 'PARADA').read_bytes().decode('utf-8').strip()}). "
                 "No se sigue hasta que Nico la revise y borre corrida/PARADA (§7.1).")


# --- logs: §4.1 a §4.3 -------------------------------------------------------------------

def sorteo():
    s = generador.sortear(SEMILLA, N_SORTEO, False)
    datos = {"semilla": SEMILLA, "n": N_SORTEO, "estratificado_por_falla": False,
             "prompt_md5": generador.PROMPT_MD5, "sorteo": s}
    f = DIR / "sorteo.json"
    if f.exists():
        if leer(f) != datos:
            sys.exit(f"{f} no coincide con el sorteo que sale de la semilla. El arnés para.")
    else:
        escribir(f, datos)
    return s


def etapa_logs(args):
    sin_parada()
    objetivo = args.objetivo or OBJETIVO_LOGS
    # v20, hallazgo 10 de la cuarta revisión: un objetivo chico volvería «final» a una tanda
    # chica, y la regla de §4.3 se aplicaría sobre ella.
    if objetivo < OBJETIVO_LOGS:
        sys.exit(f"--objetivo no puede ser menor que {OBJETIVO_LOGS}: para tandas, usar --limite.")
    fijado = arnes.verificar_binarios(BINARIOS)
    prompt = generador.leer_prompt()
    ejemplos = generador.listas(prompt)
    claves = chequeo.claves_de_la_metadata(prompt)
    pasan, hechas, completo = 0, 0, False
    for k, sorteado in enumerate(sorteo()):
        if pasan >= objetivo:
            completo = True
            break
        carpeta = DIR / "logs" / f"{k:03d}"
        f = carpeta / "estado.json"
        est = leer(f) if f.exists() else {"log": k, "sorteo": sorteado,
                                           "valores": generador.valores(ejemplos, sorteado),
                                           "generador": {"intentos": []}}
        if est.get("final"):
            pasan += est["final"] == "pasa"
            continue
        if args.limite is not None and hechas >= args.limite:
            break

        def guardar():
            escribir(f, est)

        # §4.1: el generador, con la configuración de §7.1.
        gen = est["generador"]
        if gen.get("estado") not in TERMINALES_GEN:
            mensaje = generador.llenar(prompt, ejemplos, sorteado).encode("utf-8")
            gen["mensaje_md5"] = arnes.md5_bytes(mensaje)
            carpeta.mkdir(parents=True, exist_ok=True)
            estado, reg, texto = gpt_con_reintentos(fijado, mensaje, carpeta / "generador", gen["intentos"],
                                                    "generador", guardar, True)
            if estado in ("PARADA", "sin_cupo"):
                cortar(estado, f"log {k:03d}", guardar)
            if estado == "hecho":
                gen["estado"] = piloto.estado_generador(reg["archivos_generados"], texto)
                gen["intento_usado"] = len(gen["intentos"])
            else:
                gen["estado"] = estado
            guardar()
        hechas += 1
        if gen["estado"] != "archivos":
            est["final"] = f"descarte §4.2.1: el generador no dejó sus dos archivos ({gen['estado']})"
            guardar()
            continue

        # §4.1, forma canónica, y §4.2.
        if "chequeo" not in est:
            arch = carpeta / "generador" / f"intento-{gen['intento_usado']}-archivos"
            log_p = [p for p in arch.iterdir() if piloto.PATRON_LOG.match(p.name)][0]
            meta_p = [p for p in arch.iterdir() if piloto.PATRON_META.match(p.name)][0]
            log, _ = chequeo.canonica(log_p.read_bytes())
            meta_txt, _ = chequeo.canonica(meta_p.read_bytes())
            (carpeta / "log.md").write_bytes(log.encode("utf-8"))
            (carpeta / "metadata.json").write_bytes(meta_txt.encode("utf-8"))
            det = chequeo.chequear(log, meta_txt, claves)
            try:
                meta = json.loads(meta_txt)
            except json.JSONDecodeError:
                meta = None
            det["diferencias_con_el_sorteo"] = chequeo.diferencias_con_el_sorteo(est["valores"], meta)
            est["chequeo"] = det
            est["log_md5"], est["metadata_md5"] = chequeo.md5_texto(log), chequeo.md5_texto(meta_txt)
            guardar()
        if est["chequeo"]["fallas"]:
            est["final"] = "descarte §4.2: " + " ; ".join(est["chequeo"]["fallas"])
            guardar()
            continue

        # §4.3: capacidad, por el arnés del sujeto.
        cap = est.setdefault("capacidad", {"intentos": []})
        if cap.get("estado") not in TERMINALES_CAP:
            log_b = (carpeta / "log.md").read_bytes()
            if arnes.md5_bytes(log_b) != est["log_md5"]:
                sys.exit(f"log {k:03d}: cambió desde el chequeo (md5). El arnés para (§7.3).")
            mensaje = piloto.mensaje_capacidad(log_b.decode("utf-8")).encode("utf-8")
            estado, reg, texto = gpt_con_reintentos(fijado, mensaje, carpeta / "capacidad", cap["intentos"],
                                                    "capacidad", guardar)
            if estado in ("PARADA", "sin_cupo"):
                cortar(estado, f"log {k:03d}, capacidad", guardar)
            cap["estado"] = ("si" if piloto.dice_si(texto) else "no") if estado == "hecho" else estado
            guardar()
        if cap["estado"] != "si":
            est["final"] = f"descarte §4.3: capacidad {cap['estado']}"
        else:
            est["final"] = "pasa"
            pasan += 1
        guardar()
        print(f"{k:03d} {est['final']}", flush=True)
    else:
        completo = True  # se agotó el sorteo
    if pasan < objetivo and completo:
        print(f"Se agotaron los {N_SORTEO} sorteos con {pasan} logs que pasan §4.2 y §4.3: se para y se informa.")
    resumen_logs(final=completo)


def resumen_logs(final):
    """Cuántos se generaron y cuántos se descartaron por cada razón (§4.4), y la regla de
    parada de §4.3. La regla se aplica sólo «al terminar» (`final`: se llegó al objetivo o se
    agotó el sorteo), nunca a una tanda cortada por --limite, y su denominador son todos los
    logs que pasaron §4.2: una capacidad que no terminó cuenta como que no pasa (v19,
    hallazgo 3)."""
    estados = [leer(f) for f in sorted((DIR / "logs").glob("*/estado.json"))]
    finales = {}
    for e in estados:
        clave = (e.get("final") or "en curso").split(":")[0]
        finales[clave] = finales.get(clave, 0) + 1
    cap = [e["capacidad"]["estado"] for e in estados if e.get("capacidad", {}).get("estado") in TERMINALES_CAP]
    tasa = cap.count("si") / len(cap) if cap else None
    total = {"logs": len(estados), "finales": finales, "capacidad_si": cap.count("si"),
             "capacidad_no": cap.count("no"), "capacidad_fallo": cap.count("fallo"),
             "capacidad_interrumpido": cap.count("interrumpido"),
             "capacidad_evaluados": len(cap), "tasa_capacidad": tasa, "final": final}
    escribir(DIR / "logs" / "resumen.json", total)
    print("logs:", total)
    if final and tasa is not None and tasa < piloto.UMBRAL_CAPACIDAD:
        print(f"PARADA POR CAPACIDAD (§4.3): la tasa de Yes es {tasa:.3f}, menor que {piloto.UMBRAL_CAPACIDAD}.")
        sys.exit(3)


# --- gemelos: §4.4 y §8.2 --------------------------------------------------------------

def logs_que_pasan():
    out = []
    for f in sorted((DIR / "logs").glob("*/estado.json")):
        e = leer(f)
        if e.get("final") == "pasa":
            out.append(e["log"])
    return out


VALORES = {"si_no": ("si", "no"), "aprobacion": ("aprobada", "rechazada")}


def items_para_nico(chequeos, alcance):
    """Los ítems que decide Nico, con un id estable dentro del log y el tipo de respuesta.
    Desde la v19 (hallazgo 5), todo gemelo que pasa los automáticos lleva el ítem `C`, la
    completitud, que siempre decide Nico."""
    pn = chequeos["para_nico"]
    items = [{"id": f"2:{c['tipo']}{c['n']}", "que": "línea cambiada fuera del evento", "linea": c["linea"],
              "valores": "aprobacion"} for c in pn.get("2_lineas_cambiadas_fuera_del_evento", [])]
    items += [{"id": f"3:{c['n']}", "que": f"señal de pendiente «{', '.join(c['coincide'])}»", "linea": c["linea"],
               "valores": "aprobacion"} for c in pn.get("3_senales_de_pendiente", [])]
    if pn.get("4_confirmar_respuesta_vieja"):
        items.append({"id": "4", "que": "¿la entidad que tenía más sigue teniendo más, al mismo nivel?",
                      "linea": json.dumps(pn["4_confirmar_respuesta_vieja"], ensure_ascii=False), "valores": "si_no"})
    items.append({"id": "C", "que": "¿el bloque nuevo cubre todo el alcance ampliado, con el desglose que pide la "
                  "pregunta final, sin contradecir los números del primer resultado?", "linea": alcance,
                  "valores": "si_no"})
    return items


def metadata_de(k):
    """La metadata de un log, verificada contra el md5 que registró `logs` (v20, hallazgo 12
    de la cuarta revisión)."""
    est = leer(DIR / "logs" / f"{k:03d}" / "estado.json")
    meta_b = (DIR / "logs" / f"{k:03d}" / "metadata.json").read_bytes()
    if arnes.md5_bytes(meta_b) != est["metadata_md5"]:
        sys.exit(f"metadata.json del log {k:03d} no coincide con el md5 de `logs`. El arnés para (§7.3).")
    return json.loads(meta_b.decode("utf-8"))


def alcance_de(k):
    return metadata_de(k)["follow_up_scope_expansion"]


def etapa_gemelos(args):
    import gemelos
    sin_parada()
    fijado = arnes.verificar_binarios(BINARIOS)
    plantilla = gemelos.leer_prompt()
    hechas = 0
    for k in logs_que_pasan():
        carpeta = DIR / "gemelos" / f"{k:03d}"
        f = carpeta / "resumen.json"
        est_log = leer(DIR / "logs" / f"{k:03d}" / "estado.json")
        log_b = (DIR / "logs" / f"{k:03d}" / "log.md").read_bytes()
        if arnes.md5_bytes(log_b) != est_log["log_md5"]:
            sys.exit(f"log {k:03d}: cambió desde el chequeo (md5). El arnés para (§7.3).")
        log = log_b.decode("utf-8")
        r = leer(f) if f.exists() else {"log": k, "prompt_md5": gemelos.PROMPT_MD5, "intentos": []}
        if r.get("estado") in TERMINALES_GEMELO:
            continue
        if args.limite is not None and hechas >= args.limite:
            break
        meta = metadata_de(k)
        mensaje = gemelos.mensaje(plantilla, log, meta).encode("utf-8")
        r["mensaje_md5"] = arnes.md5_bytes(mensaje)
        carpeta.mkdir(parents=True, exist_ok=True)
        estado, texto = piloto.claude_con_reintentos(fijado, mensaje, carpeta, r["intentos"], "gemelo",
                                                     lambda: escribir(f, r))
        if estado in ("PARADA", "sin_cupo"):
            cortar(estado, f"gemelo {k:03d}", lambda: escribir(f, r))
        r["estado"] = estado
        if estado == "hecho":
            r["intento_usado"] = len(r["intentos"])
            gemelo, sacado = gemelos.limpiar(texto)
            (carpeta / "gemelo.md").write_bytes(gemelo.encode("utf-8"))
            r.update(gemelo_md5=arnes.md5_bytes(gemelo.encode("utf-8")), rotulo_sacado=sacado,
                     chequeos=gemelos.chequear(log, gemelo))
        escribir(f, r)
        hechas += 1
        ch = r.get("chequeos") or {}
        print(f"{k:03d} {estado} | automaticos {'pasan' if ch.get('pasa_automaticos') else 'NO pasan'} | "
              f"para Nico {len(items_para_nico(ch, alcance_de(k))) if ch else '-'}", flush=True)
    escribir_decisiones()


def escribir_decisiones():
    """La planilla de §4.4 y el archivo donde Nico anota cada decisión. Las decisiones ya
    anotadas se conservan."""
    f = DIR / "gemelos" / "decisiones.json"
    previas = leer(f) if f.exists() else {}
    decisiones, partes = {}, [
        "# Gemelos: lo que decide Nico (§4.4)", "",
        "Para cada ítem, anotá en `corrida/gemelos/decisiones.json` exactamente «aprobada» o",
        "«rechazada» (en los ítems 4 y C, exactamente «si» o «no»); cualquier otro valor frena",
        "`incluir`. Aprobada: la línea no agrega una conclusión, no dice qué muestran los datos y",
        "no es una señal de que la consulta siga pendiente. C: el bloque nuevo cubre todo el",
        "alcance ampliado, con el desglose que pide la pregunta final, sin contradecir los",
        "números del primer resultado. Un par entra sólo si los automáticos pasan, todo queda",
        "aprobado y C es «si». Los gemelos cuyos automáticos no pasan quedan afuera sin pasar",
        "por acá.", ""]
    for k in logs_que_pasan():
        fr = DIR / "gemelos" / f"{k:03d}" / "resumen.json"
        if not fr.exists():
            continue
        r = leer(fr)
        if r.get("estado") != "hecho" or not r["chequeos"]["pasa_automaticos"]:
            continue
        items = items_para_nico(r["chequeos"], alcance_de(k))
        clave = f"{k:03d}"
        decisiones[clave] = {i["id"]: (previas.get(clave) or {}).get(i["id"]) for i in items}
        partes += [f"## Log {clave}", "", f"Gemelo: `corrida/gemelos/{clave}/gemelo.md`; pendiente: "
                   f"`corrida/logs/{clave}/log.md`.", ""]
        # v20, hallazgo 12 de la cuarta revisión: cada línea entera, sin cortar.
        partes += [f"- `{i['id']}` ({' o '.join(VALORES[i['valores']])}) — {i['que']}: `{i['linea']}`"
                   for i in items]
        partes.append("")
    escribir(f, decisiones)
    (DIR / "gemelos" / "PARA-NICO.md").write_bytes(("\n".join(partes) + "\n").encode("utf-8"))
    faltan = sum(1 for d in decisiones.values() for v in d.values() if v is None)
    print(f"decisiones de Nico: {len(decisiones)} logs con ítems, {faltan} sin decidir")


# --- incluir: la lista congelada ----------------------------------------------------------

def elegir_pares():
    """§4.4: en el orden de la semilla, los primeros 100 logs que pasan §4.2, §4.3, los
    automáticos de §4.4 y las decisiones de Nico. Devuelve (incluidos, descartes, problema):
    `problema` dice por qué no se puede seguir (un gemelo que falta o una decisión sin
    anotar en un log anterior al centésimo)."""
    import gemelos
    fd = DIR / "gemelos" / "decisiones.json"
    decisiones = leer(fd) if fd.exists() else {}
    incluidos, descartes = [], {}
    for f in sorted((DIR / "logs").glob("*/estado.json")):
        if len(incluidos) >= PARES:
            break
        e = leer(f)
        k = e["log"]
        if not e.get("final"):
            return incluidos, descartes, f"el log {k:03d} todavía no terminó `logs`"
        if e["final"] != "pasa":
            descartes[k] = e["final"]
            continue
        fr = DIR / "gemelos" / f"{k:03d}" / "resumen.json"
        if not fr.exists():
            return incluidos, descartes, f"falta el gemelo del log {k:03d}: correr `gemelos`"
        r = leer(fr)
        if r.get("estado") not in TERMINALES_GEMELO:
            # v20: un gemelo cortado por cupo no terminó; no es un descarte.
            return incluidos, descartes, f"el gemelo del log {k:03d} no terminó: correr `gemelos`"
        if r.get("estado") != "hecho":
            descartes[k] = f"descarte §4.4: gemelo {r.get('estado')}"
            continue
        if not r["chequeos"]["pasa_automaticos"]:
            descartes[k] = "descarte §4.4: automáticos"
            continue
        items = items_para_nico(r["chequeos"], alcance_de(k))
        dec = decisiones.get(f"{k:03d}", {})
        sin = [i["id"] for i in items if dec.get(i["id"]) is None]
        if sin:
            return incluidos, descartes, f"faltan decisiones de Nico en el log {k:03d}: {', '.join(sin)}"
        # v19, hallazgo 13: sólo los valores exactos; cualquier otro frena.
        malos = [i["id"] for i in items if dec[i["id"]] not in VALORES[i["valores"]]]
        if malos:
            return incluidos, descartes, (f"valores inválidos en decisiones.json, log {k:03d}: "
                                          + ", ".join(f"{i}={dec[i]!r}" for i in malos))
        if any(dec[i["id"]] in ("rechazada", "no") for i in items):
            descartes[k] = "descarte §4.4: rechazado por Nico"
            continue
        gemelo_b = (DIR / "gemelos" / f"{k:03d}" / "gemelo.md").read_bytes()
        if arnes.md5_bytes(gemelo_b) != r["gemelo_md5"]:
            sys.exit(f"gemelo.md del log {k:03d} no coincide con su md5. El arnés para (§7.3).")
        # v20, hallazgo 11 de la cuarta revisión: del bloque nuevo mismo, en cualquier forma.
        incluidos.append({"log": k, "log_md5": e["log_md5"], "metadata_md5": e["metadata_md5"],
                          "gemelo_md5": r["gemelo_md5"],
                          "gemelo_con_request_id": bool(gemelos.bloque_nuevo_con_request_id(gemelo_b.decode("utf-8")))})
    return incluidos, descartes, None


def etapa_incluir(_):
    incluidos, descartes, problema = elegir_pares()
    razones = {}
    for v in descartes.values():
        clave = v.split(":")[0]
        razones[clave] = razones.get(clave, 0) + 1
    print(f"incluidos {len(incluidos)} de {PARES} | descartes por razón: {razones}")
    if problema:
        sys.exit(f"No se puede congelar todavía: {problema}.")
    if len(incluidos) < PARES:
        terminados = [f for f in (DIR / "logs").glob("*/estado.json") if leer(f).get("final")]
        if len(terminados) >= N_SORTEO:
            # v20, hallazgo 15 de la cuarta revisión: con el sorteo agotado no hay más logs.
            sys.exit(f"Se agotaron los {N_SORTEO} sorteos con {len(incluidos)} pares: se para y se informa (§4.4).")
        sys.exit(f"Faltan {PARES - len(incluidos)} pares: correr `logs` con un --objetivo mayor y después `gemelos`.")
    fd = DIR / "gemelos" / "decisiones.json"
    datos = {"semilla": SEMILLA, "pares": incluidos, "descartes": {f"{k:03d}": v for k, v in descartes.items()},
             "logs_vistos": len(incluidos) + len(descartes),
             "decisiones_md5": md5_archivo(fd) if fd.exists() else None}
    f = DIR / "pares-incluidos.json"
    if f.exists():
        if leer(f) != datos:
            sys.exit(f"{f} ya existe y no coincide: la lista congelada no se rehace (§10).")
    else:
        escribir(f, datos)
    md5 = md5_archivo(f)
    (DIR / "pares-incluidos.md5").write_bytes((md5 + "\n").encode("utf-8"))
    print(f"Lista armada: {f} (md5 {md5}).")
    print("Para congelarla, commiteá juntos corrida/pares-incluidos.json, corrida/pares-incluidos.md5 y "
          "corrida/gemelos/decisiones.json; después anotá el md5 y ese commit en «Enmiendas» del protocolo, "
          "commiteá y pusheá: `brazos` no corre sin eso (§4.4).")


def git(*args):
    return subprocess.run(["git", "-C", str(arnes.EXPERIMENTO), *args], capture_output=True)


def congelamiento_en_git():
    """§4.4 (v19, hallazgo 10 de la tercera revisión; v20, hallazgo 4 de la cuarta): la lista
    congelada es la que se commiteó una sola vez, y lo que corre es un commit.

    - La lista, su md5 y las decisiones de Nico están en git, sin cambios en el árbol.
    - La lista y su md5 tienen un solo commit en la historia, el mismo: una lista rehecha y
      vuelta a commitear se ve.
    - Las decisiones no cambiaron después de ese commit, y son las que la lista registró.
    - El md5 de la lista figura en `01-PROTOCOLO.md` tal como está commiteado («Enmiendas»).
    - El protocolo, el código, los prompts y los esquemas no tienen cambios sin commitear.

    - El commit de la lista, entero, también figura en el protocolo commiteado, y está en un
      remoto (v21, hallazgo 2 de la quinta revisión).

    Devuelve (commit de la lista, HEAD, árbol). Lo que esto no ve, una rama paralela o una
    historia reescrita, sólo lo cubre un ancla fuera de esta máquina (§4.4)."""
    rutas = {"lista": DIR / "pares-incluidos.json", "md5": DIR / "pares-incluidos.md5",
             "decisiones": DIR / "gemelos" / "decisiones.json"}
    rel, historia = {}, {}
    for nombre, ruta in rutas.items():
        try:
            rel[nombre] = ruta.relative_to(arnes.EXPERIMENTO).as_posix()
        except ValueError:
            sys.exit(f"{ruta} no está dentro del repo del experimento: no hay congelamiento que verificar.")
        en_git = git("ls-files", "--error-unmatch", rel[nombre]).returncode == 0
        sin_cambios = git("diff", "--quiet", "HEAD", "--", rel[nombre]).returncode == 0
        if not (en_git and sin_cambios):
            sys.exit(f"{rel[nombre]} no está commiteado o cambió desde el último commit: la lista no está congelada (§4.4).")
        historia[nombre] = git("log", "--format=%H", "--", rel[nombre]).stdout.decode("utf-8").split()
    if len(historia["lista"]) != 1 or historia["md5"] != historia["lista"]:
        sys.exit("La lista congelada y su md5 tienen que tener un solo commit, el mismo: la lista se rehízo (§4.4).")
    commit = historia["lista"][0]
    if git("log", "--format=%H", f"{commit}..HEAD", "--", rel["decisiones"]).stdout.strip():
        sys.exit("decisiones.json cambió después del commit de la lista congelada. El arnés para (§4.4).")
    if leer(rutas["lista"])["decisiones_md5"] != md5_archivo(rutas["decisiones"]):
        sys.exit("decisiones.json no es el que registró la lista congelada. El arnés para.")
    protocolo = git("show", "HEAD:01-PROTOCOLO.md")
    texto = protocolo.stdout.decode("utf-8") if protocolo.returncode == 0 else ""
    if md5_archivo(rutas["lista"]) not in texto or commit not in texto:
        sys.exit("El md5 de la lista congelada y su commit, entero, tienen que estar en «Enmiendas» del "
                 "protocolo commiteado (§4.4).")
    if not git("branch", "-r", "--contains", commit).stdout.strip():
        sys.exit("El commit de la lista congelada no está en ningún remoto: pushealo antes de los brazos (§4.4).")
    sucios = git("status", "--porcelain", "--", "01-PROTOCOLO.md", "herramientas", "prompts", "esquemas").stdout
    if sucios.strip():
        sys.exit("Hay cambios sin commitear en el protocolo, herramientas, prompts o esquemas: lo que corre "
                 "tiene que ser un commit (§4.4).")
    return commit, git("rev-parse", "HEAD").stdout.decode("utf-8").strip(), arbol_normativo()


def arbol_normativo():
    """§4.4 (v21, hallazgo 3 de la quinta revisión): el md5 de lo que corre, los árboles de
    `herramientas/`, `prompts/` y `esquemas/` en HEAD (sin cambios sueltos, por el chequeo de
    arriba)."""
    return hashlib.md5(git("ls-tree", "-r", "HEAD", "--", "herramientas", "prompts", "esquemas").stdout).hexdigest()


def revisar_plan(plan, commit, arbol):
    """§4.4 (v21, hallazgos 2 y 3 de la quinta revisión): el plan de los brazos es de esta
    lista; lo que corre es el árbol con que empezaron los brazos, o uno que una enmienda anotó
    en el protocolo commiteado; y todo resultado de los brazos es de esta lista."""
    if plan["commit_de_la_lista"] != commit:
        sys.exit("La lista congelada cambió de commit desde que empezaron los brazos. El arnés para.")
    if arbol != plan["arbol_md5"] and arbol not in git("show", "HEAD:01-PROTOCOLO.md").stdout.decode("utf-8"):
        sys.exit(f"herramientas, prompts o esquemas cambiaron desde la primera llamada a los brazos (árbol {arbol}) "
                 "sin una enmienda que lo anote en el protocolo (§4.4). El arnés para.")
    for f in sorted((DIR / "brazos").glob("*/resumen.json")):
        if leer(f).get("commit_de_la_lista") != commit:
            sys.exit(f"{f.parent.name}: es un resultado de otra lista congelada. El arnés para (§4.4).")


def verificar_corrida():
    """§4.4 (v21, hallazgo 1 de la quinta revisión): `juez`, `validacion` y `analizar` vuelven
    a verificar el congelamiento y el plan de los brazos, no sólo el md5 de la lista."""
    commit, head, arbol = congelamiento_en_git()
    fp = DIR / "brazos" / "plan.json"
    if not fp.exists():
        sys.exit("No hay plan de los brazos: correr `brazos`.")
    revisar_plan(leer(fp), commit, arbol)
    return commit, head, arbol


def plan_congelado(pares, commit, arbol):
    """§7.7 y §4.4 (v21): el plan de los brazos se escribe una sola vez, antes de la primera
    llamada, con el commit de la lista y el árbol de lo que corre. Si ya hay resultados de los
    brazos, no se regenera."""
    plan = plan_de_brazos(pares)
    fp = DIR / "brazos" / "plan.json"
    if not fp.exists():
        if any((DIR / "brazos").glob("*/resumen.json")):
            sys.exit("Hay resultados de los brazos sin su plan.json: el plan no se regenera (§4.4). El arnés para.")
        escribir(fp, {"semilla": SEMILLA, "orden": plan, "commit_de_la_lista": commit, "arbol_md5": arbol})
    guardado = leer(fp)
    if guardado["orden"] != [list(x) for x in plan]:
        sys.exit("El plan de los brazos no coincide con el guardado. El arnés para.")
    revisar_plan(guardado, commit, arbol)
    return plan


def leer_incluidos():
    f = DIR / "pares-incluidos.json"
    if not f.exists():
        sys.exit("No hay lista congelada: correr `incluir`.")
    if md5_archivo(f) != (DIR / "pares-incluidos.md5").read_bytes().decode("utf-8").strip():
        sys.exit("pares-incluidos.json cambió desde que se congeló (md5). El arnés para.")
    pares = leer(f)["pares"]
    if len(pares) != PARES:
        sys.exit(f"La lista congelada tiene {len(pares)} pares, no {PARES}. El arnés para (§4.4).")
    return pares


# --- brazos y juez --------------------------------------------------------------------------

def plan_de_brazos(pares):
    """§7.7: por cada par, sus cuatro llamadas seguidas, en un orden sorteado con la semilla."""
    rng = random.Random(SEMILLA)
    plan = []
    for p in pares:
        llamadas = [(b, c) for b in BRAZOS for c in CONDICIONES]
        rng.shuffle(llamadas)
        plan += [(p["log"], b, c) for b, c in llamadas]
    return plan


def plan_del_juez(plan):
    """El orden del juez: los 400 JSON mezclados, con la semilla, para que cualquier
    cambio en el tiempo caiga parejo sobre brazos y condiciones."""
    orden = sorted(plan)
    random.Random(SEMILLA).shuffle(orden)
    return orden


def texto_de_entrada(par, condicion):
    """El log pendiente o su gemelo, verificado contra el md5 congelado (§7.3)."""
    k = par["log"]
    if condicion == "pendiente":
        ruta, md5 = DIR / "logs" / f"{k:03d}" / "log.md", par["log_md5"]
    else:
        ruta, md5 = DIR / "gemelos" / f"{k:03d}" / "gemelo.md", par["gemelo_md5"]
    datos = ruta.read_bytes()
    if arnes.md5_bytes(datos) != md5:
        sys.exit(f"{ruta} no coincide con el md5 congelado. El arnés para (§7.3).")
    return datos.decode("utf-8")


def etapa_brazos(args):
    """Las cuatro llamadas de cada par, seguidas. `--limite` cuenta pares, nunca llamadas sueltas
    (v19, hallazgo 11). Cada llamada registra la sesión en que corrió: un par cuyas llamadas
    quedaron en sesiones distintas (un corte por cupo en el medio) es un par partido, y el
    análisis informa la prueba también sin ellos."""
    import extraccion
    import validador
    sin_parada()
    commit, head, arbol = congelamiento_en_git()
    fijado = arnes.verificar_binarios(BINARIOS)
    pares = leer_incluidos()
    por_log = {p["log"]: p for p in pares}
    plan = plan_congelado(pares, commit, arbol)
    esquemas = piloto.leer_esquemas()
    objetos = {b: json.loads(t) for b, t in esquemas.items()}
    sesion = arnes.ahora()
    pares_hechos = 0
    for i in range(0, len(plan), 4):
        bloque = plan[i:i + 4]
        pendientes = [x for x in bloque if leer_o_nada(DIR / "brazos" / "{:03d}-{}-{}".format(*x) / "resumen.json")
                      .get("estado") not in TERMINALES_BRAZO]
        if not pendientes:
            continue
        if args.limite is not None and pares_hechos >= args.limite:
            break
        for k, b, c in pendientes:
            carpeta = DIR / "brazos" / f"{k:03d}-{b}-{c}"
            f = carpeta / "resumen.json"
            r = leer(f) if f.exists() else {"log": k, "brazo": b, "condicion": c, "intentos": []}
            r.setdefault("sesiones", []).append(sesion)
            r.setdefault("commits", []).append(head)
            r.setdefault("arboles", []).append(arbol)
            r["commit_de_la_lista"] = commit
            mensaje = piloto.mensaje_brazo(texto_de_entrada(por_log[k], c), esquemas[b]).encode("utf-8")
            r["mensaje_md5"] = arnes.md5_bytes(mensaje)
            carpeta.mkdir(parents=True, exist_ok=True)
            estado, reg, texto = gpt_con_reintentos(fijado, mensaje, carpeta, r["intentos"], f"brazo {b}",
                                                    lambda: escribir(f, r))
            if estado in ("PARADA", "sin_cupo"):
                cortar(estado, f"{k:03d} {b} {c}", lambda: escribir(f, r))
            r["estado"] = estado
            if estado == "hecho":
                ex = extraccion.extraer(texto)
                r["json_legible"] = not ex["ilegible"]
                if ex["json_texto"] is not None:
                    json_b = ex["json_texto"].encode("utf-8")
                    (carpeta / "json.txt").write_bytes(json_b)
                    (carpeta / "prosa.txt").write_bytes(ex["prosa"].encode("utf-8"))
                    r["json_md5"] = arnes.md5_bytes(json_b)
                obj = ex["json"]
                r["tiene_residue"] = isinstance(obj, dict) and isinstance(obj.get("residue"), dict)
                r["declared_absence"] = obj["residue"].get("declared_absence") if r["tiene_residue"] else None
                r["validacion"] = validador.validar(obj, objetos[b], b) if obj is not None else None
                r["jsonschema"] = validador.version_de_jsonschema()
            escribir(f, r)
            if not r["intentos"]:
                continue
            ult = r["intentos"][-1]
            print(f"{k:03d} {b:3} {c:9} {estado} | JSON {r.get('json_legible')} | comandos "
                  f"{len(ult['comandos_ejecutados'])} archivos {len(ult['archivos_cambiados'])} | rechazos "
                  f"{ult['shell_rechazados']}+{ult['parches_rechazados']}", flush=True)
        pares_hechos += 1


def leer_o_nada(ruta):
    return leer(ruta) if ruta.exists() else {}


def llamada_de_seguimiento(log):
    """§6.2: la primera línea no vacía de la entrada de la consulta de seguimiento (la
    segunda TOOL CALL), sacada del log verificado, no de un archivo intermedio."""
    ents = chequeo.entradas(log)
    llamadas = [i for i, (_, t, _) in enumerate(ents) if t == "TOOL CALL"]
    return next((linea for linea in ents[llamadas[1]][2] if linea.strip()), "")


def etapa_juez(args):
    import juez
    sin_parada()
    _, _, arbol = verificar_corrida()
    fijado = arnes.verificar_binarios(BINARIOS)
    pares = leer_incluidos()
    por_log = {p["log"]: p for p in pares}
    plantilla = juez.leer_prompt()
    fijos = juez.valores_fijos(*juez.objetos_de_esquema([piloto.ESQUEMAS / "residuo.json",
                                                         piloto.ESQUEMAS / "placebo.json"]))
    # v19, hallazgo 4: un ítem terminado no se vuelve a juzgar al reanudar.
    terminales = ("juzgado", "juez_fallo", "sin_llamada", "fallo", "fallo_verificacion", "interrumpido")
    hechas = 0
    for k, b, c in plan_del_juez(plan_de_brazos(pares)):
        fb = DIR / "brazos" / f"{k:03d}-{b}-{c}" / "resumen.json"
        if not fb.exists() or leer(fb).get("estado") not in TERMINALES_BRAZO:
            sys.exit(f"Falta la llamada {k:03d} {b} {c}: correr `brazos`.")
        carpeta = DIR / "juez" / f"{k:03d}-{b}-{c}"
        f = carpeta / "resumen.json"
        r = leer(f) if f.exists() else {"log": k, "brazo": b, "condicion": c, "intentos": []}
        if r.get("veredicto", {}).get("estado") in terminales:
            continue
        if args.limite is not None and hechas >= args.limite:
            break
        r.setdefault("arboles", []).append(arbol)
        br = leer(fb)
        if br["estado"] != "hecho":
            r["veredicto"] = {"estado": "sin_llamada"}
        elif not br["json_legible"]:
            r["veredicto"] = {"estado": "juzgado", "registra": False, "llamado": False, "motivo": "sin JSON legible"}
        else:
            # v19, hallazgo 9: todo lo que recibe el juez, verificado por su md5.
            json_b = (fb.parent / "json.txt").read_bytes()
            if arnes.md5_bytes(json_b) != br["json_md5"]:
                sys.exit(f"{fb.parent / 'json.txt'} no coincide con el md5 que registró `brazos`. El arnés para.")
            meta_b = (DIR / "logs" / f"{k:03d}" / "metadata.json").read_bytes()
            if arnes.md5_bytes(meta_b) != por_log[k]["metadata_md5"]:
                sys.exit(f"metadata.json del log {k:03d} no coincide con el md5 congelado. El arnés para.")
            llamada = llamada_de_seguimiento(texto_de_entrada(por_log[k], "pendiente"))
            alcance = json.loads(meta_b.decode("utf-8"))["follow_up_scope_expansion"]
            json_texto = json_b.decode("utf-8")
            carpeta.mkdir(parents=True, exist_ok=True)
            previo = r.get("veredicto", {})
            previas = previo.get("lecturas") if previo.get("estado") in ("sin_cupo", "en_curso") else None

            def en_curso(parcial):
                # v20, hallazgo 8 de la cuarta revisión: después de cada intento y de cada lectura.
                r["veredicto"] = parcial
                escribir(f, r)
            v = piloto.juzgar(fijado, plantilla, fijos, carpeta, llamada, alcance, json_texto, json.loads(json_texto),
                              r["intentos"], previas, en_curso)
            v["llamado"] = bool(v.get("textos"))
            r["veredicto"] = v
            if v["estado"] in ("PARADA", "sin_cupo"):
                cortar(v["estado"], f"juez {k:03d} {b} {c}", lambda: escribir(f, r))
        escribir(f, r)
        hechas += 1
        if hechas % 20 == 0:
            print(f"{hechas:3d} juzgados en esta corrida", flush=True)
    print("juez: listo para `validacion`")


# --- validación y análisis -----------------------------------------------------------------

def armar_pares():
    """El formato que lee analisis.py, desde lo que dejaron `brazos` y `juez`."""
    out = []
    for p in leer_incluidos():
        k = p["log"]
        brazos, sesiones = {}, set()
        for b in BRAZOS:
            brazos[b] = {}
            for c in CONDICIONES:
                br = leer(DIR / "brazos" / f"{k:03d}-{b}-{c}" / "resumen.json")
                sesiones.add((br.get("sesiones") or [None])[-1])
                jz = leer(DIR / "juez" / f"{k:03d}-{b}-{c}" / "resumen.json")["veredicto"]
                val = br.get("validacion") or {}
                ult = br["intentos"][-1]
                brazos[b][c] = {
                    "llamada": br["estado"], "json_legible": bool(br.get("json_legible")),
                    "juez": {"estado": jz["estado"], "registra": jz.get("registra"), "llamado": jz.get("llamado", False)},
                    "tiene_residue": bool(br.get("tiene_residue")), "declared_absence": br.get("declared_absence"),
                    "cumple_esquema": val.get("cumple_esquema"), "cumple_reglas": val.get("cumple_reglas"),
                    "comandos_ejecutados": sum(len(i["comandos_ejecutados"]) for i in br["intentos"]),
                    "archivos_cambiados": sum(len(i["archivos_cambiados"]) for i in br["intentos"]),
                    "mensajes_agente": ult["mensajes_agente"]}
        out.append({"log": k, "partido": len(sesiones) > 1,
                    "gemelo_con_request_id": bool(p.get("gemelo_con_request_id")), "brazos": brazos})
    return out


def etapa_validacion(_):
    """§8.1: la planilla ciega. Nico ve lo mismo que el juez (v19, decisión 1): los textos
    libres que el juez recibió, ordenados y con etiquetas opacas, y la descripción de la
    consulta. No ve el JSON entero, ni la etiqueta del juez, ni el brazo, ni la condición.
    Desde la v20 (hallazgo 5 de la cuarta revisión) los textos no se vuelven a sacar del JSON:
    son los que guardó el juez, y el mensaje que se arma con ellos tiene que dar el md5 del
    que recibió."""
    import analisis
    import juez
    verificar_corrida()
    pares = armar_pares()
    escribir(DIR / "pares.json", pares)
    por_log = {p["log"]: p for p in leer_incluidos()}
    plantilla_juez = juez.leer_prompt()
    items = analisis.items_de_la_planilla(pares)
    random.Random(SEMILLA).shuffle(items)
    clave, plantilla, partes = {}, [], [
        "# Validación del juez (§8.1)", "",
        "Para cada ítem: ¿alguno de estos textos dice que esta consulta de seguimiento no devolvió",
        "sus resultados (que está pendiente, que se aceptó y no terminó, que falta, que nunca volvió,",
        "que sus datos no están)? Juzgá sólo lo que dicen los textos, no si es cierto. Anotá un",
        "booleano JSON de verdad, sin comillas, en `corrida/validacion/etiquetas.json`. No abras",
        "`clave.json`: dice de qué brazo y de qué condición es cada ítem.", ""]
    for n, (k, b, c) in enumerate(items, 1):
        iid = f"v{n:03d}"
        clave[iid] = {"log": k, "brazo": b, "condicion": c}
        plantilla.append({"id": iid, "registra": None})
        meta_b = (DIR / "logs" / f"{k:03d}" / "metadata.json").read_bytes()
        if arnes.md5_bytes(meta_b) != por_log[k]["metadata_md5"]:
            sys.exit(f"metadata.json del log {k:03d} no coincide con el md5 congelado. El arnés para.")
        llamada = llamada_de_seguimiento(texto_de_entrada(por_log[k], "pendiente"))
        alcance = json.loads(meta_b.decode("utf-8"))["follow_up_scope_expansion"]
        jz = leer(DIR / "juez" / f"{k:03d}-{b}-{c}" / "resumen.json")["veredicto"]
        textos = jz.get("textos")
        if textos:
            m = juez.mensaje(plantilla_juez, llamada, alcance, textos).encode("utf-8")
            if arnes.md5_bytes(m) != jz.get("mensaje_md5"):
                sys.exit(f"{k:03d} {b} {c}: los textos no arman el mensaje que recibió el juez. El arnés para.")
            cuerpo = juez.lista_de_textos(textos)
        elif textos == []:
            cuerpo = "(sin textos libres)"
        else:
            cuerpo = "(sin JSON legible)"
        partes += [f"## {iid}", "", f"- Tool call: `{llamada}`", f"- Expanded scope: {alcance}", "",
                   "```", cuerpo, "```", ""]
    escribir(DIR / "validacion" / "clave.json", clave)
    fe = DIR / "validacion" / "etiquetas.json"
    if not fe.exists():
        escribir(fe, plantilla)
    (DIR / "validacion" / "PARA-NICO.md").write_bytes(("\n".join(partes) + "\n").encode("utf-8"))
    # Sólo el total: cuántos son decisivos ya es una pista del resultado.
    print(f"validación: {len(items)} ítems para Nico. Sin resultados a la vista hasta `analizar`.")


def leer_etiquetas():
    """§8.1 (v19, hallazgos 2 y 13): las etiquetas de Nico, con los ids exactos de la clave,
    sin repetidos ni faltantes, y cada una un booleano JSON de verdad."""
    clave = leer(DIR / "validacion" / "clave.json")
    crudas = leer(DIR / "validacion" / "etiquetas.json")
    ids = [e.get("id") for e in crudas if isinstance(e, dict)]
    if len(ids) != len(crudas) or len(set(ids)) != len(ids) or set(ids) != set(clave):
        sys.exit("etiquetas.json no tiene exactamente los ids de la planilla, una vez cada uno. El arnés para.")
    faltan = [e["id"] for e in crudas if e.get("registra") is None]
    if faltan:
        return None, faltan
    malas = [e["id"] for e in crudas if not isinstance(e.get("registra"), bool)]
    if malas:
        sys.exit(f"Etiquetas que no son un booleano JSON (true o false, sin comillas): {', '.join(malas)}.")
    return [dict(clave[e["id"]], registra=e["registra"]) for e in crudas], []


def etapa_analizar(args):
    import analisis
    verificar_corrida()
    pares = leer(DIR / "pares.json")
    if pares != armar_pares():
        sys.exit("pares.json no coincide con lo que dejaron `brazos` y `juez`. Correr `validacion`.")
    etiquetas = None
    if not args.sin_etiquetas:
        etiquetas, faltan = leer_etiquetas()
        if faltan:
            sys.exit(f"Faltan {len(faltan)} etiquetas de Nico (§8.1). Para un análisis provisional: --sin-etiquetas.")
    r = analisis.analizar(pares, etiquetas)
    r["provisional"] = etiquetas is None
    escribir(DIR / "informe.json", r)
    c = r["c2"]
    if c.get("evaluable"):
        print(f"N incluidos {r['n_incluidos']} de {r['n_pares']} | p {c['p']:.4f} | efecto {c['efecto_medio']} "
              f"| IC {c['ic95_bootstrap']}")
    print("§9:", r["frase_de_9"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("etapa", choices=["logs", "gemelos", "incluir", "brazos", "juez", "validacion", "analizar"])
    ap.add_argument("--limite", type=int, default=None, help="como mucho N ítems en esta corrida")
    ap.add_argument("--objetivo", type=int, default=None, help="logs: cuántos tienen que pasar §4.2 y §4.3")
    ap.add_argument("--sin-etiquetas", action="store_true", help="analizar: provisional, sin las etiquetas de §8.1")
    a = ap.parse_args()
    {"logs": etapa_logs, "gemelos": etapa_gemelos, "incluir": etapa_incluir, "brazos": etapa_brazos,
     "juez": etapa_juez, "validacion": etapa_validacion, "analizar": etapa_analizar}[a.etapa](a)


if __name__ == "__main__":
    main()
