"""El gemelo limpio: su mensaje y los cinco chequeos de §4.4 (protocolo v11).

Funciones puras, sin llamadas a modelos. Lo que necesita una decisión humana (las
líneas cambiadas fuera del evento reemplazado, las coincidencias de la expresión
regular y el chequeo 4 cuando el formato no se deja leer) sale en listas para que
Nico las apruebe o las rechace.
"""
import difflib
import hashlib
import re
from pathlib import Path

import chequeo

PROMPT = Path(__file__).resolve().parent.parent / "prompts" / "gemelo.txt"
PROMPT_MD5 = "8a1988396c48e59f013a7ad3cf64b452"

# §4.4.3, textual.
RE_PENDIENTE = re.compile(
    r"pend|process|progress|accept|queue|async|start|running|wait|submit|acknowledg|poll|request_id|partial"
    r"|incomplet|not yet|still", re.I)


def leer_prompt():
    datos = PROMPT.read_bytes()
    if hashlib.md5(datos).hexdigest() != PROMPT_MD5:
        raise SystemExit(f"{PROMPT.name} no tiene el md5 congelado {PROMPT_MD5}")
    return datos.decode("utf-8")


def mensaje(plantilla, log, meta):
    """§8.2: el prompt con el log canónico (sin su salto final) y los dos campos de la metadata."""
    valores = {"{log_content}": log.rstrip("\n"),
               "{follow_up_scope_expansion}": meta["follow_up_scope_expansion"],
               "{missing_follow_up_behavior}": meta["missing_follow_up_behavior"]}
    texto = plantilla
    for marca, valor in valores.items():
        if texto.count(marca) != 1:
            raise SystemExit(f"El marcador {marca} aparece {texto.count(marca)} veces")
        texto = texto.replace(marca, valor)
    return texto


def _lineas_por_entrada(log):
    """Cada línea del log con el índice de su entrada (-1 antes del primer encabezado)."""
    out, actual = [], -1
    for linea in log.rstrip("\n").split("\n"):
        if chequeo.RE_ENCABEZADO.match(linea):
            actual += 1
        out.append((linea, actual))
    return out


def _texto_de_entrada(ents, i):
    hora, tipo, cuerpo = ents[i]
    lineas = list(cuerpo)
    while lineas and not lineas[-1].strip():
        lineas.pop()
    return "\n".join([f"[{hora}] {tipo}"] + lineas)


def _indices(ents):
    """Primer resultado, consulta de seguimiento, la entrada que sigue y la pregunta final."""
    llamadas = [i for i, (_, t, _) in enumerate(ents) if t == "TOOL CALL"]
    if len(llamadas) < 2:
        return None
    seg = llamadas[1]
    primero = next((i for i, (_, t, _) in enumerate(ents) if t == "TOOL RESULT" and i < seg), None)
    final = max((i for i, (_, t, _) in enumerate(ents) if t == "USER"), default=None)
    siguiente = seg + 1 if seg + 1 < len(ents) else None
    return {"primero": primero, "seguimiento": seg, "evento": siguiente, "final": final}


