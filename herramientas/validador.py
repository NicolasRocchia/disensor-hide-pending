"""El validador de §5.3 (protocolo v16): sólo descriptivo, no toca ninguna variable de C2.

Cada JSON se valida contra su fragmento de esquema con `jsonschema`
(`Draft202012Validator`, sin verificar formatos, igual que `rules.py` de disensor).
En A2, además, exactamente cuatro reglas de `rules.py` en `de14e5c`, las únicas que
leen sólo `findings` y `residue`: R1, R2, R2 bis y R8. Están reimplementadas acá
porque `rules.py` lee el sobre del evento antes de correr cualquier regla, y porque
`rules.py` supone un artefacto ya válido contra el esquema: estas toleran un JSON mal
formado (un campo que falta o tiene otro tipo no dispara la regla; lo informa el
esquema).

`jsonschema` no es de la biblioteca estándar: está en el site de usuario de Python,
como dependencia de disensor. Por eso el arnés y sus pruebas corren sin `python -I`.
"""
from importlib.metadata import version

# Copiados textuales de src/disensor/rules.py en de14e5c.
GENERIC_MARKERS = {
    # English
    "n/a", "na", "none", "all resolved", "applied", "ok", "no residue",
    "-", "not applicable", "done", "resolved",
    # Spanish (teams write in their own language; laziness has no border)
    "ninguno", "ninguna", "todo resuelto", "aplicado", "sin residuo", "no aplica",
}
RESIDUE_STATES = {"escalated_open", "refuted_verifiable", "refuted_interpretive"}
EXPECTED_CLASS = {
    "escalated_open": "escalation_without_decision",
    "refuted_verifiable": "principal_refutation",
    "refuted_interpretive": "principal_refutation",
}
TEMPLATE_MARKER = "FILL_IN"


def version_de_jsonschema():
    return version("jsonschema")


def errores_de_esquema(obj, esquema):
    """Como `rules.schema_errors`: los errores ordenados por ruta."""
    from jsonschema import Draft202012Validator
    validador = Draft202012Validator(esquema)
    return [f"[schema] {'/'.join(str(p) for p in err.path) or '(root)'}: {err.message}"
            for err in sorted(validador.iter_errors(obj), key=lambda x: [str(p) for p in x.path])]


def _dicts(lista):
    return [x for x in lista if isinstance(x, dict)] if isinstance(lista, list) else []


def errores_de_reglas(obj):
    """R1, R2, R2 bis y R8 de `rules.py` en de14e5c, sobre `findings` y `residue`."""
    e = []
    if not isinstance(obj, dict):
        return e
    hallazgos = _dicts(obj.get("findings"))
    residuo = obj.get("residue") if isinstance(obj.get("residue"), dict) else {}
    items = _dicts(residuo.get("items"))
    por_id = {h.get("id"): h for h in hallazgos if isinstance(h.get("id"), str)}

    # R1: cada hallazgo en un estado de residuo tiene su item, y cada item con referencia
    # apunta a un hallazgo que existe y cuyo estado corresponde a su clase.
    if obj.get("findings") is not None:
        refs = {i.get("finding_ref") for i in items if i.get("finding_ref")}
        for h in hallazgos:
            if h.get("final_state") in RESIDUE_STATES and h.get("id") not in refs:
                e.append(f"[R1] finding {h.get('id')} ({h.get('final_state')}) without a residue item")
        for i in items:
            ref = i.get("finding_ref")
            if ref:
                if ref not in por_id:
                    e.append(f"[R1] item {i.get('id')} references nonexistent finding {ref}")
                else:
                    st = por_id[ref].get("final_state")
                    if st in EXPECTED_CLASS and i.get("class") != EXPECTED_CLASS[st]:
                        e.append(f"[R1] item {i.get('id')} class {i.get('class')} does not match state {st} of {ref}")

    # R2: ningún marcador genérico en las declaraciones de texto.
    textos = []
    if residuo.get("declared_absence"):
        textos.append(("residue.declaration", residuo.get("declaration", "")))
    for i in items:
        if "description" in i:
            textos.append((f"residue.items[{i.get('id')}].description", i["description"]))
    for donde, t in textos:
        if isinstance(t, str) and t.strip().lower() in GENERIC_MARKERS:
            e.append(f"[R2] generic marker in {donde}: '{t}'")

    # R2 bis: ningún campo empieza con el marcador de plantilla.
    def buscar(valor, ruta):
        if isinstance(valor, str) and valor.startswith(TEMPLATE_MARKER):
            e.append(f"[R2] unfilled template marker in {ruta}")
        elif isinstance(valor, dict):
            for k, v in valor.items():
                buscar(v, f"{ruta}.{k}")
        elif isinstance(valor, list):
            for n, v in enumerate(valor):
                buscar(v, f"{ruta}[{n}]")
    buscar(obj, "artifact")

    # R8: una refutación interpretativa pide atención humana.
    for i in items:
        if i.get("refutation_type") == "interpretive" and not i.get("requires_human_attention"):
            e.append(f"[R8] item {i.get('id')}: interpretive refutation with requires_human_attention=false")
    return e


def validar(obj, esquema, brazo):
    """§5.3 para un JSON legible: errores de esquema y, en A2, de las cuatro reglas."""
    esq = errores_de_esquema(obj, esquema)
    reglas = errores_de_reglas(obj) if brazo == "A2" else []
    return {"cumple_esquema": not esq, "errores_de_esquema": esq,
            "cumple_reglas": not reglas if brazo == "A2" else None, "errores_de_reglas": reglas}
