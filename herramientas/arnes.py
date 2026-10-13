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


def verificar_binarios(registro, necesarios=("codex", "claude")):
    """§7.4: sha256 y versión de los binarios que usa la etapa; la primera vez quedan fijados
    los dos en `registro`. Desde la v23 (hallazgo 3 de la séptima revisión), una etapa que sólo
    llama a Claude no exige Codex, y al revés: actualizar Codex después de los brazos no frena
    al juez."""
    if not registro.exists():
        necesarios = ("codex", "claude")
    actual = {}
    if "codex" in necesarios:
        codex = encontrar_codex_exe()
        v_codex = correr([str(codex), "--version"], env=entorno_codex(), timeout=120)["stdout"].decode("utf-8").strip()
        if v_codex != CODEX_VERSION:
            sys.exit(f"Codex es {v_codex!r}, se esperaba {CODEX_VERSION!r}")
        actual.update(codex_exe=str(codex), codex_sha256=sha256(codex), codex_version=v_codex)
    if "claude" in necesarios:
        if not CLAUDE_EXE.is_file():
            sys.exit(f"No existe {CLAUDE_EXE}: corré primero herramientas/prueba_claude.py")
        v_claude = correr([str(CLAUDE_EXE), "--version"], env=entorno_claude(), timeout=120)["stdout"].decode("utf-8").strip()
        if not v_claude.startswith(CLAUDE_VERSION):
            sys.exit(f"Claude Code es {v_claude!r}, se esperaba {CLAUDE_VERSION}")
        actual.update(claude_exe=str(CLAUDE_EXE), claude_sha256=sha256(CLAUDE_EXE), claude_version=v_claude)
    print("variables de entorno que no pasan a los modelos:", ", ".join(variables_sacadas()) or "ninguna")
    if not registro.exists():
        registro.parent.mkdir(parents=True, exist_ok=True)
        registro.write_bytes(json.dumps(actual, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
        return actual
    fijado = json.loads(registro.read_bytes().decode("utf-8"))
    for k, v in actual.items():
        if k != "claude_exe" and fijado[k] != v:
            sys.exit(f"Cambió {k}: {fijado[k]!r} -> {v!r}. El arnés para (§7.4).")
    return {**fijado, **actual}


def prohibidas_en(texto):
    return sorted({p.pattern for p in PROHIBIDAS if p.search(texto)})


def comando_codex_exec(codex_exe, salida_ultimo_mensaje, generador=False, efimero=True):
    """La llamada de §7.1. El mensaje va por stdin.

    Capacidad y brazos corren con sandbox de sólo lectura. El generador, por la
    contingencia de §7.1 (09-PILOTO-GENERAR-1.md), tiene que poder escribir sus dos
    archivos: `workspace-write` sólo sobre su carpeta de trabajo (sin %TEMP%, sin
    /tmp, sin red) y sin la herramienta de shell, así que la única forma de escribir
    es apply_patch y la red de seguridad sigue siendo «ningún comando ejecutado».

    `windows.sandbox=unelevated` hace falta: sin un modo de sandbox de Windows, que el
    home aislado no trae, Codex 0.153.4 deja `workspace-write` en sólo lectura
    (10-PRUEBA-SANDBOX-GENERADOR.md). `unelevated` no necesita la instalación con
    permisos de administrador que pide `elevated`. El sujeto no lo lleva: sin modo de
    Windows, todo comando se le rechaza, que es lo que se quiere.
    """
    if generador:
        sandbox = ["-s", "workspace-write", "--disable", "shell_tool",
                   "-c", "windows.sandbox=unelevated",
                   "-c", "sandbox_workspace_write.exclude_tmpdir_env_var=true",
                   "-c", "sandbox_workspace_write.exclude_slash_tmp=true",
                   "-c", "sandbox_workspace_write.network_access=false"]
    else:
        sandbox = ["-s", "read-only"]
    # `efimero=False` sólo para comprobar en el piloto los bytes que llegan por stdin
    # (§7.6, punto 8): sin --ephemeral, Codex guarda la sesión en CODEX_HOME/sessions.
    return [str(codex_exe), "exec", "-m", MODELO_GPT, *sandbox, *(["--ephemeral"] if efimero else []),
            "--ignore-user-config", "--ignore-rules",
            "-c", "project_doc_max_bytes=0",
            "-c", f"model_reasoning_effort={ESFUERZO_GPT}",
            "-c", "skills.include_instructions=false",
            "--skip-git-repo-check", "--json", "-o", str(salida_ultimo_mensaje)]


def comando_claude():
    """§7.2, igual para gemelos y juez. El mensaje va por stdin. `--tools ""` va como un
    elemento vacío de la lista: desde PowerShell o Git Bash se perdería."""
    return [str(CLAUDE_EXE), "-p", "--safe-mode", "--setting-sources", "project",
            "--tools", "", "--system-prompt", "", "--disable-slash-commands",
            "--effort", ESFUERZO_CLAUDE, "--no-session-persistence",
            "--output-format", "stream-json", "--verbose", "--model", MODELO_CLAUDE]


def revisar_stream_claude(stdout_bytes):
    """§7.2: lo que hay que verificar en cada llamada a Claude, del flujo `stream-json`."""
    r = {"init_tools": None, "modelo": None, "usos_de_herramienta": 0, "turnos": None,
         "subtipo": None, "es_error": None, "resultado": None, "uso": None, "costo_usd": None,
         "lineas_ilegibles": 0}
    for linea in stdout_bytes.splitlines():
        if not linea.strip():
            continue
        try:
            e = json.loads(linea.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            r["lineas_ilegibles"] += 1
            continue
        t = e.get("type")
        if t == "system" and e.get("subtype") == "init":
            r["init_tools"] = e.get("tools")
            r["modelo"] = e.get("model")
        elif t == "assistant":
            contenido = (e.get("message") or {}).get("content") or []
            r["usos_de_herramienta"] += sum(1 for c in contenido if c.get("type") in ("tool_use", "server_tool_use"))
        elif t == "result":
            r.update(turnos=e.get("num_turns"), subtipo=e.get("subtype"), es_error=e.get("is_error"),
                     resultado=e.get("result"), uso=e.get("usage"), costo_usd=e.get("total_cost_usd"))
    r["verificado"] = (r["init_tools"] == [] and r["modelo"] == MODELO_CLAUDE
                       and r["usos_de_herramienta"] == 0 and r["turnos"] == 1)
    return r


def revisar_eventos(jsonl_bytes):
    """§7.1, red de seguridad: qué hizo el agente además de contestar.

    Un comando cuenta como ejecutado si terminó `completed` o tiene código de salida;
    un cambio de archivo, si terminó `completed`. Con Codex 0.153.4 los intentos que
    el sandbox rechaza no aparecen en este flujo (08-PRUEBA-SANDBOX-3-Y-CONTEXTO.md,
    punto 3): se cuentan en el stderr, con `revisar_stderr`. Las claves
    `comandos_rechazados` y `cambios_rechazados` quedan por si otra versión los emite.
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


# Líneas del stderr de Codex 0.153.4 con los rechazos del sandbox (08, puntos 2 y 3).
RE_SHELL_RECHAZADO = re.compile(r"exec_command failed: .*rejected: blocked by policy")
RE_PARCHE_RECHAZADO = re.compile(r"error=patch rejected")
RE_ERROR_HERRAMIENTA = re.compile(r"codex_core::tools::router: error=")
# Señales de cupo agotado, para parar sin gastar reintentos (§7.7).
RE_SIN_CUPO = re.compile(r"usage limit|rate limit|quota|too many requests|\b429\b", re.I)


def sin_cupo(ev, stderr_bytes):
    """§7.7: la llamada falló por cupo.

    Mira el turno fallido, los eventos de error y las líneas del stderr, salvo las de
    herramientas rechazadas: ésas repiten el texto del comando, y un log que diga
    «429» o «quota» no es falta de cupo (09, pendientes de la revisión de b816af4).
    """
    textos = [str(ev.get("turno_fallido") or ""), *(str(e) for e in ev.get("errores") or [])]
    for linea in stderr_bytes.decode("utf-8", errors="replace").splitlines():
        if "codex_core::tools::router" not in linea:
            textos.append(linea)
    return any(RE_SIN_CUPO.search(t) for t in textos)


def revisar_stderr(stderr_bytes):
    """Los intentos rechazados por el sandbox, contados en el stderr, una línea por intento."""
    r = {"shell_rechazados": [], "parches_rechazados": [], "otros_errores_herramienta": []}
    for linea in stderr_bytes.decode("utf-8", errors="replace").splitlines():
        if RE_SHELL_RECHAZADO.search(linea):
            r["shell_rechazados"].append(linea)
        elif RE_PARCHE_RECHAZADO.search(linea):
            r["parches_rechazados"].append(linea)
        elif RE_ERROR_HERRAMIENTA.search(linea):
            r["otros_errores_herramienta"].append(linea)
    return r


def verificar_sha(fijado, cual):
    """§7.4, antes de cada llamada: el binario sigue siendo el fijado."""
    ruta = fijado[f"{cual}_exe"]
    if sha256(ruta) != fijado[f"{cual}_sha256"]:
        sys.exit(f"Cambió el sha256 de {ruta}. El arnés para (§7.4).")
