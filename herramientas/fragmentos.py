"""Los dos esquemas de los brazos, por script (protocolo v11, §5.2).

Salen de `src/disensor/residue.schema.json` de disensor en el commit fijado,
leído con `git show` del repositorio de disensor, sin tocar su checkout:

    python experimento\\herramientas\\fragmentos.py [ruta del repo de disensor]

Escribe `experimento/esquemas/residuo.json`, `placebo.json` y `fragmentos.json`
(commit, md5 de la fuente, md5 y tamaño de cada fragmento, y los conteos de
vocabulario de §5.4).
"""
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

COMMIT = "de14e5c"
RUTA_FUENTE = "src/disensor/residue.schema.json"
REPO_POR_DEFECTO = Path(r"D:\Programacion\Disensor")
SALIDA = Path(__file__).resolve().parent.parent / "esquemas"

# §5.2: la raíz conserva estas claves, en el orden en que están en la fuente.
RAIZ = ("$schema", "type", "required", "additionalProperties", "properties", "$defs", "allOf")
QUITAR_DE_FINDING = ("final_state", "verification", "fix_verification", "remedy_adjustment",
                     "debt_id", "risk_record", "evidence")
VOCABULARIO = ("tool", "query", "missing", "async", "incomplete", "execution", "pending", "Honest")


def leer_fuente(repo):
    datos = subprocess.run(["git", "-C", str(repo), "show", f"{COMMIT}:{RUTA_FUENTE}"],
                           capture_output=True, check=True).stdout
    return datos, json.loads(datos.decode("utf-8"))


def referencias(obj):
    """Los nombres de `$defs` a los que apunta cualquier `$ref` dentro de `obj`."""
    out = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "$ref" and isinstance(v, str) and v.startswith("#/$defs/"):
                out.add(v[len("#/$defs/"):])
            else:
                out |= referencias(v)
    elif isinstance(obj, list):
        for v in obj:
            out |= referencias(v)
    return out


def alcanzables(raiz_sin_defs, defs):
    """Los `$defs` alcanzables desde la raíz, siguiendo referencias entre definiciones."""
    vistos, pendientes = set(), list(referencias(raiz_sin_defs))
    while pendientes:
        n = pendientes.pop()
        if n in vistos:
            continue
        vistos.add(n)
        pendientes.extend(referencias(defs[n]))
    return vistos


def _armar(fuente, propiedades, all_of, defs_nuevos, requeridas):
    out = {}
    for clave in fuente:
        if clave not in RAIZ:
            continue
        if clave == "required":
            out["required"] = requeridas
        elif clave == "properties":
            out["properties"] = {k: copy.deepcopy(fuente["properties"][k]) for k in propiedades}
        elif clave == "$defs":
            out["$defs"] = defs_nuevos
        elif clave == "allOf":
            if all_of:
                out["allOf"] = all_of
        else:
            out[clave] = copy.deepcopy(fuente[clave])
    return out


def construir(fuente):
    """§5.2: devuelve (residuo, placebo), como objetos."""
    # ESQUEMA_RESIDUO: findings y residue tal cual; la entrada 0 del allOf de la raíz;
    # los $defs alcanzables. Una transformación: findings pasa a ser requerida (R10).
    props_r = [k for k in fuente["properties"] if k in ("findings", "residue")]
    all_of_r = [copy.deepcopy(fuente["allOf"][0])]
    sin_defs = {"properties": {k: fuente["properties"][k] for k in props_r}, "allOf": all_of_r}
    nombres = alcanzables(sin_defs, fuente["$defs"])
    defs_r = {k: copy.deepcopy(v) for k, v in fuente["$defs"].items() if k in nombres}
    req_r = [k for k in props_r if k in fuente["required"] or k == "findings"]
    residuo = _armar(fuente, props_r, all_of_r, defs_r, req_r)

    # ESQUEMA_PLACEBO: el mismo fragmento sin lo que distingue a la declaración de
    # residuo de un listado de hallazgos.
    finding = copy.deepcopy(fuente["$defs"]["finding"])
    for k in QUITAR_DE_FINDING:
        finding["properties"].pop(k, None)
    finding["required"] = [k for k in finding["required"] if k not in QUITAR_DE_FINDING]
    finding.pop("allOf", None)
    props_p = ["findings"]
    defs_todos = dict(fuente["$defs"], finding=finding)
    nombres_p = alcanzables({"properties": {"findings": fuente["properties"]["findings"]}}, defs_todos)
    defs_p = {k: (finding if k == "finding" else copy.deepcopy(v))
              for k, v in fuente["$defs"].items() if k in nombres_p}
    placebo = _armar(fuente, props_p, [], defs_p, ["findings"])
    return residuo, placebo


def serializar(obj):
    """Compacto, sin escapar lo que no es ASCII, en el orden de la fuente."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def vocabulario(texto):
    return {p: len(re.findall(re.escape(p), texto)) if p == "Honest" else len(re.findall(re.escape(p), texto, re.I))
            for p in VOCABULARIO}


def main():
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_POR_DEFECTO
    crudo, fuente = leer_fuente(repo)
    residuo, placebo = construir(fuente)
    SALIDA.mkdir(exist_ok=True)
    info = {"commit": COMMIT, "fuente": RUTA_FUENTE, "fuente_md5": hashlib.md5(crudo).hexdigest()}
    for nombre, obj in (("residuo", residuo), ("placebo", placebo)):
        texto = serializar(obj)
        (SALIDA / f"{nombre}.json").write_bytes(texto.encode("utf-8"))
        info[nombre] = {"md5": hashlib.md5(texto.encode("utf-8")).hexdigest(), "caracteres": len(texto),
                        "defs": list(obj["$defs"]), "propiedades": list(obj["properties"]),
                        "required": obj["required"], "vocabulario": vocabulario(texto)}
    (SALIDA / "fragmentos.json").write_bytes(json.dumps(info, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
    for nombre in ("residuo", "placebo"):
        i = info[nombre]
        print(f"{nombre}: {i['caracteres']} caracteres | md5 {i['md5']} | defs {i['defs']} | "
              f"required {i['required']} | vocabulario {i['vocabulario']}")
    print("fuente:", COMMIT, RUTA_FUENTE, "md5", info["fuente_md5"])


if __name__ == "__main__":
    main()
