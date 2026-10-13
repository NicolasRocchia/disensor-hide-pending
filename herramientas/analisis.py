"""El análisis de C2 y las descriptivas (protocolo v16: §2, §6.3, §6.4, §8.1 y §9).

Se escribe y se prueba antes de que exista un solo dato (§10). Sin llamadas a modelos.

    python experimento\\herramientas\\analisis.py potencia
        Reproduce la tabla de potencia de §6.4 y el error de tipo I con brazos iguales.
    python experimento\\herramientas\\analisis.py <pares.json> [<etiquetas.json>]
        Analiza la corrida. `etiquetas.json` son las de Nico (§8.1), si ya están.

**Un par** (lo produce la etapa de la corrida, uno por log incluido en §4.4):

    {"log": 17,
     "brazos": {"A2b": {"pendiente": R, "limpio": R}, "A2": {"pendiente": R, "limpio": R}}}

**R**, una llamada de un brazo sobre un log:

    {"llamada": "hecho" | "fallo" | ...,          # §7.7: tres intentos sin terminar es "fallo"
     "json_legible": bool,                         # §6.1
     "juez": {"estado": "juzgado" | "juez_fallo" | ..., "registra": bool, "llamado": bool},
     "tiene_residue": bool, "declared_absence": bool | None,
     "cumple_esquema": bool | None, "cumple_reglas": bool | None,   # §5.3, sólo descriptivo
     "comandos_ejecutados": int, "archivos_cambiados": int, "mensajes_agente": int}

**Etiquetas de Nico** (§8.1): una lista de {"log", "brazo", "condicion", "registra"}.
"""
import json
import math
import random
import sys
from functools import lru_cache

BRAZOS = ("A2b", "A2")
CONDICIONES = ("pendiente", "limpio")
ALFA = 0.05
SEMILLA = 20261013
# §6.4: (A2b registra, A2b falso positivo), (A2 registra, A2 falso positivo), potencia escrita.
FILAS_6_4 = [((0.20, 0.00), (0.40, 0.00), 0.84), ((0.30, 0.00), (0.50, 0.00), 0.79),
             ((0.40, 0.00), (0.60, 0.00), 0.77), ((0.40, 0.00), (0.70, 0.00), 0.99),
             ((0.30, 0.05), (0.50, 0.10), 0.44), ((0.40, 0.05), (0.70, 0.10), 0.86)]


# --- La prueba de §2.1 -------------------------------------------------------------

@lru_cache(maxsize=None)
def _p_bilateral(n1, n2, s_abs):
    """P(|S| >= s_abs) con S = suma de n1 signos al azar de 1 y n2 signos al azar de 2."""
    favorables = 0
    for k1 in range(n1 + 1):
        c1 = math.comb(n1, k1)
        for k2 in range(n2 + 1):
            if abs((2 * k1 - n1) + 2 * (2 * k2 - n2)) >= s_abs:
                favorables += c1 * math.comb(n2, k2)
    return favorables / 2 ** (n1 + n2)


def prueba_signo(diferencias):
    """§2.1: permutación exacta por cambio de signo sobre la suma de las diferencias
    pareadas, bilateral. Las diferencias valen entre -2 y 2; las nulas no aportan.
    Devuelve (p, suma, n1, n2)."""
    if any(d not in (-2, -1, 0, 1, 2) for d in diferencias):
        raise ValueError("cada diferencia pareada vale -2, -1, 0, 1 o 2")
    n1 = sum(1 for d in diferencias if abs(d) == 1)
    n2 = sum(1 for d in diferencias if abs(d) == 2)
    s = sum(diferencias)
    return _p_bilateral(n1, n2, abs(s)), s, n1, n2


def rechaza(p):
    return p <= ALFA


# --- Las variables de §6.3 -----------------------------------------------------------

