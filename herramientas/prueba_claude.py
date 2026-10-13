"""Prueba de Claude Code para el piloto (protocolo v4, §7.2 y §7.6).

Copia el binario versionado de Claude Code a una ruta fija con extensión .exe,
verifica que la copia sea idéntica, guarda su --help y hace dos llamadas
mínimas a Opus desde una carpeta de trabajo neutra: sin y con
--system-prompt "". Escribe todo en experimento/piloto/. No toca nada más.
"""
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

VERSION = "2.1.285"
HOME = Path.home()
ORIGEN = HOME / ".local" / "share" / "claude" / "versions" / VERSION
DESTINO = HOME / "ch-bin" / f"claude-{VERSION}.exe"
TRABAJO = Path(r"C:\w\p4")
SALIDA = Path(__file__).resolve().parent.parent / "piloto"
MENSAJE = "Reply with only: ok".encode("utf-8")


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main():
    if not ORIGEN.is_file():
        sys.exit(f"No existe {ORIGEN}")
    DESTINO.parent.mkdir(exist_ok=True)
    if not DESTINO.exists():
        shutil.copy2(ORIGEN, DESTINO)
    h_origen, h_copia = sha256(ORIGEN), sha256(DESTINO)
    print("sha256 origen:", h_origen)
    print("sha256 copia :", h_copia)
    if h_origen != h_copia:
        sys.exit("La copia no coincide con el original")

    TRABAJO.mkdir(parents=True, exist_ok=True)
    SALIDA.mkdir(exist_ok=True)
    env = dict(os.environ, DISABLE_AUTOUPDATER="1")

    ayuda = subprocess.run([str(DESTINO), "--help"], capture_output=True,
                           cwd=TRABAJO, env=env, timeout=120)
    (SALIDA / "claude-help.txt").write_bytes(ayuda.stdout + ayuda.stderr)

    base = [str(DESTINO), "-p", "--safe-mode", "--tools", "",
            "--no-session-persistence", "--output-format", "stream-json",
            "--verbose", "--model", "opus"]
    for nombre, extra in [("claude-a", []), ("claude-b", ["--system-prompt", ""])]:
        r = subprocess.run(base + extra, input=MENSAJE, capture_output=True,
                           cwd=TRABAJO, env=env, timeout=300)
        (SALIDA / f"{nombre}.jsonl").write_bytes(r.stdout)
        (SALIDA / f"{nombre}.stderr.txt").write_bytes(r.stderr)
        print(f"{nombre}: codigo {r.returncode}, {len(r.stdout)} bytes")
    print("Listo. Las salidas estan en", SALIDA)


if __name__ == "__main__":
    main()
