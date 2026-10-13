#!/usr/bin/env python3
"""Deshace los cortes de línea que mete la maqueta del PDF en un prompt de juez
que está escrito como objeto JSON.

Dentro de un string JSON no puede haber un salto de línea real, así que todo
salto que caiga adentro de un string es un corte de la maqueta y se deshace.
Afuera de los strings, los saltos son espacio en blanco de JSON y se dejan.

La única decisión es con qué se une: con un espacio, o con nada. El recuadro del
PDF corta en un espacio siempre que puede; sólo corta en medio de un token cuando
el renglón entero no tiene espacios. Entonces se une SIN espacio solamente si el
renglón anterior no tiene ningún espacio y además llegó al ancho del recuadro, o
viene detrás de otro renglón así. En cualquier otro caso, con un espacio.

Cinco pruebas, y si alguna falla el script aborta sin escribir nada:
  1. Sacando todo el espacio en blanco, salida y entrada son idénticas.
  2. La salida parsea como JSON.
  3. Los marcadores {{...}} del prompt_template son exactamente las claves de
     "inputs", una vez cada uno.
  4. Cada descripción de la rúbrica aparece textual dentro del prompt_template.
     Las dos copias están cortadas en lugares distintos del PDF, así que si
     coinciden, las uniones con espacio de esos pasajes están bien.
  5. Ninguna línea vacía: el recuadro del PDF no tiene ninguna.

Uso:
    python3 -I reflow_json.py ENTRADA SALIDA_JSON SALIDA_PROMPT --ancho 79
"""
import json
import re
import sys


def comillas_sin_escapar(s):
    n, i = 0, 0
    while i < len(s):
        if s[i] == '"':
            barras, j = 0, i - 1
            while j >= 0 and s[j] == "\\":
                barras += 1
                j -= 1
            if barras % 2 == 0:
                n += 1
        i += 1
    return n


def main():
    args = sys.argv[1:]
    ancho = int(args[args.index("--ancho") + 1])
    entrada, sal_json, sal_prompt = [a for a in args if not a.startswith("--") and a != str(ancho)]

    crudas = open(entrada, encoding="utf-8").read().split("\n")[1:]  # sin el título de sección
    vacias = sum(1 for l in crudas if not l.strip())
    fisicas = [l.strip() for l in crudas if l.strip()]

    salida, uniones = [], []
    abierto = False          # ¿la línea acumulada termina adentro de un string?
    corrida_sin_espacio = False
    for l in fisicas:
        if salida and abierto:
            previa = ultimo_fisico
            sin_esp = " " not in previa
            pegado = sin_esp and (len(previa) == ancho or corrida_sin_espacio)
            sep = "" if pegado else " "
            uniones.append((previa, l, sep))
            salida[-1] = salida[-1] + sep + l
            corrida_sin_espacio = pegado and " " not in l
        else:
            salida.append(l)
            corrida_sin_espacio = False
        ultimo_fisico = l
        if " " not in l and len(l) == ancho:
            corrida_sin_espacio = True
        abierto = comillas_sin_escapar(salida[-1]) % 2 == 1

    texto = "\n".join(salida) + "\n"
    original = "\n".join(crudas)

    # 1
    if re.sub(r"\s", "", texto) != re.sub(r"\s", "", original):
        sys.exit("FALLA prueba 1: cambió un caracter que no es espacio")
    # 2
    try:
        obj = json.loads(texto)
    except json.JSONDecodeError as e:
        sys.exit(f"FALLA prueba 2: no parsea: {e}")
    # 3
    plantilla = obj["prompt_template"]
    marcadores = re.findall(r"\{\{([^}]*)\}\}", plantilla)
    esperados = list(obj["inputs"].keys())
    if sorted(marcadores) != sorted(esperados) or len(set(marcadores)) != len(marcadores):
        sys.exit(f"FALLA prueba 3: marcadores {marcadores} contra inputs {esperados}")
    # 4
    for r in obj["rubric"]:
        if r["description"] not in plantilla:
            sys.exit(f"FALLA prueba 4: la rúbrica {r['score']} no aparece textual en la plantilla")
    # 5
    if any(not l.strip() for l in texto.strip().split("\n")):
        sys.exit("FALLA prueba 5: quedó una línea vacía")

    open(sal_json, "w", encoding="utf-8").write(texto)
    open(sal_prompt, "w", encoding="utf-8").write(plantilla)

    sin = [(p, l) for p, l, s in uniones if s == ""]
    print(f"ok  {len(fisicas)} renglones físicos -> {len(salida)} líneas JSON  (vacías quitadas: {vacias})")
    print(f"    prueba 1 caracteres idénticos: sí")
    print(f"    prueba 2 JSON parsea: sí")
    print(f"    prueba 3 marcadores = inputs: {marcadores}")
    print(f"    prueba 4 las {len(obj['rubric'])} rúbricas aparecen textuales en la plantilla: sí")
    print(f"    prueba 5 sin líneas vacías: sí")
    print(f"    uniones: {len(uniones)}, de ellas SIN espacio: {len(sin)}")
    for p, l in sin:
        print(f"      «{p[-40:]}» + «{l[:40]}»")
    print(f"    plantilla decodificada: {len(plantilla)} caracteres, {plantilla.count(chr(10))} saltos de línea")


if __name__ == "__main__":
    main()