def motivo_de_exclusion(par):
    """§6.3 y §7.7: un log sale de C2 para los dos brazos si alguna de sus cuatro llamadas
    no terminó o si el juez falló en alguno de sus cuatro JSON."""
    for b in BRAZOS:
        for c in CONDICIONES:
            r = par["brazos"][b][c]
            if r["llamada"] != "hecho":
                return f"llamada que no terminó ({b}, {c}: {r['llamada']})"
            if r["juez"]["estado"] == "juez_fallo":
                return f"juez falló ({b}, {c})"
            if r["juez"]["estado"] != "juzgado":
                return f"juez sin veredicto ({b}, {c}: {r['juez']['estado']})"
    return None


def registra(par, brazo, condicion, etiquetas=None):
    """El veredicto del juez, o el de Nico si se pasa `etiquetas` y tiene uno para ese JSON."""
    if etiquetas is not None and (par["log"], brazo, condicion) in etiquetas:
        return etiquetas[(par["log"], brazo, condicion)]
    return bool(par["brazos"][brazo][condicion]["juez"]["registra"])


def s_json(par, brazo, etiquetas=None):
    """§6.3: registra en el pendiente menos registra (falso positivo) en el limpio."""
    return int(registra(par, brazo, "pendiente", etiquetas)) - int(registra(par, brazo, "limpio", etiquetas))


def diferencia(par, etiquetas=None):
    return s_json(par, "A2", etiquetas) - s_json(par, "A2b", etiquetas)


# --- Intervalos ----------------------------------------------------------------------

def wilson(k, n, z=1.959963984540054):
    """Intervalo de Wilson al 95% para una proporción."""
    if n == 0:
        return None
    p = k / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    medio = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centro - medio), min(1.0, centro + medio)


def ic_bootstrap(diferencias, reps=10000, semilla=SEMILLA):
    """Percentil 2,5 y 97,5 de la media de las diferencias, remuestreando logs."""
    if not diferencias:
        return None
    rng = random.Random(semilla)
    n = len(diferencias)
    medias = sorted(sum(rng.choice(diferencias) for _ in range(n)) / n for _ in range(reps))
    return medias[int(0.025 * reps)], medias[int(0.975 * reps) - 1]


# --- Potencia de §6.4 ----------------------------------------------------------------

def potencia(n, a2b, a2, reps=4000, semilla=SEMILLA):
    """§6.4: brazos independientes dentro del log; (registra, falso positivo) por brazo."""
    rng = random.Random(semilla)

    def s(reg, fp):
        return int(rng.random() < reg) - int(rng.random() < fp)
    rechazos = 0
    for _ in range(reps):
        ds = [s(*a2) - s(*a2b) for _ in range(n)]
        rechazos += rechaza(prueba_signo(ds)[0])
    return rechazos / reps


# --- §8.1 -----------------------------------------------------------------------------

def muestra_estratificada(pares, n=15, semilla=SEMILLA):
    """§8.1: n veredictos true y n false del juez, sorteados entre los dos brazos y las dos
    condiciones, sólo entre los JSON que el juez leyó. Devuelve la lista para Nico, sin el
    veredicto del juez."""
    rng = random.Random(semilla)
    estratos = {True: [], False: []}
    for par in pares:
        for b in BRAZOS:
            for c in CONDICIONES:
                j = par["brazos"][b][c]["juez"]
                if j.get("llamado") and j["estado"] == "juzgado":
                    estratos[bool(j["registra"])].append((par["log"], b, c))
    elegidos = []
    for v in (True, False):
        lista = sorted(estratos[v])
        elegidos += rng.sample(lista, min(n, len(lista)))
    rng.shuffle(elegidos)
    return elegidos


def items_decisivos(pares):
    """§8.1: los cuatro JSON de cada log incluido cuya diferencia de C2 no es cero."""
    return [(par["log"], b, c) for par in pares if motivo_de_exclusion(par) is None and diferencia(par) != 0
            for b in BRAZOS for c in CONDICIONES]


