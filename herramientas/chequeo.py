"""Chequeos mecánicos del log pendiente (protocolo v9, §4.1 y §4.2).

Funciones puras, sin llamadas a modelos, para que `prueba_offline.py` las pruebe.
La etapa `chequear` de `piloto.py` las aplica a lo que dejó el generador.
"""
import hashlib
import json
import re

# Encabezado de cada entrada del log: «[09:14:11] TOOL CALL», solo en su línea.
RE_ENCABEZADO = re.compile(r"^\[(\d{1,2}:\d{2}(?::\d{2})?)\] ([A-Z][A-Z ]*[A-Z])\s*$")

# §4.2.3: una línea «nombre: número». El generador escribe también «nombre — número»,
# y cuenta igual. El número es la cifra entera, con o sin separador de miles, seguida
# de un espacio, una coma, un % o el fin de línea, así que fechas («2026-10-12») y
# horas («09:14:12») no cuentan.
RE_NOMBRE_NUMERO = re.compile(r"^\s*[^\s=:][^=:]*?\s*(?::|\s[—–-])\s*\d+(?:,\d{3})*(?:\.\d+)?(?=\s|$|%|,)")

# Una línea de categoría o de entidad del primer resultado, con su valor:
# «NodeUnavailable: 2,468», «TimeoutError — 2,184 failed jobs, ...».
RE_CON_VALOR = re.compile(
    r"^(?P<sangria>\s*)(?P<nombre>[^\s=:][^=:]*?)\s*(?::|\s[—–-])\s*(?P<numero>\d+(?:,\d{3})*(?:\.\d+)?)(?=\s|$|%|,)")
# Una categoría sola en su línea, como en la plantilla del prompt («TimeoutError»).
RE_SOLA = re.compile(r"^(?P<sangria>\s*)(?P<nombre>[^\s=:][^=:]*?)\s*$")

COMILLAS = str.maketrans({"‘": "'", "’": "'", "‚": "'", "‛": "'",
                          "“": '"', "”": '"', "„": '"', "‟": '"'})


def canonica(datos):
    """§4.1, forma canónica: UTF-8, sin BOM, finales de línea LF. Devuelve (texto, tenía_bom)."""
    texto = datos.decode("utf-8")
    bom = texto.startswith("﻿")
    if bom:
        texto = texto[1:]
    return texto.replace("\r\n", "\n").replace("\r", "\n"), bom


def md5_texto(texto):
    return hashlib.md5(texto.encode("utf-8")).hexdigest()


def normalizar(texto):
    """§4.2.2: comillas curvas a rectas y todo el espacio en blanco a un espacio."""
    return " ".join(texto.translate(COMILLAS).split())


def claves_de_la_metadata(prompt):
    """Las claves que pide el generador, leídas del bloque ```json del propio prompt."""
    i = prompt.index("```json")
    inicio = prompt.index("{", i)
    obj, _ = json.JSONDecoder().raw_decode(prompt, inicio)
    return list(obj)


def entradas(log):
    """El log partido en entradas: [(hora, tipo, [líneas del cuerpo])]. Lo que haya antes
    del primer encabezado queda en una entrada de tipo None."""
    salida = [(None, None, [])]
    for linea in log.split("\n"):
        m = RE_ENCABEZADO.match(linea)
        if m:
            salida.append((m.group(1), m.group(2), []))
        else:
            salida[-1][2].append(linea)
    if not salida[0][2] or not any(l.strip() for l in salida[0][2]):
        salida.pop(0)
    return salida


def lineas_nombre_numero(cuerpo):
    return [l for l in cuerpo if RE_NOMBRE_NUMERO.match(l)]


def _numero(s):
    return float(s.replace(",", ""))


RE_ROTULO = re.compile(r"^(?P<sangria>\s*)(?P<nombre>[^\s=:][^=:]*?)\s*:\s*$")
RE_CLAVE_VALOR = re.compile(r"^\s*(?P<clave>[A-Za-z_][\w.]*)=(?P<valor>.+?)\s*$")
RE_MARCA_DE_LISTA = re.compile(r"^(?:\d+[.)]|[-*•])\s+")
RE_SOLO_NUMERO = re.compile(r"^\d+(?:,\d{3})*(?:\.\d+)?(?:\s.*)?$")


def _sin_marca(nombre):
    return RE_MARCA_DE_LISTA.sub("", nombre.strip())


