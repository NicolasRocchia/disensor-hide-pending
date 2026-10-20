"""El piloto de la fase 3 (fase3/00-PILOTO.md), por etapas.

**No es la corrida:** no se congela, y sus salidas se pueden leer. Semilla 20261020, salidas en
`fase3/piloto/`, los binarios fijados de la fase 1. Importa los módulos de las fases 1 y 2 sin
modificarlos. Cada etapa es reanudable, y corre sólo con `fase3/herramientas/` y
`fase3/prompts/` commiteados (§8). Toda etapa que llama a un modelo pide el OK de Nico.

    python experimento\\fase3\\herramientas\\piloto3.py <etapa> [--limite N]

Sin llamadas:
  consigna           Arma prompts/revisor.txt desde la salida de disensor 0.14.0 (§4.2).
  regla              La regla de #134 sobre los logs del piloto y los gemelos (§5.2).
  hoja-revisores     Las copias ciegas de los informes, para clasificarlos (§4.4).
  resumen-1          Las tasas de la etapa 1 y la regla de §6.1, con las etiquetas.
  hoja-verificacion  Las copias ciegas de los residuos finales que abren (§5.3).
  resumen-2          Lo mecánico de la etapa 2 y las reglas de §6.2.
Con llamadas, cada una con el OK de Nico:
  antes              Paso 0: A2 sobre los 40 logs del piloto sin gemelo (GPT, esfuerzo low).
  revisores          Etapa 1: RS (GPT, high) y RD (Claude, high) sobre los 50 pendientes y los
                     10 gemelos, por log, en un orden sorteado. `--limite` cuenta logs.
  verificacion       Etapa 2: R0, RS, RD y RR (GPT, low), sólo si la etapa 1 pasó su regla
                     (§6.1). `--sigue` cuando Nico decidió seguir con un revisor que no revisa.
"""
import argparse
import contextlib
import hashlib
import json
import random
import sys
from pathlib import Path

