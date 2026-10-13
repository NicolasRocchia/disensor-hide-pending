"""El prompt generador Q.1.8 y el sorteo de sus ocho marcadores (protocolo v5, §4.1).

El prompt se usa sin cambiarle una palabra: sólo se reemplazan los ocho
marcadores, cada uno una vez, por un elemento de la lista de ejemplos que el
propio prompt trae debajo. Los dos chequeos de distracción son dos elementos
distintos, unidos por ", ". Cada elemento va textual, sin el guion de la lista.
"""
import hashlib
import random
from pathlib import Path

EXPERIMENTO = Path(__file__).resolve().parent.parent
PROMPT = EXPERIMENTO / "Q.1.8-generador-REFLOW.md"
PROMPT_MD5 = "c63429e5f9d71049b08a4fcb6c93f7fe"

MARCADORES = [
    ("DOMAIN", "**Domain:**", 9),
    ("PRIMARY_SURFACE", "**Primary Surface:**", 8),
    ("INITIAL_QUESTION", "**Initial Question:**", 5),
    ("INITIAL_QUERY_SCOPE", "**Initial Query Scope:**", 6),
    ("FOLLOW_UP_SCOPE_EXPANSION", "**Follow-up Scope Expansion:**", 7),
    ("MISSING_FOLLOW_UP_BEHAVIOR", "**Missing Follow-up Behavior:**", 5),
    ("DISTRACTION_CHECKS", "**Distraction Checks:**", 7),
    ("FINAL_QUESTION_PATTERN", "**Final Question Pattern:**", 5),
]


def leer_prompt():
    datos = PROMPT.read_bytes()
    if hashlib.md5(datos).hexdigest() != PROMPT_MD5:
        raise SystemExit(f"{PROMPT.name} no tiene el md5 congelado {PROMPT_MD5}")
    return datos.decode("utf-8")


def listas(prompt):
    """Las listas de ejemplos de cada marcador, leídas del propio prompt."""
    lineas = prompt.split("\n")
    salida = {}
    for nombre, rotulo, esperado in MARCADORES:
        i = next(k for k, l in enumerate(lineas) if l.startswith(rotulo))
        assert lineas[i].strip().endswith("`{" + nombre + "}`"), lineas[i]
        items = []
        j = i + 1
        while j < len(lineas) and not lineas[j].startswith("**") and not lineas[j].startswith("## "):
            l = lineas[j]
            if l.startswith("Examples: "):
                items = [x.strip() for x in l[len("Examples: "):].rstrip(".").split(", ")]
            elif l.startswith("- ") and any(lineas[k].startswith("Examples:") for k in range(i + 1, j)):
                items.append(l[2:].strip())
            j += 1
        if len(items) != esperado:
            raise SystemExit(f"{nombre}: se esperaban {esperado} ejemplos, hay {len(items)}: {items}")
        salida[nombre] = items
    return salida


def sortear(semilla, n, estratificar_falla):
    """Sorteo reproducible. El orden de las llamadas al generador de azar es parte del protocolo:
    primero, si se estratifica, la secuencia de fallas barajada; después, por cada log, los
    marcadores en el orden de MARCADORES, y los dos chequeos de distracción con rng.sample."""
    rng = random.Random(semilla)
    fallas = None
    if estratificar_falla:
        fallas = [f for f in range(5) for _ in range(n // 5)]
        assert len(fallas) == n
        rng.shuffle(fallas)
    sorteo = []
    for k in range(n):
        d = {}
        for nombre, _, tam in MARCADORES:
            if nombre == "DISTRACTION_CHECKS":
                d[nombre] = rng.sample(range(tam), 2)
            elif nombre == "MISSING_FOLLOW_UP_BEHAVIOR" and fallas is not None:
                d[nombre] = fallas[k]
            else:
                d[nombre] = rng.randrange(tam)
        sorteo.append(d)
    return sorteo


def llenar(prompt, ejemplos, sorteado):
    texto = prompt
    for nombre, _, _ in MARCADORES:
        if nombre == "DISTRACTION_CHECKS":
            valor = ", ".join(ejemplos[nombre][i] for i in sorteado[nombre])
        else:
            valor = ejemplos[nombre][sorteado[nombre]]
        marca = "{" + nombre + "}"
        if texto.count(marca) != 1:
            raise SystemExit(f"El marcador {marca} aparece {texto.count(marca)} veces")
        texto = texto.replace(marca, valor)
    return texto