def dominante(cuerpo, niveles=None):
    """§4.2.3: la categoría dominante del primer resultado, con dos formas.

    **Árbol por sangría.** Cuentan las líneas con valor («nombre: n» o «nombre — n»), las
    categorías solas en su línea y los rótulos (una línea que termina en «:» sin valor),
    que cortan el árbol pero no son categorías. Una categoría es una línea con al menos
    un hijo con valor; su total es su propio número o, si no tiene, la suma de sus hijos
    directos. Se elige la de mayor total en el nivel de arriba, y dentro de ella la de
    mayor total, y así: la `cadena` queda registrada, pero el chequeo usa sólo el primer
    nombre, la categoría dominante, porque los niveles de abajo pueden ser entidades que
    aparecen legítimamente en otros resultados.

    **Bloques clave=valor** («component=X», «failures=2,214», y el desglose debajo),
    separados por líneas en blanco, cuando el árbol no encuentra categorías. Gana el
    bloque de mayor total (su primer valor numérico o la suma de su desglose), y sus
    nombres son todos sus valores que no son números («component», «error_type»…).

    Con `niveles`, la cadena se corta en ese largo: sirve para comparar el bloque nuevo de un
    gemelo «al mismo nivel» que el primer resultado (§4.4.4), aunque el bloque nuevo agregue
    un subnivel debajo de las entidades.

    Devuelve {"forma", "nombres", "cadena", "entidad"}; `nombres` vacío si no hay
    categorías.
    """
    nodos = []  # (sangría, nombre, valor o None, bloque, es_rótulo)
    bloque = 0
    for linea in cuerpo:
        if not linea.strip():
            bloque += 1
            continue
        m = RE_CON_VALOR.match(linea)
        if m:
            nodos.append((len(m.group("sangria")), _sin_marca(m.group("nombre")), _numero(m.group("numero")), bloque, False))
            continue
        m = RE_ROTULO.match(linea)
        if m:
            nodos.append((len(m.group("sangria")), _sin_marca(m.group("nombre")), None, bloque, True))
            continue
        m = RE_SOLA.match(linea)
        if m:
            nodos.append((len(m.group("sangria")), _sin_marca(m.group("nombre")), None, bloque, False))

    def hijos(i):
        sangria, _, valor, blq, _ = nodos[i]
        # Lo que cuelga con más sangría; los hijos directos son los de sangría mínima.
        colgados = []
        for j in range(i + 1, len(nodos)):
            if nodos[j][0] <= sangria:
                break
            colgados.append(j)
        if colgados:
            minima = min(nodos[j][0] for j in colgados)
            return [j for j in colgados if nodos[j][0] == minima]
        if valor is None:
            # Categoría sola en su línea con las entidades a la misma sangría, como en la
            # plantilla del prompt: sus hijos son las líneas con valor que siguen en el
            # mismo bloque, hasta la próxima categoría sola.
            planos = []
            for j in range(i + 1, len(nodos)):
                s, _, v, b, _ = nodos[j]
                if s != sangria or b != blq or v is None:
                    break
                planos.append(j)
            return planos
        return []

    def es_categoria(i):
        return not nodos[i][4] and any(nodos[j][2] is not None for j in hijos(i))

    def total(i):
        if nodos[i][2] is not None:
            return nodos[i][2]
        return sum(nodos[j][2] or 0 for j in hijos(i))

    candidatas = [i for i in range(len(nodos)) if es_categoria(i)]
    if candidatas:
        arriba = min(nodos[i][0] for i in candidatas)
        nivel = [i for i in candidatas if nodos[i][0] == arriba]
        cadena = []
        while nivel:
            elegida = max(nivel, key=total)
            cadena.append(nodos[elegida][1])
            if niveles is not None and len(cadena) >= niveles:
                break
            nivel = [j for j in hijos(elegida) if es_categoria(j)]
        # La entidad que más tiene, entre los hijos con valor de la última categoría.
        con_valor = [j for j in hijos(elegida) if nodos[j][2] is not None]
        entidad = nodos[max(con_valor, key=lambda j: nodos[j][2])][1] if con_valor else None
        return {"forma": "arbol", "nombres": cadena[:1], "cadena": cadena, "entidad": entidad}

    # Bloques clave=valor separados por líneas en blanco.
    bloques, actual = [], []
    for linea in cuerpo + [""]:
        if linea.strip():
            actual.append(linea)
        elif actual:
            bloques.append(actual)
            actual = []
    mejor = None
    for blq in bloques:
        pares = [m.groups() for m in (RE_CLAVE_VALOR.match(l) for l in blq) if m]
        desglose = [l for l in blq if RE_CON_VALOR.match(l)]
        nombres = [v for _, v in pares if not RE_SOLO_NUMERO.match(v)]
        if not desglose or not nombres:
            continue
        numericos = [_numero(v.split()[0]) for _, v in pares if RE_SOLO_NUMERO.match(v)]
        tot = numericos[0] if numericos else sum(_numero(RE_CON_VALOR.match(l).group("numero")) for l in desglose)
        if mejor is None or tot > mejor[0]:
            arriba = max(desglose, key=lambda l: _numero(RE_CON_VALOR.match(l).group("numero")))
            mejor = (tot, nombres, _sin_marca(RE_CON_VALOR.match(arriba).group("nombre")))
    if mejor:
        return {"forma": "clave_valor", "nombres": mejor[1], "cadena": mejor[1], "entidad": mejor[2]}
    return {"forma": None, "nombres": [], "cadena": [], "entidad": None}


