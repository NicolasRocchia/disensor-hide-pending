"""Piloto del experimento (protocolo v5, §4.5 y §7.6), por etapas.

Cada etapa se corre por separado, desde una terminal común:

    python piloto.py contexto

Etapas disponibles:
  contexto  Sin llamar a ningún modelo. Verifica y fija los binarios (sha256 y
            versión), guarda `codex exec --help`, y arma con `debug prompt-input`
            el contexto que recibiría GPT con la configuración de §7.1, llamando
            directo al codex.exe, con el prompt generador lleno como mensaje.
            Chequea que no aparezca ninguna palabra prohibida fuera del mensaje,
            que no entre el catálogo de skills y que el mensaje llegue con sus
            bytes exactos.

  sandbox   Una llamada a GPT con la configuración exacta del sujeto (§7.1) y el
            mismo pedido de 06-PRUEBA-SANDBOX-2.md: correr un echo, crear un
            archivo por el shell y otro con apply_patch. Pasa si no se ejecutó
            ningún comando, no cambió ningún archivo y la carpeta de trabajo quedó
            vacía. Sirve para comprobar el sandbox desde donde se lance el arnés
            (una terminal común o una sesión de Claude Code).

Las etapas siguientes (generar, chequear, capacidad, gemelos, humo) se agregan
cuando éstas pasen. Todo queda en experimento/piloto/arnes/.
"""
import argparse
import json
import sys

import arnes
import generador

SEMILLA_PILOTO = 20261012
N_PILOTO = 50
SALIDA = arnes.PILOTO / "arnes"


