"""El cruce de las ausencias falsas de A2 pendiente con el validador de §5.3.

Corrección del 15/10/2026 a `29-INFORME-DISENSOR.md`: la primera versión decía que las 71
declaraciones de ausencia con el hueco abierto pasaban el esquema y todas las reglas. Este
script rehace el cruce desde las 100 respuestas de A2 pendiente, sin llamar a ningún modelo:

- saca el JSON de cada `corrida/brazos/NNN-A2-pendiente/intento-1-ultimo-mensaje.md` con
  `herramientas/extraccion.py`, como hizo `corrida.py brazos`;
- lo valida con `herramientas/validador.py` contra `esquemas/residuo.json` (fragmento de
  esquema y las cuatro reglas: R1, R2, R2 bis y R8);
- compara cada resultado con el que guardó la corrida en `resumen.json`, y sale con error si
  alguno difiere;
- cruza `declared_absence` con el resultado del validador.

Imprime sólo números de log, conteos y los mensajes del validador: no muestra ninguna respuesta.

No está en `herramientas/` a propósito: `corrida.py validacion` y `analizar` recalculan el md5
del árbol de `herramientas/`, `prompts/` y `esquemas/` y paran si cambió (§4.4). Un archivo
nuevo ahí rompería la reproducción de la corrida.

    python cruces\\ausencias_y_reglas.py

Sin `-I`: `jsonschema` está en el site de usuario de Python, como dependencia de disensor
(lo mismo dice `herramientas/validador.py`). La extracción y las reglas son stdlib.
"""
import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))

import extraccion  # noqa: E402
import validador  # noqa: E402

BRAZOS = RAIZ / "corrida" / "brazos"
ESQUEMAS = RAIZ / "esquemas"


def esquema_de_a2():
    """Como `piloto.leer_esquemas`: el fragmento de A2, verificado contra su md5."""
    datos = (ESQUEMAS / "residuo.json").read_bytes()
    esperado = json.loads((ESQUEMAS / "fragmentos.json").read_text(encoding="utf-8"))["residuo"]["md5"]
    if hashlib.md5(datos).hexdigest() != esperado:
        sys.exit("esquemas/residuo.json no coincide con su md5 de fragmentos.json.")
    return json.loads(datos.decode("utf-8"))


def rehacer(carpeta, esquema):
    """Lo que `corrida.etapa_brazos` guardó para una llamada terminada, recalculado."""
    mensajes = sorted(carpeta.glob("intento-*-ultimo-mensaje.md"))
    if len(mensajes) != 1:
        sys.exit(f"{carpeta.name}: se esperaba un solo intento y hay {len(mensajes)}.")
    ex = extraccion.extraer(mensajes[0].read_bytes().decode("utf-8"))
    obj = ex["json"]
    tiene_residue = isinstance(obj, dict) and isinstance(obj.get("residue"), dict)
    return {"json_legible": not ex["ilegible"],
            "declared_absence": obj["residue"].get("declared_absence") if tiene_residue else None,
            "validacion": validador.validar(obj, esquema, "A2") if obj is not None else None}


def main():
    esquema = esquema_de_a2()
    carpetas = sorted(BRAZOS.glob("*-A2-pendiente"))
    filas = []
    for carpeta in carpetas:
        guardado = json.loads((carpeta / "resumen.json").read_text(encoding="utf-8"))
        if guardado.get("estado") != "hecho":
            sys.exit(f"{carpeta.name}: la llamada no terminó ({guardado.get('estado')}).")
        nuevo = rehacer(carpeta, esquema)
        distinto = [k for k in nuevo if nuevo[k] != guardado.get(k)]
        if distinto:
            sys.exit(f"{carpeta.name}: el cruce no reproduce lo guardado en resumen.json ({', '.join(distinto)}).")
        filas.append((guardado["log"], nuevo))

    legibles = [(k, r) for k, r in filas if r["json_legible"]]
    validados = [(k, r) for k, r in filas if r["validacion"] is not None]
    ausencias = [(k, r) for k, r in filas if r["declared_absence"] is True]
    falla_esquema = [(k, r) for k, r in validados if not r["validacion"]["cumple_esquema"]]
    falla_reglas = [(k, r) for k, r in validados if not r["validacion"]["cumple_reglas"]]
    reglas = sorted({e.split("]")[0] + "]" for _, r in falla_reglas for e in r["validacion"]["errores_de_reglas"]})
    aus_pasan = [k for k, r in ausencias
                 if r["validacion"]["cumple_esquema"] and r["validacion"]["cumple_reglas"]]
    aus_fallan = [(k, r) for k, r in ausencias
                  if not (r["validacion"]["cumple_esquema"] and r["validacion"]["cumple_reglas"])]

    print(f"jsonschema {validador.version_de_jsonschema()}; esquema esquemas/residuo.json (md5 verificado)")
    print(f"Respuestas de A2 pendiente: {len(filas)}; las {len(filas)} reproducen lo guardado en resumen.json")
    print(f"JSON legible: {len(legibles)}; validadas: {len(validados)}")
    print(f"Fallan el esquema: {len(falla_esquema)} {[k for k, _ in falla_esquema]}")
    print(f"Fallan alguna regla: {len(falla_reglas)} {[k for k, _ in falla_reglas]}; reglas que fallan: {reglas}")
    print(f"Declaran ausencia (declared_absence true): {len(ausencias)}")
    print(f"  pasan esquema y las cuatro reglas: {len(aus_pasan)}")
    print(f"  no pasan: {len(aus_fallan)}")
    for k, r in aus_fallan:
        v = r["validacion"]
        for e in v["errores_de_esquema"] + v["errores_de_reglas"]:
            print(f"    log {k:03d}: {e}")


if __name__ == "__main__":
    main()
