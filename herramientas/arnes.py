"""Arnés del experimento: lo común a todas las etapas (protocolo v5, §7).

Sólo biblioteca estándar. Corre en la máquina de Nico, con Windows, desde una
terminal común. Todo mensaje viaja como bytes UTF-8 (§7.3), cada llamada trabaja
en una carpeta nueva con nombre al azar (§7, «Rutas neutras») y los binarios se
verifican por sha256 y versión antes de cada llamada (§7.4).
"""
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

EXPERIMENTO = Path(__file__).resolve().parent.parent
PILOTO = EXPERIMENTO / "piloto"
HOME = Path.home()

CODEX_HOME = HOME / "ch"
CODEX_PAQUETE = Path(os.environ.get("APPDATA", "")) / "npm" / "node_modules" / "@openai" / "codex"
CODEX_VERSION = "codex-cli 0.153.4"
MODELO_GPT = "gpt-5.6-sol"
ESFUERZO_GPT = "low"

CLAUDE_EXE = HOME / "ch-bin" / "claude-2.1.285.exe"
CLAUDE_VERSION = "2.1.285"
MODELO_CLAUDE = "claude-opus-5-5"
ESFUERZO_CLAUDE = "high"

RAIZ_TRABAJO = Path(r"C:\w")

# §7.6, punto 2: nada de esto puede aparecer en el contexto fuera de nuestro mensaje.
PROHIBIDAS = [
    re.compile(r"disensor", re.I),
    re.compile(r"residuo", re.I),
    re.compile(r"residue", re.I),
    re.compile(r"red-team", re.I),
    re.compile(r"experimento", re.I),
    re.compile(r"Dev solo"),
    re.compile(r"\bNico\b"),
    re.compile(r"\bRocchia\b"),
]


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def md5_bytes(datos):
    return hashlib.md5(datos).hexdigest()


def ahora():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def encontrar_codex_exe():
    """El codex.exe que arranca el lanzador de npm, por ruta absoluta (§7.1)."""
    candidatos = set()
    for base in [CODEX_PAQUETE, CODEX_PAQUETE.parent / "codex-win32-x64"]:
        if base.is_dir():
            for p in base.rglob("codex.exe"):
                if "vendor" in p.parts:
                    candidatos.add(p.resolve())
    if len(candidatos) != 1:
        sys.exit(f"Se esperaba un solo codex.exe bajo {CODEX_PAQUETE}, hay {len(candidatos)}: {sorted(candidatos)}")
    return candidatos.pop()


# Variables que no pasan a ningún modelo: las de una sesión de Claude Code o de
# Codex desde la que se lance el arnés, y claves de API que cambiarían la cuenta
# con que corre cada CLI. Se sacan por prefijo; los nombres sacados se registran.
PREFIJOS_FUERA = ("CLAUDE", "ANTHROPIC_", "CODEX_", "OPENAI_", "OTEL_")


def entorno_base():
    """Copia del entorno sin las variables de PREFIJOS_FUERA."""
    return {k: v for k, v in os.environ.items() if not k.upper().startswith(PREFIJOS_FUERA)}


def variables_sacadas():
    return sorted(k for k in os.environ if k.upper().startswith(PREFIJOS_FUERA))


def entorno_codex():
    """El entorno que arma bin/codex.js antes de arrancar el binario, más el home aislado."""
    env = entorno_base()
    env["CODEX_MANAGED_PACKAGE_ROOT"] = str(CODEX_PAQUETE.resolve())
    env["CODEX_MANAGED_BY_NPM"] = "1"
    env["CODEX_HOME"] = str(CODEX_HOME)
    return env


def entorno_claude():
    return dict(entorno_base(), DISABLE_AUTOUPDATER="1")


def carpeta_trabajo():
    """Carpeta nueva y vacía, con nombre al azar del mismo patrón para todas."""
    RAIZ_TRABAJO.mkdir(exist_ok=True)
    while True:
        c = RAIZ_TRABAJO / secrets.token_hex(6)
        if not c.exists():
            c.mkdir()
            return c


def soltar_carpeta(c):
    """Borra la carpeta de trabajo sólo si quedó vacía; si no, la deja para revisar."""
    try:
        c.rmdir()
        return True
    except OSError:
        return False


def correr(comando, mensaje=None, cwd=None, env=None, timeout=1800):
    """Una llamada, con la entrada como bytes y la salida cruda."""
    inicio = ahora()
    t0 = time.monotonic()
    r = subprocess.run(comando, input=mensaje, capture_output=True, cwd=cwd, env=env, timeout=timeout)
    return {
        "inicio": inicio,
        "duracion_s": round(time.monotonic() - t0, 3),
        "codigo": r.returncode,
        "stdout": r.stdout,
        "stderr": r.stderr,
    }