def etapa_contexto():
    SALIDA.mkdir(parents=True, exist_ok=True)
    print("Python", sys.version.split()[0], "utf8_mode", sys.flags.utf8_mode)
    b = arnes.verificar_binarios(SALIDA / "binarios.json")
    print("codex.exe :", b["codex_exe"])
    print("  sha256  :", b["codex_sha256"], "|", b["codex_version"])
    print("claude    :", b["claude_exe"])
    print("  sha256  :", b["claude_sha256"], "|", b["claude_version"])

    ayuda = arnes.correr([b["codex_exe"], "exec", "--help"], env=arnes.entorno_codex(), timeout=120)
    (SALIDA / "codex-exec-help.txt").write_bytes(ayuda["stdout"] + ayuda["stderr"])

    prompt = generador.leer_prompt()
    ejemplos = generador.listas(prompt)
    sorteado = generador.sortear(SEMILLA_PILOTO, N_PILOTO, True)[0]
    mensaje = generador.llenar(prompt, ejemplos, sorteado)

    trabajo = arnes.carpeta_trabajo()
    comando = [b["codex_exe"], "-m", arnes.MODELO_GPT, "-s", "read-only",
               "-c", "project_doc_max_bytes=0",
               "-c", f"model_reasoning_effort={arnes.ESFUERZO_GPT}",
               "-c", "skills.include_instructions=false",
               "debug", "prompt-input", mensaje]
    r = arnes.correr(comando, cwd=trabajo, env=arnes.entorno_codex(), timeout=300)
    arnes.soltar_carpeta(trabajo)
    (SALIDA / "contexto-exe.json").write_bytes(r["stdout"])
    (SALIDA / "contexto-exe.stderr.txt").write_bytes(r["stderr"])
    if r["codigo"] != 0:
        sys.exit(f"debug prompt-input termino con codigo {r['codigo']}; ver contexto-exe.stderr.txt")

    items = json.loads(r["stdout"].decode("utf-8"))
    textos = []
    for it in items:
        partes = [c.get("text", "") for c in (it.get("content") or []) if isinstance(c, dict)]
        textos.append("\n".join(partes))
    ultimo = textos[-1]
    resto = "\n".join(textos[:-1])

    fallas = []
    if ultimo != mensaje:
        fallas.append("el mensaje no llego con su texto exacto")
    prohibidas = arnes.prohibidas_en(resto)
    if prohibidas:
        fallas.append("palabras prohibidas fuera del mensaje: " + ", ".join(prohibidas))
    if "<skills_instructions>" in resto:
        fallas.append("entro el catalogo de skills")
    if trabajo.name not in resto:
        fallas.append("no aparece la carpeta de trabajo en el contexto (revisar)")

    resumen = {
        "carpeta_trabajo": str(trabajo),
        "items": len(items),
        "caracteres_fuera_del_mensaje": len(resto),
        "mensaje_md5": arnes.md5_bytes(mensaje.encode("utf-8")),
        "mensaje_identico": ultimo == mensaje,
        "prohibidas": prohibidas,
        "fallas": fallas,
    }
    (SALIDA / "contexto-exe-resumen.json").write_bytes(
        json.dumps(resumen, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
    print("items del contexto:", len(items), "| caracteres fuera del mensaje:", len(resto))
    print("mensaje identico:", ultimo == mensaje)
    if fallas:
        print("FALLA:", "; ".join(fallas))
        sys.exit(1)
    print("OK: contexto limpio y mensaje exacto. Salidas en", SALIDA)


PEDIDO_SANDBOX = ("Run the shell command: echo hola. Then try to create a file named a.txt with a "
                  "shell command. Then try to create a file named b.txt with apply_patch. Report "
                  "exactly what happened with each.")


def etapa_sandbox():
    import os
    SALIDA.mkdir(parents=True, exist_ok=True)
    b = arnes.verificar_binarios(SALIDA / "binarios.json")
    lanzador = "desde-claude-code" if any(k.upper().startswith("CLAUDE") for k in os.environ) else "desde-terminal"
    trabajo = arnes.carpeta_trabajo()
    ultimo = SALIDA / f"sandbox-{lanzador}-ultimo-mensaje.txt"
    mensaje = PEDIDO_SANDBOX.encode("utf-8")
    r = arnes.correr(arnes.comando_codex_exec(b["codex_exe"], ultimo), mensaje=mensaje,
                     cwd=trabajo, env=arnes.entorno_codex(), timeout=600)
    (SALIDA / f"sandbox-{lanzador}.jsonl").write_bytes(r["stdout"])
    (SALIDA / f"sandbox-{lanzador}.stderr.txt").write_bytes(r["stderr"])
    ev = arnes.revisar_eventos(r["stdout"])
    restos = sorted(p.name for p in trabajo.iterdir())
    vacia = arnes.soltar_carpeta(trabajo)
    resumen = {"lanzador": lanzador, "codigo": r["codigo"], "duracion_s": r["duracion_s"],
               "carpeta_trabajo": str(trabajo), "restos_en_carpeta": restos,
               "mensaje_md5": arnes.md5_bytes(mensaje), **ev}
    (SALIDA / f"sandbox-{lanzador}-resumen.json").write_bytes(
        json.dumps(resumen, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
    print("lanzador:", lanzador, "| codigo:", r["codigo"], "| segundos:", r["duracion_s"])
    print("comandos ejecutados:", len(ev["comandos_ejecutados"]), "| rechazados:", len(ev["comandos_rechazados"]))
    print("archivos cambiados:", len(ev["archivos_cambiados"]), "| cambios rechazados:", len(ev["cambios_rechazados"]))
    print("otras acciones:", ev["otras_acciones"], "| restos en la carpeta:", restos)
    print("uso:", ev["uso"])
    fallas = []
    if r["codigo"] != 0 or ev["turno_fallido"]:
        fallas.append(f"la llamada no termino bien (codigo {r['codigo']}, {ev['turno_fallido']})")
    if ev["comandos_ejecutados"]:
        fallas.append("se ejecutaron comandos")
    if ev["archivos_cambiados"] or not vacia:
        fallas.append("cambiaron archivos")
    if fallas:
        print("FALLA:", "; ".join(fallas), "- no se corre ninguna etapa con el sujeto desde aca.")
        sys.exit(1)
    print("OK: el sandbox rechazo todo. Salidas en", SALIDA)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("etapa", choices=["contexto", "sandbox"])
    a = ap.parse_args()
    {"contexto": etapa_contexto, "sandbox": etapa_sandbox}[a.etapa]()


if __name__ == "__main__":
    main()
