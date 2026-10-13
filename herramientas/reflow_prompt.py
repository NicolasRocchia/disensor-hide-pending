#!/usr/bin/env python3
"""Deshace los cortes de línea que mete la maqueta del PDF en un prompt extraído.

Une una línea a la anterior SOLO cuando la anterior quedó cortada a mitad de
oración y la actual no abre un elemento estructural. Nunca toca un caracter del
contenido: lo único que cambia son saltos de línea por espacios, y espacios al
borde de cada línea.

Tres pruebas, y si alguna falla el script aborta sin escribir nada:
  1. Colapsando todo el espacio en blanco, salida y entrada son idénticas.
  2. La cantidad de líneas estructurales es la misma antes y después.
  3. El bloque ```json, si existe, parsea como JSON válido.

Uso:
    python3 -I reflow_prompt.py ENTRADA SALIDA [--saltear-primera-linea] [--sin-lineas-vacias]

--sin-lineas-vacias: para prompts cuyo recuadro en el PDF no tiene ninguna línea
en blanco. Las que aparecen en la extracción son cortes de página, donde se
sacaron el número de página y el encabezado corrido.
"""
import json
import re
import sys

# Una línea que arranca así abre un elemento propio: nunca se pega a la anterior.
ESTRUCTURAL = [
    r"^#{1,6} ",                      # encabezado
    r"^- ",                           # viñeta
    r"^\d+\. ",                       # ítem numerado
    r"^> ",                           # cita
    r"^\[\d\d:\d\d:\d\d\] ",          # línea del log de plantilla
    r"^<",                            # marcador de plantilla
    r"^\{$", r"^\}$", r"^```",        # JSON y cercos de código
    r'^"[a-z_]+":',                   # clave JSON
    r"^\*\*[A-Z][^*]*:\*\*",          # rótulo en negrita, **Domain:**
    r"^\*\*File \d",                  # rótulo **File 1 ...**
    r"^[\w-]+: [\d,]+$",              # muestra de datos, worker: 181
    r"^[\w_]+=",                      # muestra de evento, status=accepted
    r"^Examples:",                    # cabecera de lista de ejemplos
    r"^Follow exactly:",
]
# Después de una línea así, lo que sigue va en línea nueva.
CIERRA_SIEMPRE = [
    r"^#{1,6} ",
    r"^\[\d\d:\d\d:\d\d\] ",
    r"^\*\*[A-Z][^*]*:\*\*",
    r"^\*\*File \d",
]
ESTRUCT_RE = [re.compile(p) for p in ESTRUCTURAL]
CIERRA_RE = [re.compile(p) for p in CIERRA_SIEMPRE]


def es_estructural(linea):
    return any(r.search(linea) for r in ESTRUCT_RE)


def termina_unidad(linea):
    if any(r.search(linea) for r in CIERRA_RE):
        return True
    s = linea.rstrip()
    # se pelan cierres que no deciden: comillas, negrita, código, paréntesis
    while s and s[-1] in "\"”’'`)*":
        s = s[:-1]
    return s.endswith((".", "?", "!", ":"))


def reflow(lineas):
    """Decide cada unión mirando el último fragmento físico, no la línea ya
    unida, para que una oración partida en tres renglones se una entera."""
    salida, uniones = [], []
    ultimo = ""
    for crudo in lineas:
        l = crudo.strip()
        if not l:
            if salida and salida[-1] != "":
                salida.append("")
            ultimo = ""
            continue
        if salida and salida[-1] != "" and not es_estructural(l) and not termina_unidad(ultimo):
            uniones.append((ultimo, l))
            salida[-1] = salida[-1] + " " + l
        else:
            salida.append(l)
        ultimo = l
    return "\n".join(salida).strip() + "\n", uniones


def colapsar(t):
    return re.sub(r"\s+", " ", t).strip()


def contar_estructurales(texto):
    return sum(1 for l in texto.split("\n") if es_estructural(l.strip()))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    saltear = "--saltear-primera-linea" in sys.argv
    sin_vacias = "--sin-lineas-vacias" in sys.argv
    entrada, salida_path = args
    lineas = open(entrada, encoding="utf-8").read().split("\n")
    if saltear:
        lineas = lineas[1:]
    if sin_vacias:
        quitadas = sum(1 for l in lineas if not l.strip())
        lineas = [l for l in lineas if l.strip()]
        print(f"    líneas vacías quitadas: {quitadas}")
    original = "\n".join(lineas)

    texto, uniones = reflow(lineas)

    # Prueba 1: ningún caracter de contenido cambió
    if colapsar(texto) != colapsar(original):
        a, b = colapsar(texto), colapsar(original)
        i = next(i for i in range(min(len(a), len(b))) if a[i] != b[i])
        sys.exit(f"FALLA prueba 1 en {i}: {a[i-40:i+40]!r} vs {b[i-40:i+40]!r}")
    # Prueba 2: ninguna línea estructural se tragó a otra
    ce, cs = contar_estructurales(original), contar_estructurales(texto)
    if ce != cs:
        sys.exit(f"FALLA prueba 2: {ce} estructurales en la entrada, {cs} en la salida")
    # Prueba 3: el bloque JSON parsea
    m = re.search(r"```json\n(.*?)(?:\n```|\Z)", texto, re.S)
    json_ok = None
    if m:
        try:
            json.loads(m.group(1))
            json_ok = True
        except json.JSONDecodeError as e:
            sys.exit(f"FALLA prueba 3: el bloque JSON no parsea: {e}")

    open(salida_path, "w", encoding="utf-8").write(texto)
    print(f"ok  {len(original.splitlines())} líneas -> {len(texto.splitlines())}")
    print(f"    prueba 1 contenido idéntico: sí")
    print(f"    prueba 2 estructurales: {ce} = {cs}")
    print(f"    prueba 3 JSON: {'parsea' if json_ok else 'no hay bloque'}")
    print(f"    uniones: {len(uniones)}")
    for p, l in uniones:
        print(f"      «{p[-38:]}» + «{l[:38]}»")


if __name__ == "__main__":
    main()