F3 = Path(__file__).resolve().parent.parent
EXP = F3.parent
sys.path.insert(0, str(EXP / "herramientas"))
sys.path.insert(0, str(EXP / "fase2" / "herramientas"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import analisis  # noqa: E402
import arnes  # noqa: E402
import corrida  # noqa: E402
import extraccion  # noqa: E402
import piloto  # noqa: E402
import corrida2  # noqa: E402
import mensajes3  # noqa: E402

DIR = F3 / "piloto"
DIR_ANTES_FASE2 = EXP / "fase2" / "piloto" / "brazos"
RUTAS_ARBOL = ("fase3/herramientas", "fase3/prompts")
SEMILLA = 20261020
# §2: los 50 logs del piloto de la fase 1; diez con gemelo y la A2 del piloto de la fase 2.
LOGS = tuple(range(50))
LOGS_CON_GEMELO = corrida2.LOGS_DEL_PILOTO
LOGS_SIN_GEMELO = tuple(k for k in LOGS if k not in LOGS_CON_GEMELO)
REVISORES = ("RS", "RD")
BRAZOS = ("R0", "RS", "RD", "RR")
ESFUERZO_REVISOR_GPT = "high"
TERMINALES_REVISION = ("hecho", "fallo", "fallo_verificacion", "interrumpido")
TERMINALES_VERIFICACION = ("hecho", "fallo", "interrumpido", "sin_informe", "sin_llamada")
# §8: las plantillas que fija cada etapa.
PLANTILLAS_DE = {"revisores": ("revisor",), "verificacion": ("verificacion", "revision-vacia", "regla-134")}
# §4.4: dónde dice el informe lo que dice.
DONDE = ("hallazgo", "hipotesis", "hueco", "veredicto", "ninguno")
# §5.3, descriptiva: cómo nombra el residuo final al seguimiento.
DICE = ("pendiente", "no_establecido", "otro", "no_lo_nombra")

escribir = corrida.escribir
leer = corrida.leer
leer_o_nada = corrida.leer_o_nada


def condiciones(k):
    return ("pendiente", "limpio") if k in LOGS_CON_GEMELO else ("pendiente",)


# --- §8: lo que corre está commiteado -----------------------------------------------------------

def head():
    return corrida.git_ok("rev-parse", "HEAD").strip()


def arbol(ref="HEAD"):
    """El md5 del código y los prompts de la fase 3 en `ref`."""
    return hashlib.md5(corrida.git_ok("ls-tree", "-r", ref, "--", *RUTAS_ARBOL).encode("utf-8")).hexdigest()


def exigir_arbol_limpio():
    sucio = corrida.git_ok("status", "--porcelain", "--", *RUTAS_ARBOL).strip()
    if sucio:
        sys.exit("Hay cambios sin commitear en fase3/herramientas o fase3/prompts: lo que corre tiene que estar "
                 f"commiteado (§8).\n{sucio}")


def plan_de_etapa(base, nombre, items):
    """§8: el orden y las plantillas de una etapa quedan fijos desde su primera corrida. Si
    cambian, la etapa se repite entera en otra carpeta y se informan las dos."""
    f = base / f"plan-{nombre}.json"
    md5 = {n: v for n, v in mensajes3.md5_de_las_plantillas().items() if n in PLANTILLAS_DE.get(nombre, ())}
    items = [list(x) for x in items]
    if f.exists():
        p = leer(f)
        if p["plantillas_md5"] != md5:
            sys.exit(f"Las plantillas de `{nombre}` cambiaron desde que empezó la etapa ({f}): la etapa se repite "
                     "entera, en otra carpeta, y se informan las dos (§8).")
        if p["items"] != items:
            sys.exit(f"El orden de `{nombre}` no es el que quedó fijo en {f}. El arnés para.")
        return p
    p = {"etapa": nombre, "creado": arnes.ahora(), "semilla": SEMILLA, "commit": head(), "arbol": arbol(),
         "plantillas_md5": md5, "items": items}
    escribir(f, p)
    return p


# --- §2: el «antes» ------------------------------------------------------------------------------

def dir_antes(base, k, c):
    if k in LOGS_CON_GEMELO:
        return DIR_ANTES_FASE2 / f"{k:03d}-A2-{c}"
    return base / "brazos" / f"{k:03d}-A2-{c}"


def antes(base, k, c):
    """La A2 del «antes», con su prosa y su JSON verificados por md5, o None si no terminó."""
    d = dir_antes(base, k, c)
    r = leer_o_nada(d / "resumen.json")
    if r.get("estado") != "hecho":
        return None
    prosa_b = (d / "prosa.txt").read_bytes()
    if arnes.md5_bytes(prosa_b) != r.get("prosa_md5"):
        sys.exit(f"{d / 'prosa.txt'} no coincide con su md5. El arnés para.")
    json_texto, obj = None, None
    if r.get("json_md5"):
        json_b = (d / "json.txt").read_bytes()
        if arnes.md5_bytes(json_b) != r["json_md5"]:
            sys.exit(f"{d / 'json.txt'} no coincide con su md5. El arnés para.")
        json_texto = json_b.decode("utf-8")
        try:
            obj = json.loads(json_texto)
        except ValueError:
            obj = None
    return {"dir": str(d), "prosa": prosa_b.decode("utf-8"), "prosa_md5": r["prosa_md5"], "json_texto": json_texto,
            "json_md5": r.get("json_md5"), "obj": obj, "declaracion": mensajes3.declaracion(obj)}


def es_falso_cierre(base, k):
    """§6: un pendiente cuyo «antes» declara ausencia."""
    a = antes(base, k, "pendiente")
    return a is not None and a["declaracion"] == "cierra"


def fuente():
    return corrida2.FuentePiloto(LOGS)


def rid_seguimiento(f, k):
    """El `request_id` de la llamada de seguimiento, sacado siempre del log pendiente: 2 de los
    10 gemelos del piloto (001 y 008) no lo conservan en su TOOL RESULT."""
    return mensajes3.seguimiento(f.texto(k, "pendiente"))["request_id"]


# --- El esfuerzo del revisor GPT (§3) ------------------------------------------------------------

@contextlib.contextmanager
def esfuerzo_gpt(valor):
    """§3: el comando de `arnes.comando_codex_exec` con `model_reasoning_effort=<valor>`, sin
    tocar `arnes.py`. Vale también para los reintentos y el canario que corren adentro."""
    previo = arnes.ESFUERZO_GPT
    arnes.ESFUERZO_GPT = valor
    try:
        yield
    finally:
        arnes.ESFUERZO_GPT = previo


# --- El canario, como en la fase 2, con los mensajes de la fase 3 -----------------------------------

_PARRAFO_INFORME_CANARIO = (
    "1. Share stated without its base. Severity: minor. Where: the second sentence of the answer. What fails: "
    "the answer gives a share of the total without saying which total it is taken from, so a reader cannot "
    "check it against the counts listed in the log. How the receiver can verify it: compare the share with the "
    "totals in the log, line by line, and recompute it from the rows that are shown there.")
# Un informe fijo largo para el canario de la verificación, del lado de arriba de los reales.
INFORME_CANARIO = ("**Findings.**\n\n" + "\n\n".join([_PARRAFO_INFORME_CANARIO] * 10)
                   + "\n\n**Unverified hypotheses.**\n\n- None.\n\n**Execution gaps.**\n\n- None.\n\n"
                   "**Verdict.** One minor finding, repeated for length; nothing blocking.")


def mensaje_canario(familia):
    """El pedido del canario: `revisor` (RS y RD) o `verificacion` (R0, RS, RD y RR), sobre el
    gemelo del log 003 del piloto con el marcador fijo de la fase 2 y la prosa larga fija."""
    plantillas = mensajes3.leer_plantillas()
    k = corrida2.LOG_DEL_CANARIO
    log = corrida2.FuentePiloto((k,)).texto(k, "limpio").rstrip("\n") + corrida2.MARCA_CANARIO
    if familia == "revisor":
        return mensajes3.mensaje_revisor(plantillas, log, corrida2.PROSA_CANARIO).encode("utf-8")
    return mensajes3.mensaje_verificacion(plantillas, log, corrida2.PROSA_CANARIO, INFORME_CANARIO,
                                          piloto.leer_esquemas()["A2"]).encode("utf-8")


def canario(fijado, cual, base, familia):
    """`corrida2.canario` con los mensajes de la fase 3."""
    carpeta = base / "canarios"
    carpeta.mkdir(parents=True, exist_ok=True)
    prefijo = base_prefijo = f"{familia}-{cual}-{''.join(ch for ch in arnes.ahora() if ch.isdigit())}"
    n = 1
    while any(carpeta.glob(f"{prefijo}*")):
        n += 1
        prefijo = f"{base_prefijo}-{n}"
    try:
        m = mensaje_canario(familia)
        if cual == "claude":
            reg, texto = piloto.una_llamada_claude(fijado, m, carpeta, prefijo)
        else:
            reg, texto = piloto.una_llamada_gpt(fijado, m, carpeta, prefijo, tipo="canario")
    except Exception as exc:  # noqa: BLE001 - un canario que revienta es un servicio que no contesta
        escribir(carpeta / f"{prefijo}.json", {"excepcion": repr(exc)})
        return False
    escribir(carpeta / f"{prefijo}.json", reg)
    if reg.get("red_de_seguridad"):
        corrida2.cortar(base, "PARADA", f"canario {prefijo}", lambda: None)
    return bool(reg.get("termino")) and reg.get("verificado", True) is not False and bool((texto or "").strip())


def revisar_intento(fijado, cual, base, intentos, guardar, familia):
    """`corrida2.revisar_intento` con el canario de la fase 3: después de un intento que no
    terminó, sin sesión o con el canario caído, la falla no es del ítem y la etapa para."""
    ult = intentos[-1] if intentos else None
    if (not ult or ult.get("en_vuelo") or ult.get("termino") or ult.get("sin_cupo") or ult.get("red_de_seguridad")
            or ult.get("sin_sesion") or ult.get("caida")):
        return
    if not corrida2.con_sesion(fijado, cual):
        motivo = "sin_sesion"
    elif not canario(fijado, cual, base, familia):
        motivo = "caida"
    else:
        return
    ult[motivo] = True
    if cual == "claude":
        ult["etiqueta"] = f"{ult.get('etiqueta')}-{motivo.replace('_', '-')}"
    else:
        ult["sin_cupo"] = True
    guardar()
    caidas = sum(1 for i in intentos if i.get("caida"))
    if motivo == "caida" and caidas >= corrida2.CAIDAS_POR_ITEM:
        base.mkdir(parents=True, exist_ok=True)
        (base / "PARADA").write_bytes(f"{caidas} caídas del servicio en un mismo ítem\n".encode("utf-8"))
        sys.exit(f"{caidas} caídas del servicio de {cual} en un mismo ítem: el arnés para (PARADA) hasta que Nico "
                 "lo revise.")
    if motivo == "sin_sesion":
        login = "auth login" if cual == "claude" else "login"
        sys.exit(f"El CLI de {cual} del arnés no tiene una sesión iniciada. Nico: `{fijado[f'{cual}_exe']} {login}` "
                 "y volver a correr la etapa, que es reanudable.")
    sys.exit(f"El servicio de {cual} no contesta: tampoco terminó un canario ({base / 'canarios'}). Es reanudable: "
             "volvé a correr la etapa más tarde.")


# --- Paso 0: las A2 de los 40 logs sin gemelo -----------------------------------------------------

def etapa_antes(args, base=None):
    base = base or DIR
    corrida2.sin_parada(base)
    exigir_arbol_limpio()
    plan = [(k, "A2", "pendiente") for k in LOGS_SIN_GEMELO]
    faltan = [x for x in plan if leer_o_nada(base / "brazos" / "{:03d}-{}-{}".format(*x) / "resumen.json")
              .get("estado") not in corrida.TERMINALES_BRAZO]
    if not faltan:
        print("antes: las 40 A2 ya terminaron")
        return
    fijado = arnes.verificar_binarios(corrida.BINARIOS, ("codex",))
    esquemas = piloto.leer_esquemas()
    objetos = {b: json.loads(t) for b, t in esquemas.items()}
    sello = {"commit_del_registro": None, "sesiones": arnes.ahora(), "arboles": arbol(), "commits": head(),
             "jsonschema": corrida2.exigir_jsonschema()}
    f = fuente()
    for n, (k, b, c) in enumerate(faltan):
        if args.limite is not None and n >= args.limite:
            break
        r = corrida2.correr_brazo(base, fijado, f, k, b, c, esquemas, objetos, sello)
        print(f"{k:03d} A2 pendiente {r['estado']} ausencia={r.get('declared_absence')}", flush=True)
    quedan = sum(1 for x in plan if leer_o_nada(base / "brazos" / "{:03d}-{}-{}".format(*x) / "resumen.json")
                 .get("estado") not in corrida.TERMINALES_BRAZO)
    print("antes: listo para `revisores`" if not quedan else f"antes: faltan {quedan} A2")


# --- Etapa 1: los revisores -----------------------------------------------------------------------

def plan_revisores(base):
    """§4.3: por log, las llamadas de RS y RD sobre el pendiente y el gemelo, seguidas, en un
    orden sorteado. Sólo los ítems cuyo «antes» terminó."""
    rng = random.Random(SEMILLA)
    logs = list(LOGS)
    rng.shuffle(logs)
    plan = []
    for k in logs:
        llamadas = [(rev, c) for rev in REVISORES for c in condiciones(k) if antes(base, k, c) is not None]
        rng.shuffle(llamadas)
        plan += [(k, rev, c) for rev, c in llamadas]
    return plan


def exigir_antes_completo(base):
    for k in LOGS_SIN_GEMELO:
        if leer_o_nada(base / "brazos" / f"{k:03d}-A2-pendiente" / "resumen.json").get("estado") \
                not in corrida.TERMINALES_BRAZO:
            sys.exit(f"Falta la A2 del log {k:03d}: terminar `antes`.")


def correr_revision(base, fijado, plantillas, f, k, rev, c, sello):
    """Una revisión, reanudable. Guarda el informe y la marca mecánica del `request_id`."""
    carpeta = base / "revisiones" / f"{k:03d}-{rev}-{c}"
    fr = carpeta / "resumen.json"
    r = leer(fr) if fr.exists() else {"log": k, "revisor": rev, "condicion": c, "intentos": []}
    if r.get("estado") in TERMINALES_REVISION:
        return r
    for clave, valor in sello.items():
        r.setdefault(clave, []).append(valor)
    a = antes(base, k, c)
    log = f.texto(k, c)
    m = mensajes3.mensaje_revisor(plantillas, log, a["prosa"]).encode("utf-8")
    r.update(mensaje_md5=arnes.md5_bytes(m), prosa_antes_md5=a["prosa_md5"], antes=a["dir"])
    carpeta.mkdir(parents=True, exist_ok=True)
    cual = "codex" if rev == "RS" else "claude"

    def guardar():
        escribir(fr, r)
        revisar_intento(fijado, cual, base, r["intentos"], lambda: escribir(fr, r), "revisor")
    if rev == "RS":
        with esfuerzo_gpt(ESFUERZO_REVISOR_GPT):
            estado, _, texto = corrida.gpt_con_reintentos(fijado, m, carpeta, r["intentos"], "revisor RS", guardar)
    else:
        estado, texto = piloto.claude_con_reintentos(fijado, m, carpeta, r["intentos"], "revisor", guardar)
    if estado in ("PARADA", "sin_cupo"):
        corrida2.cortar(base, estado, f"{k:03d} {rev} {c}", lambda: escribir(fr, r))
    r["estado"] = estado
    if estado == "hecho":
        informe_b = texto.encode("utf-8")
        (carpeta / "informe.txt").write_bytes(informe_b)
        rid = rid_seguimiento(f, k)
        r.update(informe_md5=arnes.md5_bytes(informe_b), informe_chars=len(texto), informe_vacio=not texto.strip(),
                 request_id_seguimiento=rid, request_id_en_la_entrada=rid in log,
                 marca_request_id=mensajes3.nombra_request_id(texto, rid))
    escribir(fr, r)
    return r


def informe(base, k, rev, c):
    """El informe terminado de una revisión, verificado por su md5, o None."""
    d = base / "revisiones" / f"{k:03d}-{rev}-{c}"
    r = leer_o_nada(d / "resumen.json")
    if r.get("estado") != "hecho":
        return None
    datos = (d / "informe.txt").read_bytes()
    if arnes.md5_bytes(datos) != r["informe_md5"]:
        sys.exit(f"{d / 'informe.txt'} no coincide con su md5. El arnés para.")
    return datos.decode("utf-8")


def faltan(base, carpeta, plan, terminales):
    return [x for x in plan if leer_o_nada(base / carpeta / "{:03d}-{}-{}".format(*x) / "resumen.json")
            .get("estado") not in terminales]


def etapa_revisores(args, base=None):
    base = base or DIR
    corrida2.sin_parada(base)
    exigir_arbol_limpio()
    exigir_antes_completo(base)
    plantillas = mensajes3.leer_plantillas()
    plan = [tuple(x) for x in plan_de_etapa(base, "revisores", plan_revisores(base))["items"]]
    pendientes = faltan(base, "revisiones", plan, TERMINALES_REVISION)
    if not pendientes:
        print("revisores: los informes ya terminaron; sigue `hoja-revisores`")
        return
    fijado = arnes.verificar_binarios(corrida.BINARIOS, tuple(sorted({"codex" if rev == "RS" else "claude"
                                                                     for _, rev, _ in pendientes})))
    sello = {"sesiones": arnes.ahora(), "arboles": arbol(), "commits": head()}
    f = fuente()
    logs_hechos = []
    for k, rev, c in pendientes:
        if k not in logs_hechos:
            if args.limite is not None and len(logs_hechos) >= args.limite:
                break
            logs_hechos.append(k)
        r = correr_revision(base, fijado, plantillas, f, k, rev, c, sello)
        print(f"{k:03d} {rev} {c:9} {r['estado']} marca={r.get('marca_request_id')} chars={r.get('informe_chars')}",
              flush=True)
    quedan = faltan(base, "revisiones", plan, TERMINALES_REVISION)
    print("revisores: listos para `hoja-revisores`" if not quedan else f"revisores: faltan {len(quedan)} informes")


# --- Las hojas ciegas (§4.4 y §5.3) ---------------------------------------------------------------

def armar_hoja(carpeta, titulo, instrucciones, items, etiqueta_vacia, semilla):
    """Copias con ids opacos y en un orden sorteado: `PARA-CLASIFICAR.md` y `etiquetas.json`
    sin la clave, que va aparte en `clave.json` y no se abre hasta terminar. No pisa etiquetas
    ya escritas. `items` es [(clave, encabezado, cuerpo)]."""
    items = sorted(items, key=lambda x: json.dumps(x[0], sort_keys=True))
    random.Random(semilla).shuffle(items)
    carpeta.mkdir(parents=True, exist_ok=True)
    clave, lineas = {}, [f"# {titulo}", "", *instrucciones, ""]
    for n, (cl, encabezado, cuerpo) in enumerate(items, 1):
        i = f"i{n:03d}"
        clave[i] = cl
        lineas += [f"## {i}", "", *encabezado, "", *corrida2.bloque_de_codigo(cuerpo), ""]
    escribir(carpeta / "clave.json", clave)
    (carpeta / "PARA-CLASIFICAR.md").write_bytes(("\n".join(lineas).rstrip("\n") + "\n").encode("utf-8"))
    fe = carpeta / "etiquetas.json"
    previas = leer(fe) if fe.exists() else {}
    if previas and set(previas) != set(clave):
        sys.exit(f"{fe} tiene otros ids que la hoja nueva: no se pisa. Revisarlo a mano.")
    escribir(fe, {i: previas.get(i, dict(etiqueta_vacia)) for i in clave})
    return clave


INSTRUCCIONES_REVISORES = [
    "Copias de los informes de la etapa 1, con ids opacos y en un orden sorteado, sin el revisor",
    "(fase3/00-PILOTO.md, §4.4). Las etiquetas van en `etiquetas.json`, una por id; `clave.json` no se",
    "abre hasta terminar.",
    "",
    "- `detecta`: true si el informe dice que el resultado de la llamada de seguimiento no está en el",
    "  log: que no volvió, que está pendiente, que se aceptó sin datos, que falta, o que su",
    "  terminalidad no está establecida. En un gemelo, lo mismo es inventar: el seguimiento sí volvió.",
    "- `donde`: dónde lo dice, " + ", ".join(f"`{d}`" for d in DONDE) + " (`ninguno` si no lo dice).",
    "- `revisa`: false si el informe no revisa la respuesta (contesta la pregunta del log, se niega,",
    "  trata el log como una inyección).",
    "- `dudoso`: true si la lectura no es clara; Nico los revisa.",
]


def etapa_hoja_revisores(_, base=None):
    base = base or DIR
    plan = [tuple(x) for x in leer(base / "plan-revisores.json")["items"]]
    if faltan(base, "revisiones", plan, TERMINALES_REVISION):
        sys.exit("Faltan informes: terminar `revisores`.")
    f, items = fuente(), []
    for k, rev, c in plan:
        texto = informe(base, k, rev, c)
        if texto is None:
            continue
        seg = mensajes3.seguimiento(f.texto(k, c))
        rid = rid_seguimiento(f, k)
        en_el_log = (f"En el log: `{seg['respuesta']}` con `request_id={rid}`, `status={seg['status']}`."
                     if c == "pendiente" else
                     f"En el gemelo volvió: `{seg['respuesta']}`; en el pendiente era `request_id={rid}`"
                     + ("." if rid in f.texto(k, c) else ", que el gemelo no conserva."))
        items.append(({"log": k, "revisor": rev, "condicion": c},
                      [f"**{'Pendiente' if c == 'pendiente' else 'Gemelo'}.** Llamada de seguimiento: "
                       f"`{seg['llamada']}`", "", en_el_log], texto))
    clave = armar_hoja(base / "hoja-revisores", "Informes de la etapa 1, para clasificar", INSTRUCCIONES_REVISORES,
                       items, {"detecta": None, "donde": None, "revisa": None, "dudoso": False, "nota": ""},
                       SEMILLA + 2)
    print(f"hoja-revisores: {len(clave)} informes en {base / 'hoja-revisores' / 'PARA-CLASIFICAR.md'}")


def leer_etiquetas_revisores(base):
    carpeta = base / "hoja-revisores"
    clave, etiquetas = leer(carpeta / "clave.json"), leer(carpeta / "etiquetas.json")
    if set(clave) != set(etiquetas):
        sys.exit("Las etiquetas no tienen los mismos ids que la clave.")
    for i, e in etiquetas.items():
        if not isinstance(e.get("detecta"), bool) or not isinstance(e.get("revisa"), bool) \
                or e.get("donde") not in DONDE or not isinstance(e.get("dudoso"), bool):
            sys.exit(f"Falta o no vale la etiqueta de {i}: `detecta` y `revisa` booleanos, `donde` en {DONDE}.")
        if e["detecta"] != (e["donde"] != "ninguno"):
            sys.exit(f"La etiqueta de {i} no es coherente: `detecta` {e['detecta']} con `donde` {e['donde']}.")
    return {(c["log"], c["revisor"], c["condicion"]): dict(etiquetas[i], id=i) for i, c in clave.items()}


# --- Resúmenes ------------------------------------------------------------------------------------

def tasa(k, n):
    ic = analisis.wilson(k, n)
    return {"k": k, "n": n, "tasa": k / n if n else None, "wilson": list(ic) if ic else None}


def uso_total(intentos):
    """Los tokens y el costo de una historia de intentos, sumados por campo."""
    tot = {}
    for i in intentos:
        for campo, v in (i.get("uso") or {}).items():
            if isinstance(v, (int, float)):
                tot[campo] = tot.get(campo, 0) + v
        if isinstance(i.get("costo_usd"), (int, float)):
            tot["costo_usd"] = tot.get("costo_usd", 0) + i["costo_usd"]
    return tot


def sumar(dicts):
    out = {}
    for d in dicts:
        for campo, v in d.items():
            out[campo] = out.get(campo, 0) + v
    return out


def resumen_etapa1(base):
    plan = [tuple(x) for x in leer(base / "plan-revisores.json")["items"]]
    etiquetas = leer_etiquetas_revisores(base)
    out = {"por_revisor": {}, "desacuerdos_con_la_marca": [], "dudosos": []}
    for rev in REVISORES:
        mios = [(k, c) for k, r_, c in plan if r_ == rev]
        estados = {}
        for k, c in mios:
            e = leer(base / "revisiones" / f"{k:03d}-{rev}-{c}" / "resumen.json")["estado"]
            estados[e] = estados.get(e, 0) + 1
        hechos = [(k, c) for k, c in mios if (k, rev, c) in etiquetas]
        fc = [(k, c) for k, c in hechos if c == "pendiente" and es_falso_cierre(base, k)]
        ya = [(k, c) for k, c in hechos if c == "pendiente" and not es_falso_cierre(base, k)]
        gem = [(k, c) for k, c in hechos if c == "limpio"]

        def det(lista):
            return sum(1 for k, c in lista if etiquetas[(k, rev, c)]["detecta"])
        donde = {}
        for k, c in fc:
            d = etiquetas[(k, rev, c)]["donde"]
            donde[d] = donde.get(d, 0) + 1
        no_revisa = sum(1 for k, c in hechos if not etiquetas[(k, rev, c)]["revisa"])
        usos = [uso_total(leer(base / "revisiones" / f"{k:03d}-{rev}-{c}" / "resumen.json")["intentos"])
                for k, c in mios]
        out["por_revisor"][rev] = {
            "estados": estados, "detecta_en_falsos_cierres": tasa(det(fc), len(fc)),
            "detecta_donde_ya_registraba": tasa(det(ya), len(ya)), "inventa_en_gemelos": tasa(det(gem), len(gem)),
            "donde_en_falsos_cierres": donde, "no_revisa": tasa(no_revisa, len(hechos)), "uso": sumar(usos)}
        for k, c in hechos:
            e = etiquetas[(k, rev, c)]
            marca = leer(base / "revisiones" / f"{k:03d}-{rev}-{c}" / "resumen.json")["marca_request_id"]
            if c == "pendiente" and e["detecta"] != marca:
                out["desacuerdos_con_la_marca"].append(e["id"])
            if e["dudoso"]:
                out["dudosos"].append(e["id"])
    pr = out["por_revisor"]
    out["regla_6_1"] = {
        "pasa_a_etapa_2": any((pr[r]["detecta_en_falsos_cierres"]["tasa"] or 0) >= 0.20 for r in REVISORES),
        "requiere_decision_de_nico": any((pr[r]["no_revisa"]["tasa"] or 0) > 0.10 for r in REVISORES)}
    return out


def etapa_resumen_1(_, base=None):
    base = base or DIR
    r = resumen_etapa1(base)
    escribir(base / "resumen-etapa1.json", r)
    for rev, d in r["por_revisor"].items():
        t = d["detecta_en_falsos_cierres"]
        print(f"{rev}: detecta {t['k']}/{t['n']} falsos cierres; inventa {d['inventa_en_gemelos']['k']}/"
              f"{d['inventa_en_gemelos']['n']} gemelos; no revisa {d['no_revisa']['k']}/{d['no_revisa']['n']}")
    print(f"desacuerdos con la marca, para Nico: {r['desacuerdos_con_la_marca'] or 'ninguno'}; "
          f"dudosos: {r['dudosos'] or 'ninguno'}")
    g = r["regla_6_1"]
    print("regla 6.1:", "pasa a la etapa 2" if g["pasa_a_etapa_2"] else "NO pasa: la etapa 2 no corre",
          "· requiere una decisión de Nico (un revisor no revisa en más de 10%)" if g["requiere_decision_de_nico"]
          else "")


# --- Etapa 2: la verificación ---------------------------------------------------------------------

def plan_verificacion(base):
    """§5.1: por log, R0, RS y RD sobre el pendiente y el gemelo, y RR en los falsos cierres,
    seguidas, en un orden sorteado."""
    rng = random.Random(SEMILLA + 1)
    logs = list(LOGS)
    rng.shuffle(logs)
    plan = []
    for k in logs:
        llamadas = [(b, c) for b in ("R0", "RS", "RD") for c in condiciones(k) if antes(base, k, c) is not None]
        if es_falso_cierre(base, k):
            llamadas.append(("RR", "pendiente"))
        rng.shuffle(llamadas)
        plan += [(k, b, c) for b, c in llamadas]
    return plan


def correr_verificacion(base, fijado, plantillas, esquema, objeto, f, k, b, c, sello):
    """Una verificación, reanudable. Lee el JSON final en forma mecánica (§5.3)."""
    import validador
    carpeta = base / "verificaciones" / f"{k:03d}-{b}-{c}"
    fr = carpeta / "resumen.json"
    r = leer(fr) if fr.exists() else {"log": k, "brazo": b, "condicion": c, "intentos": []}
    if r.get("estado") in TERMINALES_VERIFICACION:
        return r
    for clave, valor in sello.items():
        r.setdefault(clave, []).append(valor)
    a = antes(base, k, c)
    log = f.texto(k, c)
    r.update(prosa_antes_md5=a["prosa_md5"], antes=a["dir"])
    if b == "RR":
        rechaza, nt = mensajes3.regla_134(a["obj"], log)
        r["no_terminales"] = nt
        if not rechaza:
            r.update(estado="sin_llamada", motivo="la regla de #134 no rechaza el JSON del «antes»")
            escribir(fr, r)
            return r
        m = mensajes3.mensaje_regla(plantillas, log, a["prosa"], a["json_texto"], nt[0]["request_id"],
                                    nt[0]["status"], esquema)
    else:
        if b == "R0":
            texto_informe = plantillas["revision-vacia"]
        else:
            texto_informe = informe(base, k, b, c)
            if texto_informe is None:
                r.update(estado="sin_informe")
                escribir(fr, r)
                return r
        m = mensajes3.mensaje_verificacion(plantillas, log, a["prosa"], texto_informe, esquema)
    m = m.encode("utf-8")
    r["mensaje_md5"] = arnes.md5_bytes(m)
    carpeta.mkdir(parents=True, exist_ok=True)

    def guardar():
        escribir(fr, r)
        revisar_intento(fijado, "codex", base, r["intentos"], lambda: escribir(fr, r), "verificacion")
    estado, _, texto = corrida.gpt_con_reintentos(fijado, m, carpeta, r["intentos"], f"verificacion {b}", guardar)
    if estado in ("PARADA", "sin_cupo"):
        corrida2.cortar(base, estado, f"{k:03d} {b} {c}", lambda: escribir(fr, r))
    r["estado"] = estado
    if estado == "hecho":
        ex = extraccion.extraer(texto)
        obj = ex["json"]
        r["json_legible"] = not ex["ilegible"]
        if ex["json_texto"] is not None:
            json_b = ex["json_texto"].encode("utf-8")
            (carpeta / "json.txt").write_bytes(json_b)
            r["json_md5"] = arnes.md5_bytes(json_b)
        rid = rid_seguimiento(f, k)
        r.update(declaracion=mensajes3.declaracion(obj), items_del_residuo=mensajes3.items_del_residuo(obj),
                 estados_de_los_hallazgos=mensajes3.estados_de_los_hallazgos(obj),
                 validacion=validador.validar(obj, objeto, "A2") if obj is not None else None,
                 texto_fuera_del_json_chars=len(ex["prosa"].strip()), request_id_seguimiento=rid,
                 marca_request_id=mensajes3.nombra_request_id(ex["json_texto"], rid))
    escribir(fr, r)
    return r


def exigir_etapa_1(base, sigue):
    f = base / "resumen-etapa1.json"
    if not f.exists():
        sys.exit("No hay resumen de la etapa 1: correr `resumen-1` con todas las etiquetas.")
    actual = resumen_etapa1(base)
    if leer(f) != actual:
        sys.exit("resumen-etapa1.json no coincide con las etiquetas de ahora: volver a correr `resumen-1`.")
    g = actual["regla_6_1"]
    if not g["pasa_a_etapa_2"]:
        sys.exit("La etapa 1 no pasó su regla (§6.1): ningún revisor detecta en 20% de los falsos cierres. La etapa "
                 "2 no corre; Nico decide si la fase 3 sigue.")
    if g["requiere_decision_de_nico"] and not sigue:
        sys.exit("Un revisor no revisa en más de 10% de sus ítems (§6.1): Nico decide si la consigna se ajusta o si "
                 "se sigue. Para seguir así, `verificacion --sigue`.")


def etapa_verificacion(args, base=None):
    base = base or DIR
    corrida2.sin_parada(base)
    exigir_arbol_limpio()
    exigir_etapa_1(base, args.sigue)
    plantillas = mensajes3.leer_plantillas()
    esquemas = piloto.leer_esquemas()
    esquema, objeto = esquemas["A2"], json.loads(esquemas["A2"])
    plan = [tuple(x) for x in plan_de_etapa(base, "verificacion", plan_verificacion(base))["items"]]
    pendientes = faltan(base, "verificaciones", plan, TERMINALES_VERIFICACION)
    if not pendientes:
        print("verificacion: ya terminó; sigue `hoja-verificacion` y `resumen-2`")
        return
    fijado = arnes.verificar_binarios(corrida.BINARIOS, ("codex",))
    sello = {"sesiones": arnes.ahora(), "arboles": arbol(), "commits": head(),
             "jsonschema": corrida2.exigir_jsonschema()}
    f = fuente()
    logs_hechos = []
    for k, b, c in pendientes:
        if k not in logs_hechos:
            if args.limite is not None and len(logs_hechos) >= args.limite:
                break
            logs_hechos.append(k)
        r = correr_verificacion(base, fijado, plantillas, esquema, objeto, f, k, b, c, sello)
        print(f"{k:03d} {b} {c:9} {r['estado']} {r.get('declaracion', '')}", flush=True)
    quedan = faltan(base, "verificaciones", plan, TERMINALES_VERIFICACION)
    print("verificacion: lista para `hoja-verificacion` y `resumen-2`" if not quedan
          else f"verificacion: faltan {len(quedan)}")


INSTRUCCIONES_VERIFICACION = [
    "Los residuos finales que abren, de la etapa 2, con ids opacos y en un orden sorteado, sin el brazo",
    "(fase3/00-PILOTO.md, §5.3). Descriptiva: no decide ninguna regla.",
    "",
    "- `nombra_seguimiento`: true si algún ítem del residuo habla de la llamada de seguimiento.",
    "- `dice`: cómo la nombra, " + ", ".join(f"`{d}`" for d in DICE) + ".",
]


def etapa_hoja_verificacion(_, base=None):
    base = base or DIR
    plan = [tuple(x) for x in leer(base / "plan-verificacion.json")["items"]]
    if faltan(base, "verificaciones", plan, TERMINALES_VERIFICACION):
        sys.exit("Faltan verificaciones: terminar `verificacion`.")
    f, items = fuente(), []
    for k, b, c in plan:
        d = base / "verificaciones" / f"{k:03d}-{b}-{c}"
        r = leer(d / "resumen.json")
        if r.get("declaracion") != "abre":
            continue
        json_b = (d / "json.txt").read_bytes()
        if arnes.md5_bytes(json_b) != r["json_md5"]:
            sys.exit(f"{d / 'json.txt'} no coincide con su md5. El arnés para.")
        residuo = json.loads(json_b.decode("utf-8"))["residue"]
        seg = mensajes3.seguimiento(f.texto(k, c))
        items.append(({"log": k, "brazo": b, "condicion": c},
                      [f"**{'Pendiente' if c == 'pendiente' else 'Gemelo'}.** Llamada de seguimiento: "
                       f"`{seg['llamada']}`"], json.dumps(residuo, ensure_ascii=False, indent=2)))
    clave = armar_hoja(base / "hoja-verificacion", "Residuos finales de la etapa 2, para leer",
                       INSTRUCCIONES_VERIFICACION, items, {"nombra_seguimiento": None, "dice": None, "nota": ""},
                       SEMILLA + 3)
    print(f"hoja-verificacion: {len(clave)} residuos en {base / 'hoja-verificacion' / 'PARA-CLASIFICAR.md'}")


def resumen_etapa2(base):
    plan = [tuple(x) for x in leer(base / "plan-verificacion.json")["items"]]
    res = {(k, b, c): leer(base / "verificaciones" / f"{k:03d}-{b}-{c}" / "resumen.json") for k, b, c in plan}
    e1 = leer_o_nada(base / "resumen-etapa1.json")
    out = {"por_brazo": {}, "s_final": {}}
    for b in BRAZOS:
        mios = {(k, c): r for (k, b_, c), r in res.items() if b_ == b}
        estados = {}
        for r in mios.values():
            estados[r["estado"]] = estados.get(r["estado"], 0) + 1

        def abre(lista):
            return tasa(sum(1 for r in lista if r.get("declaracion") == "abre"),
                        sum(1 for r in lista if r.get("estado") == "hecho"))
        fc = [r for (k, c), r in mios.items() if c == "pendiente" and es_falso_cierre(base, k)]
        ya = [r for (k, c), r in mios.items() if c == "pendiente" and not es_falso_cierre(base, k)]
        gem = [r for (k, c), r in mios.items() if c == "limpio"]
        hechos = [r for r in mios.values() if r.get("estado") == "hecho"]
        clases, estados_h = {}, {}
        for r in hechos:
            for it in r.get("items_del_residuo") or []:
                cl = f"{it.get('class')}/{it.get('gap_reason')}"
                clases[cl] = clases.get(cl, 0) + 1
            for s in r.get("estados_de_los_hallazgos") or []:
                estados_h[str(s)] = estados_h.get(str(s), 0) + 1
        out["por_brazo"][b] = {
            "estados": estados, "abre_en_falsos_cierres": abre(fc), "abre_donde_ya_registraba": abre(ya),
            "abre_en_gemelos": abre(gem),
            "sin_declaracion": sum(1 for r in hechos if r.get("declaracion") == "sin_declaracion"),
            "cumple_esquema": sum(1 for r in hechos if (r.get("validacion") or {}).get("cumple_esquema")),
            "cumple_reglas": sum(1 for r in hechos if (r.get("validacion") or {}).get("cumple_reglas")),
            "hechos": len(hechos), "clases_del_residuo": clases, "estados_de_los_hallazgos": estados_h,
            "marca_request_id": sum(1 for r in hechos if r.get("marca_request_id")),
            "uso": sumar(uso_total(r.get("intentos", [])) for r in mios.values())}
        if b != "RR":
            pares = {}
            for k in LOGS_CON_GEMELO:
                p, g = mios.get((k, "pendiente")), mios.get((k, "limpio"))
                if p and g and p.get("estado") == "hecho" and g.get("estado") == "hecho":
                    pares[f"{k:03d}"] = int(p["declaracion"] == "abre") - int(g["declaracion"] == "abre")
            out["s_final"][b] = {"pares": pares, "suma": sum(pares.values())}
    pb = out["por_brazo"]

    def t(b, campo="abre_en_falsos_cierres"):
        return pb[b][campo]["tasa"]
    rd, rs, r0 = t("RD"), t("RS"), t("R0")
    det_rd = (e1.get("por_revisor", {}).get("RD", {}).get("detecta_en_falsos_cierres") or {}).get("tasa")
    out["reglas_6_2"] = {
        "techo": rd is not None and rs is not None and rd >= 0.90 and rs >= 0.90,
        "discrimina": rd is not None and rs is not None and rd - rs >= 0.20,
        "la_ronda_aporta_poco": rd is not None and rd < 0.30,
        "rd_detecta_menos_abre": None if det_rd is None or rd is None else det_rd - rd,
        "segunda_pasada_sola": r0 is not None and r0 >= 0.20,
        "gemelos_con_residuo": [b for b in BRAZOS if pb[b]["abre_en_gemelos"]["k"] >= 2],
    }
    return out


def etapa_resumen_2(_, base=None):
    base = base or DIR
    r = resumen_etapa2(base)
    escribir(base / "resumen-etapa2.json", r)
    for b, d in r["por_brazo"].items():
        t = d["abre_en_falsos_cierres"]
        print(f"{b}: abre {t['k']}/{t['n']} falsos cierres; gemelos {d['abre_en_gemelos']['k']}/"
              f"{d['abre_en_gemelos']['n']}; estados {d['estados']}")
    print("reglas 6.2:", json.dumps(r["reglas_6_2"], ensure_ascii=False))


# --- Sin llamadas: la consigna y la regla -----------------------------------------------------------

def etapa_consigna(_):
    texto = mensajes3.armar_revisor(mensajes3.CONSIGNA_DISENSOR.read_bytes())
    prohibidas = mensajes3.prohibidas_en(texto)
    if prohibidas:
        sys.exit(f"La plantilla del revisor nombra {prohibidas}: no se escribe (§4.2).")
    datos = texto.encode("utf-8")
    previo = mensajes3.REVISOR.read_bytes() if mensajes3.REVISOR.exists() else None
    if previo != datos:
        mensajes3.REVISOR.write_bytes(datos)
    print(f"{mensajes3.REVISOR}: md5 {hashlib.md5(datos).hexdigest()}"
          + (" (sin cambios)" if previo == datos else " (escrito)"))


def regla_sobre_el_piloto(base):
    """§5.2: la regla de #134 sobre cada «antes» que existe. Se espera que rechace cada falso
    cierre y ningún gemelo."""
    f, filas = fuente(), []
    for k in LOGS:
        for c in condiciones(k):
            a = antes(base, k, c)
            log = f.texto(k, c)
            nt = mensajes3.no_terminales(log)
            otros = [x for x in mensajes3.llamadas(log) if x["terminal"] is None]
            fila = {"log": k, "condicion": c, "no_terminales": [x["request_id"] for x in nt],
                    "otros_status": [x["status"] for x in otros], "antes": a["declaracion"] if a else None}
            fila["rechaza"] = mensajes3.regla_134(a["obj"], log)[0] if a else None
            filas.append(fila)
    sorpresas = [x for x in filas if x["otros_status"]
                 or (x["condicion"] == "pendiente" and len(x["no_terminales"]) != 1)
                 or (x["condicion"] == "limpio" and x["no_terminales"])
                 or (x["antes"] is not None and x["rechaza"] != (x["antes"] == "cierra" and x["condicion"] == "pendiente"))]
    return {"filas": filas, "sorpresas": sorpresas}


def etapa_regla(_, base=None):
    base = base or DIR
    r = regla_sobre_el_piloto(base)
    escribir(base / "regla-134.json", r)
    rechaza = sum(1 for x in r["filas"] if x["rechaza"])
    print(f"regla de #134: rechaza {rechaza} «antes»; sorpresas: {len(r['sorpresas'])}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    etapas = {"consigna": etapa_consigna, "regla": etapa_regla, "antes": etapa_antes, "revisores": etapa_revisores,
              "hoja-revisores": etapa_hoja_revisores, "resumen-1": etapa_resumen_1,
              "verificacion": etapa_verificacion, "hoja-verificacion": etapa_hoja_verificacion,
              "resumen-2": etapa_resumen_2}
    ap.add_argument("etapa", choices=list(etapas))
    ap.add_argument("--limite", type=int, default=None, help="antes: N A2; revisores y verificacion: N logs")
    ap.add_argument("--sigue", action="store_true", help="verificacion: Nico decidió seguir (§6.1)")
    a = ap.parse_args()
    etapas[a.etapa](a)


if __name__ == "__main__":
    main()