def chequear(pendiente, gemelo):
    """§4.4 sobre el log pendiente y su gemelo, los dos en forma canónica."""
    ep, eg = chequeo.entradas(pendiente), chequeo.entradas(gemelo)
    ip, ig = _indices(ep), _indices(eg)
    det = {"automaticos": {}, "para_nico": {}}
    if ip is None or ig is None or None in ip.values() or None in ig.values():
        det["automaticos"]["estructura"] = "no se encontraron el primer resultado, el seguimiento, su evento o la pregunta final"
        det["pasa_automaticos"] = False
        return det

    # 1. Primer resultado, consulta de seguimiento y pregunta final, textuales; y el evento
    #    reemplazado es ahora un TOOL RESULT.
    intactos = {clave: _texto_de_entrada(ep, ip[clave]) == _texto_de_entrada(eg, ig[clave])
                for clave in ("primero", "seguimiento", "final")}
    det["automaticos"]["1_intactos"] = intactos
    det["automaticos"]["1_evento_es_tool_result"] = eg[ig["evento"]][1] == "TOOL RESULT"

    # 2. Diff línea por línea, fuera del evento reemplazado.
    lp, lg = _lineas_por_entrada(pendiente), _lineas_por_entrada(gemelo)
    cambios = []
    sm = difflib.SequenceMatcher(None, [l for l, _ in lp], [l for l, _ in lg], autojunk=False)
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == "equal":
            continue
        cambios += [{"tipo": "-", "n": k + 1, "linea": lp[k][0]} for k in range(a1, a2) if lp[k][1] != ip["evento"]]
        cambios += [{"tipo": "+", "n": k + 1, "linea": lg[k][0]} for k in range(b1, b2) if lg[k][1] != ig["evento"]]
    det["para_nico"]["2_lineas_cambiadas_fuera_del_evento"] = cambios

    # 3. Señales de pendiente fuera del primer resultado.
    seg_texto = _texto_de_entrada(eg, ig["seguimiento"]).split("\n")
    coincidencias = []
    for k, (linea, ent) in enumerate(lg):
        if ent == ig["primero"]:
            continue
        hallado = sorted({m.group(0).lower() for m in RE_PENDIENTE.finditer(linea)})
        if hallado:
            coincidencias.append({"n": k + 1, "linea": linea, "coincide": hallado,
                                  "en_la_llamada_de_seguimiento": ent == ig["seguimiento"] and linea in seg_texto})
    det["para_nico"]["3_senales_de_pendiente"] = coincidencias

    # 4. La respuesta vieja sigue siendo la correcta.
    dp = chequeo.dominante(ep[ip["primero"]][2])
    nuevo = eg[ig["evento"]][2]
    dn = chequeo.dominante(nuevo)
    c4 = {"categoria": dp["nombres"], "entidad": dp.get("entidad"),
          "categoria_en_el_nuevo": dn["nombres"], "entidad_en_el_nuevo": dn.get("entidad")}
    mismo = lambda a, b: a is not None and b is not None and a.strip().lower() == b.strip().lower()  # noqa: E731
    if dp["nombres"] and dn["nombres"] and any(mismo(a, b) for a in dp["nombres"] for b in dn["nombres"]):
        c4["metodo"] = "estructura"
        c4["resultado"] = "ok" if mismo(dp.get("entidad"), dn.get("entidad")) else "no"
    else:
        # Respaldo: la hoja mayor entre las del nivel más profundo, que son las entidades;
        # un total suelto («total_…: 3,078») queda arriba y no compite.
        hs = chequeo.hojas(nuevo)
        if hs:
            fondo = max(h[2] for h in hs)
            hs = [h for h in hs if h[2] == fondo]
        if hs and dp.get("entidad"):
            arriba = max(hs, key=lambda h: h[1])[0]
            c4["metodo"] = "hoja mayor del nivel más profundo del bloque nuevo"
            c4["hoja_mayor"] = arriba
            c4["resultado"] = "ok" if mismo(arriba, dp["entidad"]) else "a_mano"
        else:
            c4["metodo"] = "ninguno"
            c4["resultado"] = "a_mano"
    det["automaticos"]["4_respuesta_vieja"] = c4
    if c4["resultado"] == "a_mano":
        det["para_nico"]["4_confirmar_respuesta_vieja"] = c4

    # 5. El bloque nuevo tiene al menos dos entidades con un número.
    n5 = len(chequeo.lineas_nombre_numero(nuevo))
    det["automaticos"]["5_entidades_con_numero"] = n5

    det["pasa_automaticos"] = (all(intactos.values()) and det["automaticos"]["1_evento_es_tool_result"]
                               and c4["resultado"] != "no" and n5 >= 2)
    det["pendiente_de_nico"] = bool(cambios or coincidencias or c4["resultado"] == "a_mano")
    return det
