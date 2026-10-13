"""Sacar el JSON y la prosa de una respuesta del sujeto (protocolo v11, §6.1).

Funciones puras, sin llamadas a modelos. La prueba de humo sólo usa si se
encontró el JSON; nadie lee las respuestas a los brazos antes de congelar.
"""
import json
import re

RE_CERCO = re.compile(r"^\s*```")


def ultimo_objeto_con(texto, clave):
    """§6.1, regla 1: el último objeto de nivel superior que parsea y tiene `clave`.

    Intenta `raw_decode` desde cada «{», que respeta las llaves dentro de strings; un
    objeto que parsea se saltea entero, así que sólo cuentan los de nivel superior. Un
    arreglo que parsea desde un «[» también se saltea entero: un objeto adentro de un
    arreglo no es de nivel superior (v19, hallazgo 12). Devuelve (inicio, fin, objeto) o
    None. La usan la extracción y el juez (§6.2).
    """
    dec = json.JSONDecoder()
    elegido = None
    i = 0
    while i < len(texto):
        if texto[i] == "[":
            try:
                valor, fin = dec.raw_decode(texto, i)
            except json.JSONDecodeError:
                i += 1
                continue
            i = fin if isinstance(valor, list) else i + 1
            continue
        if texto[i] == "{":
            try:
                obj, fin = dec.raw_decode(texto, i)
            except json.JSONDecodeError:
                i += 1
                continue
            if isinstance(obj, dict) and clave in obj:
                elegido = (i, fin, obj)
            i = fin
            continue
        i += 1
    return elegido


def extraer(texto):
    """§6.1: el último objeto de nivel superior con la clave `findings`.

    Devuelve {"json", "json_texto", "ilegible", "en_cerco", "prosa"}. `json_texto` es el
    objeto tal como lo escribió el sujeto, que es lo que recibe el juez. `json` es None si
    ningún objeto con `findings` parsea; entonces la respuesta es «JSON ilegible» y la
    prosa se corta en el último cerco de código o en la última línea que empieza con «{»,
    lo que aparezca primero.
    """
    elegido = ultimo_objeto_con(texto, "findings")
    if elegido is None:
        lineas = texto.split("\n")
        cercos = [k for k, l in enumerate(lineas) if RE_CERCO.match(l)]
        # «El último cerco de código» es la línea que abre el último bloque: con un número
        # par de cercos, el anteúltimo; con uno impar, el bloque quedó abierto y es el último.
        apertura = (cercos[-2] if len(cercos) % 2 == 0 else cercos[-1]) if cercos else None
        llaves = [k for k, l in enumerate(lineas) if l.startswith("{")]
        candidatos = ([apertura] if apertura is not None else []) + ([llaves[-1]] if llaves else [])
        prosa = "\n".join(lineas[:min(candidatos)]) if candidatos else texto
        return {"json": None, "json_texto": None, "ilegible": True, "en_cerco": False,
                "prosa": _sin_presentacion(prosa)}
    inicio, fin, obj = elegido
    json_texto = texto[inicio:fin]
    antes, despues = texto[:inicio], texto[fin:]
    en_cerco = False
    # Regla 2: si el objeto está dentro de un cerco, se saca también el cerco.
    m_antes = re.search(r"```[A-Za-z]*[ \t]*\n?[ \t]*$", antes)
    m_despues = re.match(r"\s*```", despues)
    if m_antes and m_despues:
        antes, despues = antes[:m_antes.start()], despues[m_despues.end():]
        en_cerco = True
    prosa = (antes.rstrip() + ("\n" + despues.strip() if despues.strip() else "")).strip("\n")
    return {"json": obj, "json_texto": json_texto, "ilegible": False, "en_cerco": en_cerco,
            "prosa": _sin_presentacion(prosa)}


def _sin_presentacion(prosa):
    """Regla 5: si la última línea no vacía termina en «:» y dice «JSON», se saca."""
    lineas = prosa.rstrip().split("\n")
    if lineas and lineas[-1].rstrip().endswith(":") and "json" in lineas[-1].lower():
        lineas = lineas[:-1]
    return "\n".join(lineas).rstrip()