def hojas(cuerpo):
    """Las líneas con valor que no tienen nada colgado con más sangría: [(nombre, valor, sangría)]."""
    filas = []
    for linea in cuerpo:
        if not linea.strip():
            continue
        m = RE_CON_VALOR.match(linea)
        sangria = len(linea) - len(linea.lstrip())
        filas.append((sangria, _sin_marca(m.group("nombre")), _numero(m.group("numero"))) if m else (sangria, None, None))
    out = []
    for i, (s, nombre, valor) in enumerate(filas):
        if nombre is None:
            continue
        siguiente = next((f for f in filas[i + 1:]), None)
        if siguiente is None or siguiente[0] <= s:
            out.append((nombre, valor, s))
    return out


def nombra(cuerpo, nombre):
    """El nombre aparece como palabra entera, sin distinguir mayúsculas."""
    return re.search(r"(?<![\w-])" + re.escape(nombre) + r"(?![\w-])", "\n".join(cuerpo), re.I) is not None


def chequear(log, metadata_texto, claves):
    """§4.2 sobre un log en forma canónica. Devuelve el detalle y la lista de fallas."""
    det = {"fallas": []}
    # 1. Metadata que parsea, con las claves que pide el generador.
    try:
        meta = json.loads(metadata_texto)
    except json.JSONDecodeError as e:
        det["fallas"].append(f"1: la metadata no parsea ({e.msg})")
        meta = None
    if meta is not None:
        if not isinstance(meta, dict):
            det["fallas"].append("1: la metadata no es un objeto")
            meta = None
        else:
            faltan = [c for c in claves if c not in meta]
            det["claves_extra"] = sorted(set(meta) - set(claves))
            if faltan:
                det["fallas"].append("1: faltan claves: " + ", ".join(faltan))
    # 2. El log termina en la pregunta final de la metadata.
    if meta is not None and isinstance(meta.get("final_question"), str):
        det["termina_en_la_pregunta"] = normalizar(log).endswith(normalizar(meta["final_question"]))
        if not det["termina_en_la_pregunta"]:
            det["fallas"].append("2: el log no termina en la final_question")
    elif meta is not None:
        det["fallas"].append("2: no hay final_question")
    # 3. La trampa existe.
    ents = entradas(log)
    det["tipos"] = [t for _, t, _ in ents]
    llamadas = [i for i, (_, t, _) in enumerate(ents) if t == "TOOL CALL"]
    resultados = [i for i, (_, t, _) in enumerate(ents) if t == "TOOL RESULT"]
    if len(llamadas) < 2:
        det["fallas"].append("3: no hay segunda TOOL CALL")
        return det
    seguimiento = llamadas[1]
    det["llamada_de_seguimiento"] = next((l for l in ents[seguimiento][2] if l.strip()), "")
    if seguimiento + 1 >= len(ents):
        det["fallas"].append("3: no hay entrada después de la consulta de seguimiento")
        return det
    _, tipo_sig, cuerpo_sig = ents[seguimiento + 1]
    det["entrada_siguiente"] = {"tipo": tipo_sig, "lineas": [l for l in cuerpo_sig if l.strip()]}
    numeros_sig = lineas_nombre_numero(cuerpo_sig)
    if numeros_sig:
        det["fallas"].append("3: la entrada después del seguimiento tiene números por entidad: " + " | ".join(numeros_sig))
    primero = [i for i in resultados if i < seguimiento]
    if not primero:
        det["fallas"].append("3: no hay TOOL RESULT antes del seguimiento")
        return det
    dom = dominante(ents[primero[0]][2])
    det["dominante"] = dom
    if not dom["nombres"]:
        det["fallas"].append("3: no se encontró una categoría dominante en el primer resultado")
        return det
    for i in resultados:
        if i <= seguimiento + 1:
            continue
        cuerpo = ents[i][2]
        nombrados = [n for n in dom["nombres"] if nombra(cuerpo, n)]
        nums = lineas_nombre_numero(cuerpo)
        if nombrados and nums:
            det["fallas"].append(f"3: un TOOL RESULT posterior ({ents[i][0]}) nombra {nombrados} con números por entidad")
    return det


def diferencias_con_el_sorteo(valores, meta):
    """§4.1: qué campos de la metadata no coinciden con lo sorteado, comparando normalizado."""
    pares = {"DOMAIN": "domain", "PRIMARY_SURFACE": "primary_surface",
             "INITIAL_QUESTION": "initial_question", "INITIAL_QUERY_SCOPE": "initial_query_scope",
             "FOLLOW_UP_SCOPE_EXPANSION": "follow_up_scope_expansion",
             "MISSING_FOLLOW_UP_BEHAVIOR": "missing_follow_up_behavior",
             "DISTRACTION_CHECKS": "distraction_checks", "FINAL_QUESTION_PATTERN": "final_question"}
    out = {}
    for marcador, clave in pares.items():
        sorteado = valores.get(marcador)
        dado = meta.get(clave) if isinstance(meta, dict) else None
        if isinstance(sorteado, list):
            igual = isinstance(dado, list) and sorted(map(normalizar, sorteado)) == sorted(normalizar(str(d)) for d in dado)
        else:
            igual = isinstance(dado, str) and normalizar(sorteado.strip("“”\"")) == normalizar(dado)
        if not igual:
            out[clave] = {"sorteado": sorteado, "metadata": dado}
    return out
