"""El juez «registra» (protocolo v20, §6.2): sus textos, su mensaje, la lectura de su salida
y la guarda.

Desde la v19 el juez no ve el JSON: ve sólo sus textos libres, ordenados y con etiquetas
opacas, para que no pueda reconocer el brazo (hallazgo 1 de la tercera revisión). Desde la
v20, los campos del esquema que no son prosa (identificadores, referencias, links, hashes,
fechas y enums) no le llegan (hallazgo 2 de la cuarta). Funciones puras, sin llamadas a
modelos; la llamada y la repetición viven en `piloto.juzgar`.
"""
import hashlib
import json
import re
from pathlib import Path

import extraccion

PROMPT = Path(__file__).resolve().parent.parent / "prompts" / "juez.txt"
PROMPT_MD5 = "528761ba0ee3c66ffc55ff36dd058de9"
CLAVE = "records_missing_followup"
# §6.2 (v20, hallazgo 2 de la cuarta revisión): las claves de los dos esquemas cuyo valor no
# es prosa. Identificadores y referencias (`origin` es, según el esquema, el reviewer_id; `record`
# es el link o identificador de un registro), formatos que delatan al residuo (`link`, `hash`,
# `date`) y los campos de enum. Pasan los ocho campos de prosa (title, description, location,
# declaration, text, detail, remedy_adjustment, risk_record) y cualquier clave que no esté en
# ningún esquema: un registro escrito en un campo inventado no se pierde.
CLAVES_EXCLUIDAS = {"id", "origin", "finding_ref", "reviewer_ref", "debt_id", "reference", "lead", "record",
                    "link", "hash", "date",
                    "severity", "final_state", "against", "type", "class", "refutation_type", "gap_reason"}
CAMPOS_DE_PROSA = {"title", "description", "location", "declaration", "text", "detail", "remedy_adjustment",
                   "risk_record"}
CONTENEDORES = {"findings", "residue", "items", "evidence", "verification", "fix_verification", "lead_acceptance",
                "declared_absence", "requires_human_attention"}
# §6.2 (v21, hallazgo 4 de la quinta revisión): un valor sin ningún espacio que no es una
# palabra (letras, con guiones o apóstrofos) es técnico: un hash, un link, una fecha, un id, un
# token del esquema. No llega al juez, bajo ninguna clave. Una clave contenedora escrita como
# string no se descarta por su clave: en A2b `residue` es una clave desconocida, y descartarla
# sólo en A2 haría perder un registro en un brazo y no en el otro.
RE_PALABRA = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*")


def es_tecnico(valor):
    v = valor.strip()
    return bool(v) and not re.search(r"\s", v) and not RE_PALABRA.fullmatch(v)


def leer_prompt():
    datos = PROMPT.read_bytes()
    if hashlib.md5(datos).hexdigest() != PROMPT_MD5:
        raise SystemExit(f"{PROMPT.name} no tiene el md5 congelado {PROMPT_MD5}")
    return datos.decode("utf-8")


def valores_fijos(*esquemas):
    """Todos los valores de `enum` y de `const` de texto de los esquemas."""
    out = set()

    def recorrer(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == "enum" and isinstance(v, list):
                    out.update(s for s in v if isinstance(s, str))
                elif k == "const" and isinstance(v, str):
                    out.add(v)
                else:
                    recorrer(v)
        elif isinstance(x, list):
            for v in x:
                recorrer(v)
    for e in esquemas:
        recorrer(e)
    return out


def textos_citables(obj, fijos, clave=None):
    """Los valores de texto del JSON que no son un valor fijo de los esquemas y cuya clave no
    es una de las excluidas. Un string dentro de una lista hereda la clave de la lista."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from textos_citables(v, fijos, k)
    elif isinstance(obj, list):
        for v in obj:
            yield from textos_citables(v, fijos, clave)
    elif isinstance(obj, str):
        if clave not in CLAVES_EXCLUIDAS and obj not in fijos and not es_tecnico(obj):
            yield obj


def textos_libres(obj, fijos):
    """§6.2: los textos citables, sin repetidos y ordenados alfabéticamente, para que ni el
    orden ni la forma dejen ver el brazo. Los vacíos o de puro espacio no cuentan."""
    return sorted({t for t in textos_citables(obj, fijos) if t.strip()})


def lista_de_textos(textos):
    """Una línea por texto: una etiqueta opaca y el texto como string JSON."""
    return "\n".join(f"t{n}: {json.dumps(t, ensure_ascii=False)}" for n, t in enumerate(textos, 1))


def mensaje(plantilla, llamada, alcance, textos):
    """§6.2: la llamada de seguimiento del pendiente, el alcance ampliado y la lista de textos.
    Iguales para el pendiente y su gemelo salvo los textos."""
    valores = {"{{FOLLOW_UP_CALL}}": llamada, "{{FOLLOW_UP_SCOPE}}": alcance, "{{TEXTS}}": lista_de_textos(textos)}
    texto = plantilla
    for marca, valor in valores.items():
        if texto.count(marca) != 1:
            raise SystemExit(f"El marcador {marca} aparece {texto.count(marca)} veces")
        texto = texto.replace(marca, valor)
    return texto


def leer_salida(texto):
    """§6.2: el último objeto de nivel superior con `records_missing_followup`. Devuelve
    (veredicto, cita) o None si no se lee: el veredicto tiene que ser un booleano, y la cita
    tiene que estar y ser un string, también con `false`."""
    hallado = extraccion.ultimo_objeto_con(texto or "", CLAVE)
    if hallado is None:
        return None
    obj = hallado[2]
    if "evidence_quote" not in obj:
        return None
    veredicto, cita = obj[CLAVE], obj["evidence_quote"]
    if not isinstance(veredicto, bool) or not isinstance(cita, str):
        return None
    return veredicto, cita


def _espacios(s):
    return " ".join(s.split())


def guarda(cita, textos):
    """§6.2: si el juez dice `true`, la cita, normalizando espacios, tiene que estar dentro de
    uno de los textos libres que recibió, tal como es o tal como lo vio el juez, escrito como
    string JSON: un salto de línea le llega como «\\n» (v20, hallazgo 2 de la cuarta
    revisión). Una cita vacía no pasa."""
    c = _espacios(cita)
    if not c:
        return False
    return any(c in _espacios(forma) for t in textos for forma in (t, json.dumps(t, ensure_ascii=False)[1:-1]))


def objetos_de_esquema(rutas):
    return [json.loads(p.read_bytes().decode("utf-8")) for p in rutas]
