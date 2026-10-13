"""El análisis de C2 y las descriptivas (protocolo v19: §2, §6.3, §6.4, §8.1 y §9).

Se escribe y se prueba antes de que exista un solo dato (§10). Sin llamadas a modelos.

    python experimento\\herramientas\\analisis.py potencia
        Reproduce la tabla de potencia de §6.4, el error de tipo I con brazos iguales y la
        grilla de potencia con correlaciones (v19).
    python experimento\\herramientas\\analisis.py <pares.json> [<etiquetas.json>]
        Analiza la corrida. `etiquetas.json` son las de Nico (§8.1), si ya están.

**Un par** (lo produce `corrida.py`, uno por log incluido en §4.4):

    {"log": 17, "partido": false, "gemelo_con_request_id": true,
     "brazos": {"A2b": {"pendiente": R, "limpio": R}, "A2": {"pendiente": R, "limpio": R}}}

`partido` dice si las cuatro llamadas del par no corrieron en la misma sesión (un corte
por cupo en el medio); `gemelo_con_request_id`, si el gemelo conserva en el bloque nuevo la
línea `request_id=…` aceptada por regla (§4.4).

**R**, una llamada de un brazo sobre un log:

    {"llamada": "hecho" | "fallo" | ...,          # §7.7: tres intentos sin terminar es "fallo"
     "json_legible": bool,                         # §6.1
     "juez": {"estado": "juzgado" | "juez_fallo" | ..., "registra": bool, "llamado": bool},
     "tiene_residue": bool, "declared_absence": bool | None,
     "cumple_esquema": bool | None, "cumple_reglas": bool | None,   # §5.3, sólo descriptivo
     "comandos_ejecutados": int, "archivos_cambiados": int, "mensajes_agente": int}

**Etiquetas de Nico** (§8.1): una lista de {"log", "brazo", "condicion", "registra"}, con
`registra` un booleano JSON de verdad.
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
# §8.1 (v19): si en un estrato de la muestra (los true o los false del juez) con al menos
# MINIMO_ESTRATO etiquetas Nico coincide con el juez menos que UMBRAL_COINCIDENCIA, C2 no
# se afirma: el instrumento no es confiable.
UMBRAL_COINCIDENCIA = 0.80
MINIMO_ESTRATO = 10
# §6.4: (A2b registra, A2b falso positivo), (A2 registra, A2 falso positivo), potencia escrita.
FILAS_6_4 = [((0.20, 0.00), (0.40, 0.00), 0.84), ((0.30, 0.00), (0.50, 0.00), 0.79),
             ((0.40, 0.00), (0.60, 0.00), 0.77), ((0.40, 0.00), (0.70, 0.00), 0.99),
             ((0.30, 0.05), (0.50, 0.10), 0.44), ((0.40, 0.05), (0.70, 0.10), 0.86)]
CORRELACIONES = (0.0, 0.3, 0.6)


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
    pareadas, bilateral. Exacta bajo la hipótesis nula de que, dentro de cada log, las
    etiquetas A2 y A2b son intercambiables (el esquema no cambia la distribución del
    resultado), que hace simétrica a cada diferencia. Las diferencias valen entre -2 y 2;
    las nulas no aportan. Devuelve (p, suma, n1, n2)."""
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
    no terminó o si el juez no dio un veredicto en alguno de sus cuatro JSON."""
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


def validar_etiquetas(lista):
    """§8.1 (v19, hallazgos 2 y 13): cada etiqueta con log, brazo y condición válidos, sin
    repetidos, y `registra` un booleano JSON de verdad (la cadena «false» no es false)."""
    out = {}
    for e in lista:
        if not isinstance(e, dict) or set(e) != {"log", "brazo", "condicion", "registra"}:
            raise ValueError(f"etiqueta mal formada: {e!r}")
        if e["brazo"] not in BRAZOS or e["condicion"] not in CONDICIONES:
            raise ValueError(f"etiqueta con brazo o condición inválidos: {e!r}")
        if not isinstance(e["registra"], bool):
            raise ValueError(f"etiqueta con registra que no es un booleano: {e!r}")
        clave = (e["log"], e["brazo"], e["condicion"])
        if clave in out:
            raise ValueError(f"etiqueta repetida: {clave}")
        out[clave] = e["registra"]
    return out


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
    """§9: percentil 2,5 y 97,5 de la media de las diferencias, remuestreando logs."""
    if not diferencias:
        return None
    rng = random.Random(semilla)
    n = len(diferencias)
    medias = sorted(sum(rng.choice(diferencias) for _ in range(n)) / n for _ in range(reps))
    return medias[int(0.025 * reps)], medias[int(0.975 * reps) - 1]


# --- Potencia de §6.4 ----------------------------------------------------------------

def potencia(n, a2b, a2, reps=4000, semilla=SEMILLA, rho_brazos=0.0, rho_condiciones=0.0):
    """§6.4: (registra, falso positivo) por brazo. Con las dos correlaciones en cero, las
    cuatro observaciones de un log son independientes, que es el supuesto de la tabla. Con
    `rho_brazos`, los dos brazos comparten el sorteo de cada condición con esa probabilidad;
    con `rho_condiciones`, dentro de un brazo el pendiente y el limpio comparten su sorteo
    con esa probabilidad (v19, hallazgo 8)."""
    rng = random.Random(semilla)
    rechazos = 0
    if rho_brazos == 0 and rho_condiciones == 0:
        # El camino de la tabla: el mismo flujo aleatorio que dio los números de §6.4.
        def s(reg, fp):
            return int(rng.random() < reg) - int(rng.random() < fp)
        for _ in range(reps):
            rechazos += rechaza(prueba_signo([s(*a2) - s(*a2b) for _ in range(n)])[0])
        return rechazos / reps
    for _ in range(reps):
        ds = []
        for _ in range(n):
            u_pend_comun, u_limp_comun = rng.random(), rng.random()
            s = {}
            for b, (reg, fp) in (("A2b", a2b), ("A2", a2)):
                up = u_pend_comun if rng.random() < rho_brazos else rng.random()
                ul = up if rng.random() < rho_condiciones else (u_limp_comun if rng.random() < rho_brazos else rng.random())
                s[b] = int(up < reg) - int(ul < fp)
            ds.append(s["A2"] - s["A2b"])
        rechazos += rechaza(prueba_signo(ds)[0])
    return rechazos / reps


# --- §8.1 -----------------------------------------------------------------------------

def muestra_estratificada(pares, n=15, semilla=SEMILLA):
    """§8.1: n veredictos true y n false del juez, sorteados entre los dos brazos y las dos
    condiciones, sólo entre los JSON que el juez leyó. Si un estrato tiene menos de n, van
    todos los que hay. Devuelve la lista para Nico, sin el veredicto del juez."""
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
        # v19, hallazgo 6: los falsos positivos, según el gemelo conserve o no el request_id.
        for con in (True, False):
            sub = [p for p in incluidos if bool(p.get("gemelo_con_request_id")) == con]
            d[f"falso_positivo_gemelo_{'con' if con else 'sin'}_request_id"] = _tasa(
                sum(registra(p, b, "limpio") for p in sub), len(sub))
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


def _prueba(incluidos, etiquetas=None):
    ds = [diferencia(p, etiquetas) for p in incluidos]
    p, suma, n1, n2 = prueba_signo(ds)
    return {"p": p, "suma": suma, "discordantes_1": n1, "discordantes_2": n2,
            "efecto_medio": (sum(ds) / len(ds)) if ds else None, "significativa": rechaza(p), "_ds": ds}


def analizar(pares, etiquetas_lista=None):
    """C2, su intervalo, la validación de §8.1, las descriptivas y la frase de §9."""
    etiquetas = validar_etiquetas(etiquetas_lista) if etiquetas_lista is not None else None
    exclusiones, incluidos = {}, []
    for par in pares:
        m = motivo_de_exclusion(par)
        if m is None:
            incluidos.append(par)
        else:
            exclusiones[par["log"]] = m
    r = {"n_pares": len(pares), "n_incluidos": len(incluidos), "exclusiones": exclusiones}
    if not incluidos:
        r["c2"] = {"evaluable": False, "significativa": False}
        r["frase_de_9"] = "C2 no evaluable: ningún par quedó incluido (§6.3); se informan las exclusiones"
        r["descriptivas"] = descriptivas(pares, incluidos)
        return r
    c2 = _prueba(incluidos)
    ds = c2.pop("_ds")
    c2.update(evaluable=True, ic95_bootstrap=ic_bootstrap(ds))
    r["c2"] = c2
    r["descriptivas"] = descriptivas(pares, incluidos)
    r["items_decisivos"] = items_decisivos(pares)
    r["muestra_estratificada"] = muestra_estratificada(pares)

    # v19, hallazgo 11: la misma prueba sin los pares partidos, como sensibilidad.
    enteros = [p for p in incluidos if not p.get("partido")]
    if len(enteros) < len(incluidos):
        s = _prueba(enteros)
        s.pop("_ds")
        r["sensibilidad_sin_pares_partidos"] = {"n": len(enteros), **s}

    if etiquetas is not None:
        # §8.1 (v19): las etiquetas de Nico reemplazan al juez en todo lo que etiquetó. Pueden
        # quitar la afirmación (si la prueba deja de dar o cambia de signo), nunca crearla.
        h = _prueba(incluidos, etiquetas)
        h.pop("_ds")
        r["c2_con_etiquetas_de_nico"] = h
        cambia = (not h["significativa"]) or (math.copysign(1, h["suma"]) != math.copysign(1, c2["suma"]))
        r["c2"]["sensible_al_juez"] = c2["significativa"] and cambia
        juez_de = {(p["log"], b, c): registra(p, b, c) for p in pares for b in BRAZOS for c in CONDICIONES}
        decisivos = set(r["items_decisivos"])
        positivos = [k for k in decisivos if juez_de[k] and k in etiquetas]
        estrat = [k for k in r["muestra_estratificada"] if k in etiquetas]
        coincidencia = {}
        for v in (True, False):
            en = [k for k in estrat if juez_de[k] == v]
            t = _tasa(sum(etiquetas[k] == juez_de[k] for k in en), len(en))
            t["suficiente"] = len(en) >= MINIMO_ESTRATO
            coincidencia[str(v)] = t
        no_confiable = any(t["suficiente"] and t["proporcion"] < UMBRAL_COINCIDENCIA for t in coincidencia.values())
        r["validacion"] = {"precision_de_los_positivos_en_los_decisivos": _tasa(sum(etiquetas[k] for k in positivos),
                                                                                len(positivos)),
                           "faltan_etiquetas_en_decisivos": sorted(decisivos - set(etiquetas)),
                           "coincidencia_estratificada": coincidencia, "juez_no_confiable": no_confiable}

    r["potencia_con_el_n_real"] = [{"a2b": list(a), "a2": list(b), "escrita_n100": esc,
                                    "con_n_real": potencia(len(incluidos), a, b)} for a, b, esc in FILAS_6_4]
    r["frase_de_9"] = frase(r, etiquetas is not None)
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
    if r["validacion"]["juez_no_confiable"]:
        return (f"C2 no se afirma: en la muestra estratificada, Nico coincide con el juez menos de "
                f"{UMBRAL_COINCIDENCIA:.0%} en algún estrato (§8.1)")
    if c.get("sensible_al_juez"):
        return "C2 «sensible al juez» (§8.1): no se afirma"
    lo, hi = c["ic95_bootstrap"]
    comun = ("Con gpt-5.6-sol corriendo por Codex, el esquema de residuo, tal como sale, hizo que el registro "
             "consignara el hueco, sin consignarlo cuando no había hueco, ")
    if c["efecto_medio"] > 0:
        return comun + f"más seguido que un listado de hallazgos sin residuo: s_json aumentó en {c['efecto_medio']:.2f} [{lo:.2f}, {hi:.2f}]"
    return comun + f"menos seguido que un listado de hallazgos sin residuo: s_json disminuyó en {-c['efecto_medio']:.2f} [{-hi:.2f}, {-lo:.2f}]"


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "potencia":
        for a, b, esc in FILAS_6_4:
            print(f"A2b {a[0]:.0%}/{a[1]:.0%}  A2 {b[0]:.0%}/{b[1]:.0%}  escrita {esc:.0%}  "
                  f"reproducida {potencia(100, a, b):.1%}")
        for x in ((0.3, 0.05), (0.2, 0.0), (0.5, 0.1)):
            print(f"brazos iguales {x[0]:.0%}/{x[1]:.0%}: rechaza {potencia(100, x, x):.1%}")
        print("grilla con correlaciones (rho entre brazos, rho entre pendiente y limpio):")
        for a, b, _ in FILAS_6_4:
            celdas = [f"{rb:.1f}/{rc:.1f}: {potencia(100, a, b, reps=1000, rho_brazos=rb, rho_condiciones=rc):.0%}"
                      for rb in CORRELACIONES for rc in CORRELACIONES]
            print(f"  A2b {a[0]:.0%}/{a[1]:.0%}  A2 {b[0]:.0%}/{b[1]:.0%}  " + "  ".join(celdas))
        for rb in CORRELACIONES:
            print(f"  brazos iguales 30%/5%, rho brazos {rb:.1f}: rechaza "
                  f"{potencia(100, (0.3, 0.05), (0.3, 0.05), reps=1000, rho_brazos=rb, rho_condiciones=0.3):.1%}")
        return
    pares = json.loads(open(sys.argv[1], "rb").read().decode("utf-8"))
    etiquetas = json.loads(open(sys.argv[2], "rb").read().decode("utf-8")) if len(sys.argv) > 2 else None
    print(json.dumps(analizar(pares, etiquetas), indent=2, ensure_ascii=False, default=list))


if __name__ == "__main__":
    main()