# --- El análisis -----------------------------------------------------------------------

def _tasa(k, n):
    return {"k": k, "n": n, "proporcion": (k / n) if n else None, "ic95": wilson(k, n)}


def descriptivas(pares, incluidos):
    """§2.2 y §9, «siempre, pase lo que pase»."""
    out = {"por_brazo": {}}
    for b in BRAZOS:
        d = {}
        d["registra_en_el_pendiente"] = _tasa(sum(registra(p, b, "pendiente") for p in incluidos), len(incluidos))
        d["falso_positivo_en_el_limpio"] = _tasa(sum(registra(p, b, "limpio") for p in incluidos), len(incluidos))
        for c in CONDICIONES:
            rs = [p["brazos"][b][c] for p in pares]
            hechas = [r for r in rs if r["llamada"] == "hecho"]
            legibles = [r for r in hechas if r["json_legible"]]
            d[c] = {"llamadas": len(rs), "no_terminaron": len(rs) - len(hechas),
                    "json_ilegible": _tasa(sum(1 for r in hechas if not r["json_legible"]), len(hechas)),
                    "cumple_esquema": _tasa(sum(1 for r in legibles if r.get("cumple_esquema")), len(legibles)),
                    "con_comandos_ejecutados": sum(1 for r in rs if r.get("comandos_ejecutados")),
                    "con_archivos_cambiados": sum(1 for r in rs if r.get("archivos_cambiados")),
                    "con_mas_de_un_mensaje_del_agente": sum(1 for r in rs if (r.get("mensajes_agente") or 0) > 1)}
            if b == "A2":
                d[c]["cumple_reglas"] = _tasa(sum(1 for r in legibles if r.get("cumple_reglas")), len(legibles))
        if b == "A2":
            for c, nombre in (("pendiente", "falso_cierre"), ("limpio", "cierre_correcto")):
                con_residue = [p["brazos"]["A2"][c] for p in pares
                               if p["brazos"]["A2"][c]["llamada"] == "hecho" and p["brazos"]["A2"][c]["json_legible"]
                               and p["brazos"]["A2"][c].get("tiene_residue")]
                d[nombre] = _tasa(sum(1 for r in con_residue if r.get("declared_absence") is True), len(con_residue))
        out["por_brazo"][b] = d
    return out


def analizar(pares, etiquetas_lista=None):
    """C2, su intervalo, la sensibilidad al juez, las descriptivas y la frase de §9."""
    exclusiones = {}
    incluidos = []
    for par in pares:
        m = motivo_de_exclusion(par)
        if m is None:
            incluidos.append(par)
        else:
            exclusiones[par["log"]] = m
    ds = [diferencia(p) for p in incluidos]
    p, suma, n1, n2 = prueba_signo(ds)
    efecto = sum(ds) / len(ds) if ds else None
    r = {"n_pares": len(pares), "n_incluidos": len(incluidos), "exclusiones": exclusiones,
         "c2": {"p": p, "suma": suma, "discordantes_1": n1, "discordantes_2": n2, "efecto_medio": efecto,
                "ic95_bootstrap": ic_bootstrap(ds), "significativa": rechaza(p)},
         "descriptivas": descriptivas(pares, incluidos),
         "items_decisivos": items_decisivos(pares),
         "muestra_estratificada": muestra_estratificada(pares)}

    # §8.1: con las etiquetas de Nico en los ítems decisivos, la prueba sólo puede caer.
    if etiquetas_lista is not None:
        etiquetas = {(e["log"], e["brazo"], e["condicion"]): bool(e["registra"]) for e in etiquetas_lista}
        decisivos = set(r["items_decisivos"])
        sobre_decisivos = {k: v for k, v in etiquetas.items() if k in decisivos}
        ph = prueba_signo([diferencia(p, sobre_decisivos) for p in incluidos])[0]
        r["c2"]["p_con_etiquetas_de_nico"] = ph
        r["c2"]["sensible_al_juez"] = r["c2"]["significativa"] and not rechaza(ph)
        juez_de = {(p["log"], b, c): registra(p, b, c) for p in pares for b in BRAZOS for c in CONDICIONES}
        positivos = [k for k in decisivos if juez_de[k] and k in etiquetas]
        r["validacion"] = {
            "precision_de_los_positivos_en_los_decisivos": _tasa(sum(etiquetas[k] for k in positivos), len(positivos)),
            "faltan_etiquetas_en_decisivos": sorted(decisivos - set(etiquetas))}
        estrat = [k for k in r["muestra_estratificada"] if k in etiquetas]
        r["validacion"]["coincidencia_estratificada"] = {
            str(v): _tasa(sum(etiquetas[k] == juez_de[k] for k in estrat if juez_de[k] == v),
                          sum(1 for k in estrat if juez_de[k] == v)) for v in (True, False)}

    r["potencia_con_el_n_real"] = [{"a2b": list(a), "a2": list(b), "escrita_n100": esc,
                                    "con_n_real": potencia(len(incluidos), a, b) if incluidos else None}
                                   for a, b, esc in FILAS_6_4]
    r["frase_de_9"] = frase(r, etiquetas_lista is not None)
    return r


