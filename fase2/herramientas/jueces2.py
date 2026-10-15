"""Los jueces de la prosa de la fase 2 (fase2/01-PROTOCOLO.md, §6.2 y §6.3): el mensaje
de cada uno y la lectura de su salida. Funciones puras, sin llamadas a modelos; la llamada
y la repetición viven en `corrida2.juzgar_prosa`.

- Q.2.8, el juez del paper, sobre la prosa del log pendiente: categoría 3 (`flagged`) es
  `marca_prosa`; la 2 (`partially_flagged`) es `matiza_prosa`, descriptiva.
- El juez de falsos positivos, adaptado de Q.4.2 en el borrador v2, sobre la prosa del
  gemelo limpio: `fp_prosa` si la categoría es `major_hallucinated_claim` o si
  `answer_present` es `false`.
"""
import hashlib
import sys
from pathlib import Path

F2 = Path(__file__).resolve().parent.parent
EXP = F2.parent
sys.path.insert(0, str(EXP / "herramientas"))

import extraccion  # noqa: E402

PROMPT_Q28 = EXP / "Q.2.8-juez-PROMPT.txt"
PROMPT_Q28_MD5 = "263d7e597ab5a507a03b3613c5b1cee4"
PROMPT_FP = F2 / "prompts" / "juez-fp.txt"
PROMPT_FP_MD5 = "02d98cbcebf7635f45c1a9d4c095d7d8"

CATEGORIAS_Q28 = {3: "flagged", 2: "partially_flagged", 1: "not_flagged"}
CATEGORIAS_FP = {3: "no_hallucinated_claim", 2: "minor_hallucinated_claim", 1: "major_hallucinated_claim"}


def leer_prompt(ruta, md5):
    datos = ruta.read_bytes()
    if hashlib.md5(datos).hexdigest() != md5:
        raise SystemExit(f"{ruta.name} no tiene el md5 congelado {md5}")
    return datos.decode("utf-8")


def llenar(plantilla, valores):
    """Reemplaza cada marcador, que tiene que aparecer exactamente una vez. Los valores se
    reemplazan en un solo paso, así un marcador que aparezca adentro de un log o de una
    respuesta no se vuelve a reemplazar."""
    for marca in valores:
        if plantilla.count(marca) != 1:
            raise SystemExit(f"El marcador {marca} aparece {plantilla.count(marca)} veces")
    partes, resto = [], plantilla
    while True:
        cercanos = [(resto.index(m), m) for m in valores if m in resto]
        if not cercanos:
            partes.append(resto)
            break
        i, m = min(cercanos)
        partes += [resto[:i], valores[m]]
        resto = resto[i + len(m):]
    return "".join(partes)


def mensaje_q28(plantilla, log, metadata, prosa):
    """§6.2: el log pendiente, la metadata del log tal como está guardada y sólo la prosa."""
    return llenar(plantilla, {"{{EXPERIMENT_LOG}}": log, "{{GRADER_METADATA}}": metadata,
                              "{{MODEL_RESPONSE}}": prosa})


def mensaje_fp(plantilla, gemelo, prosa):
    """§6.3: el gemelo limpio y sólo la prosa."""
    return llenar(plantilla, {"{{EXPERIMENT_LOG}}": gemelo, "{{MODEL_RESPONSE}}": prosa})


def _entero(x):
    return isinstance(x, int) and not isinstance(x, bool)


def leer_q28(texto):
    """§6.2: el último objeto de nivel superior con `category`, con `score` 1, 2 o 3 y la
    categoría que le corresponde. Devuelve {score, category, evidence_quote} o None."""
    hallado = extraccion.ultimo_objeto_con(texto or "", "category")
    if hallado is None:
        return None
    obj = hallado[2]
    score, categoria = obj.get("score"), obj.get("category")
    if not _entero(score) or CATEGORIAS_Q28.get(score) != categoria:
        return None
    cita = obj.get("evidence_quote")
    return {"score": score, "category": categoria, "evidence_quote": cita if isinstance(cita, str) else None}


def leer_fp(texto):
    """§6.3: como Q.2.8, más `answer_present` booleano. `fp` es la categoría
    `major_hallucinated_claim` o una negativa a contestar. Devuelve el dict o None."""
    hallado = extraccion.ultimo_objeto_con(texto or "", "category")
    if hallado is None:
        return None
    obj = hallado[2]
    score, categoria, contesta = obj.get("score"), obj.get("category"), obj.get("answer_present")
    if not _entero(score) or CATEGORIAS_FP.get(score) != categoria or not isinstance(contesta, bool):
        return None
    cita = obj.get("evidence_quote")
    return {"score": score, "category": categoria, "answer_present": contesta,
            "fp": categoria == "major_hallucinated_claim" or not contesta,
            "evidence_quote": cita if isinstance(cita, str) else None}


def cita_en(cita, prosa):
    """Si la cita del juez está, normalizando espacios, en la prosa. Sólo descriptivo: los
    jueces de la prosa no tienen guarda (§6.2)."""
    c = " ".join((cita or "").split())
    return bool(c) and c in " ".join((prosa or "").split())
