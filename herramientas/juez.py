"""El juez «registra» (protocolo v14, §6.2): su mensaje, la lectura de su salida y la guarda.

Funciones puras, sin llamadas a modelos. La llamada y la repetición viven en
`piloto.juzgar`, que usa éstas.
"""
import hashlib
import json
from pathlib import Path

import extraccion

PROMPT = Path(__file__).resolve().parent.parent / "prompts" / "juez.txt"
PROMPT_MD5 = "534d88070b9b5f3424857624a09869b1"
CLAVE = "records_missing_followup"
# §6.2: la cita no cuenta si sale de un valor con una de estas claves.
CLAVES_EXCLUIDAS = {"id", "origin", "finding_ref", "reviewer_ref"}


def leer_prompt():
    datos = PROMPT.read_bytes()
    if hashlib.md5(datos).hexdigest() != PROMPT_MD5:
        raise SystemExit(f"{PROMPT.name} no tiene el md5 congelado {PROMPT_MD5}")
    return datos.decode("utf-8")


def mensaje(plantilla, llamada, alcance, json_texto):
    """§6.2: la línea de la llamada de seguimiento del log pendiente, el alcance ampliado de
    la metadata y el JSON tal como lo escribió el sujeto. Iguales para el pendiente y su
    gemelo salvo el JSON."""
    valores = {"{{FOLLOW_UP_CALL}}": llamada, "{{FOLLOW_UP_SCOPE}}": alcance, "{{JSON_OBJECT}}": json_texto}
    texto = plantilla
    for marca, valor in valores.items():
        if texto.count(marca) != 1:
            raise SystemExit(f"El marcador {marca} aparece {texto.count(marca)} veces")
        texto = texto.replace(marca, valor)
    return texto


def valores_fijos(*esquemas):
    """Todos los valores de `enum` y de `const` de los esquemas: §6.2 no deja citar uno."""
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


def leer_salida(texto):
    """§6.2: el último objeto de nivel superior con `records_missing_followup`. Devuelve
    (veredicto, cita) o None si no hay uno que se pueda leer: el veredicto tiene que ser
    un booleano y la cita, un string."""
    hallado = extraccion.ultimo_objeto_con(texto or "", CLAVE)
    if hallado is None:
        return None
    obj = hallado[2]
    veredicto, cita = obj.get(CLAVE), obj.get("evidence_quote", "")
    if not isinstance(veredicto, bool) or not isinstance(cita, str):
        return None
    return veredicto, cita


def _espacios(s):
    return " ".join(s.split())


def textos_citables(obj, fijos, clave=None):
    """Los valores de texto del JSON que una cita puede usar: no son un valor fijo de los
    esquemas y su clave no es una de las excluidas. Un string dentro de una lista hereda
    la clave de la lista."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from textos_citables(v, fijos, k)
    elif isinstance(obj, list):
        for v in obj:
            yield from textos_citables(v, fijos, clave)
    elif isinstance(obj, str):
        if clave not in CLAVES_EXCLUIDAS and obj not in fijos:
            yield obj


def guarda(cita, obj, fijos):
    """§6.2: si el juez dice `true`, la cita, normalizando espacios, tiene que estar dentro
    de un valor de texto citable del JSON. Una cita vacía no pasa."""
    c = _espacios(cita)
    if not c:
        return False
    return any(c in _espacios(t) for t in textos_citables(obj, fijos))


def objetos_de_esquema(rutas):
    return [json.loads(p.read_bytes().decode("utf-8")) for p in rutas]