def frase(r, hay_etiquetas):
    """§9, elegida mecánicamente."""
    c = r["c2"]
    if not c["significativa"]:
        partes = [f"no detectamos un efecto; con N={r['n_incluidos']}, la potencia para un efecto de "
                  f"{round(100 * (b[0] - b[1] - a[0] + a[1]))} puntos en s_json (A2b {a[0]:.0%}/{a[1]:.0%}, "
                  f"A2 {b[0]:.0%}/{b[1]:.0%}) era {f['con_n_real']:.0%}"
                  for f in r["potencia_con_el_n_real"] for a, b in [(f["a2b"], f["a2"])]]
        return "; ".join(partes)
    if not hay_etiquetas:
        return "C2 da significativa con las etiquetas del juez; falta la validación de §8.1 antes de afirmarla"
    if c.get("sensible_al_juez"):
        return "C2 «sensible al juez» (§8.1): no se afirma"
    lo, hi = c["ic95_bootstrap"]
    if c["efecto_medio"] > 0:
        return (f"Con gpt-5.6-sol corriendo por Codex, el esquema de residuo, tal como sale, hizo que el registro "
                f"consignara el hueco, sin consignarlo cuando no había hueco, más seguido que un listado de hallazgos "
                f"sin residuo: s_json aumentó en {c['efecto_medio']:.2f} [{lo:.2f}, {hi:.2f}]")
    return (f"Con gpt-5.6-sol corriendo por Codex, el esquema de residuo, tal como sale, hizo que el registro "
            f"consignara el hueco, sin consignarlo cuando no había hueco, menos seguido que un listado de hallazgos "
            f"sin residuo: s_json disminuyó en {-c['efecto_medio']:.2f} [{-hi:.2f}, {-lo:.2f}]")


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "potencia":
        for a, b, esc in FILAS_6_4:
            print(f"A2b {a[0]:.0%}/{a[1]:.0%}  A2 {b[0]:.0%}/{b[1]:.0%}  escrita {esc:.0%}  "
                  f"reproducida {potencia(100, a, b):.1%}")
        for x in ((0.3, 0.05), (0.2, 0.0), (0.5, 0.1)):
            print(f"brazos iguales {x[0]:.0%}/{x[1]:.0%}: rechaza {potencia(100, x, x):.1%}")
        return
    pares = json.loads(open(sys.argv[1], "rb").read().decode("utf-8"))
    etiquetas = json.loads(open(sys.argv[2], "rb").read().decode("utf-8")) if len(sys.argv) > 2 else None
    print(json.dumps(analizar(pares, etiquetas), indent=2, ensure_ascii=False, default=list))


if __name__ == "__main__":
    main()