def verificar_binarios(registro):
    """§7.4: sha256 y versión de los dos binarios; la primera vez quedan fijados en `registro`."""
    codex = encontrar_codex_exe()
    v_codex = correr([str(codex), "--version"], env=entorno_codex(), timeout=120)["stdout"].decode("utf-8").strip()
    if not CLAUDE_EXE.is_file():
        sys.exit(f"No existe {CLAUDE_EXE}: corré primero herramientas/prueba_claude.py")
    v_claude = correr([str(CLAUDE_EXE), "--version"], env=entorno_claude(), timeout=120)["stdout"].decode("utf-8").strip()
    actual = {
        "codex_exe": str(codex),
        "codex_sha256": sha256(codex),
        "codex_version": v_codex,
        "claude_exe": str(CLAUDE_EXE),
        "claude_sha256": sha256(CLAUDE_EXE),
        "claude_version": v_claude,
    }
    print("variables de entorno que no pasan a los modelos:", ", ".join(variables_sacadas()) or "ninguna")
    if v_codex != CODEX_VERSION:
        sys.exit(f"Codex es {v_codex!r}, se esperaba {CODEX_VERSION!r}")
    if not v_claude.startswith(CLAUDE_VERSION):
        sys.exit(f"Claude Code es {v_claude!r}, se esperaba {CLAUDE_VERSION}")
    if registro.exists():
        fijado = json.loads(registro.read_bytes().decode("utf-8"))
        for k in ["codex_exe", "codex_sha256", "codex_version", "claude_sha256", "claude_version"]:
            if fijado[k] != actual[k]:
                sys.exit(f"Cambió {k}: {fijado[k]!r} -> {actual[k]!r}. El arnés para (§7.4).")
    else:
        registro.parent.mkdir(parents=True, exist_ok=True)
        registro.write_bytes(json.dumps(actual, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
    return actual


def prohibidas_en(texto):
    return sorted({p.pattern for p in PROHIBIDAS if p.search(texto)})


def comando_codex_exec(codex_exe, salida_ultimo_mensaje):
    """La llamada de §7.1, igual para generador, capacidad y brazos. El mensaje va por stdin."""
    return [str(codex_exe), "exec", "-m", MODELO_GPT, "-s", "read-only", "--ephemeral",
            "--ignore-user-config", "--ignore-rules",
            "-c", "project_doc_max_bytes=0",
            "-c", f"model_reasoning_effort={ESFUERZO_GPT}",
            "-c", "skills.include_instructions=false",
            "--skip-git-repo-check", "--json", "-o", str(salida_ultimo_mensaje)]


def revisar_eventos(jsonl_bytes):
    """§7.1, red de seguridad: qué hizo el agente además de contestar.

    Un comando cuenta como ejecutado si terminó `completed` o tiene código de salida;
    un cambio de archivo, si terminó `completed`. Lo demás son intentos rechazados.
    """
    r = {"comandos_ejecutados": [], "comandos_rechazados": [], "archivos_cambiados": [],
         "cambios_rechazados": [], "otras_acciones": [], "mensajes_agente": 0,
         "uso": None, "turno_fallido": None, "errores": [], "lineas_ilegibles": 0}
    for linea in jsonl_bytes.splitlines():
        if not linea.strip():
            continue
        try:
            e = json.loads(linea.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            r["lineas_ilegibles"] += 1
            continue
        t = e.get("type")
        if t == "turn.completed":
            r["uso"] = e.get("usage")
        elif t == "turn.failed":
            r["turno_fallido"] = (e.get("error") or {}).get("message")
        elif t == "error":
            r["errores"].append(e.get("message"))
        elif t == "item.completed":
            it = e.get("item") or {}
            tipo = it.get("type")
            if tipo == "agent_message":
                r["mensajes_agente"] += 1
            elif tipo == "command_execution":
                if it.get("status") == "completed" or it.get("exit_code") is not None:
                    r["comandos_ejecutados"].append(it.get("command"))
                else:
                    r["comandos_rechazados"].append(it.get("command"))
            elif tipo == "file_change":
                rutas = [c.get("path") for c in it.get("changes") or []]
                (r["archivos_cambiados"] if it.get("status") == "completed" else r["cambios_rechazados"]).extend(rutas)
            elif tipo in ("mcp_tool_call", "collab_tool_call", "web_search"):
                r["otras_acciones"].append(tipo)
    return r
