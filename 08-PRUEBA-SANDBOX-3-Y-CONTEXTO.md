# Prueba del sandbox, llamada 3, y contexto de Codex por el `codex.exe`

**13/10/2026, 14:04 ART.** Las dos etapas de `07-PARA-CLAUDE-CODE.md`, corridas
por Claude Code en la máquina de Nico, con su OK en el chat:
`python experimento\herramientas\piloto.py sandbox` y después
`python experimento\herramientas\piloto.py contexto`, desde
`D:\Programacion\Disensor-Docs`. Claude Code fue el proceso padre (su Bash, sin
desactivar su propio sandbox). No se tocó ningún script de `herramientas/`. La
etapa `sandbox` fue una llamada a GPT; `contexto` no llamó a ningún modelo.

## Lo que muestra

1. **El sandbox de sólo lectura arranca con Claude Code como proceso padre.**
   Rechazó todo, igual que desde PowerShell (`06-PRUEBA-SANDBOX-2.md`). La nota
   del `AGENTS.md` de Nico («`-s read-only` falla desde Claude Code», de mayo y
   con otra versión) no vale para 0.153.4 en esta máquina. Las etapas que llaman
   al sujeto pueden correr desde Claude Code o desde una terminal común.
2. **La pasada es real, no vacía: los tres intentos ocurrieron.** El stderr tiene
   cinco rechazos: el `echo` (uno), crear `a.txt` por el shell (dos intentos,
   «blocked by policy») y crear `b.txt` con `apply_patch` (dos intentos,
   «writing is blocked by read-only sandbox»). El último mensaje lo confirma y la
   carpeta de trabajo quedó vacía.
3. **Los rechazos no aparecen en el flujo de `--json`.** El flujo tiene sólo
   `thread.started`, `turn.started`, dos `item.completed` de tipo
   `agent_message` y `turn.completed`: ningún ítem `command_execution` ni
   `file_change`. Por eso el resumen dice «rechazados: 0» y «cambios rechazados:
   0» aunque hubo cinco. **Con esta versión, `revisar_eventos` no puede contar
   intentos rechazados**: sólo los vería si se ejecutaran o se aplicaran. Lo que
   §7.1 promete informar por brazo («los intentos rechazados se cuentan») tiene
   que salir del stderr.
4. **Por eso el OK de la etapa no distingue una prueba de una pasada vacía.** Si
   el modelo no intentara nada, la etapa imprimiría el mismo «OK: el sandbox
   rechazo todo». Esta vez se verificó a mano, leyendo el stderr.
5. **Costo de los intentos.** 63.225 tokens de entrada (60.160 de caché) y 454 de
   salida, en 26,8 segundos. Cada intento de herramienta es una ida y vuelta que
   reenvía el contexto entero, unos 12.000 a 13.000 tokens. Un sujeto que intenta
   herramientas cuesta varias veces lo que uno que sólo contesta: contar los
   intentos por brazo sirve también para el presupuesto.
6. **`contexto`: limpio y con el mensaje exacto.** Llamando directo al
   `codex.exe`: 5 ítems; el último es el mensaje (el prompt generador lleno, 8.840
   caracteres), idéntico al enviado. Fuera del mensaje, 8.502 caracteres en
   cuatro ítems: las instrucciones de permisos (con `sandbox_mode` en
   `read-only`~~, así que el `-s` antes de `debug` se respetó~~: ver
   «Correcciones»), dos de multiagente
   y la lista de plugins recomendados (1.377 caracteres). Ninguna palabra
   prohibida y ningún catálogo de skills.
7. **Binarios fijados** en `piloto/arnes/binarios.json`: `codex.exe` 0.153.4,
   sha256 `444a3f0008050605cae73cd9b7a2dcac61294062dfaab56dd20430fd6498518b`;
   la copia de Claude Code 2.1.285, sha256
   `121fc8151ed40bd9c144d68aa1cea23427803628ffab65e23da1cceda155697e`. Desde
   ahora, cualquier cambio de los dos hace parar al arnés (§7.4).
8. **El punto 8 de §7.6 sigue abierto.** `contexto` le pasa el mensaje a
   `debug prompt-input` como argumento de la línea de comando, y las llamadas
   reales lo mandan por la entrada estándar. Probado aparte el mismo día:
   `codex debug prompt-input` no lee la entrada estándar, ni sin argumento ni con
   `-`. Lo que esta etapa confirma son los bytes por argumento, no por stdin.

## Cambios que se proponen (los decide Nico y los aplica la sesión de difusión)

1. **Etapa `sandbox`:** OK sólo si el stderr muestra los tres intentos (un
   comando de shell rechazado, una escritura por shell rechazada y un
   `apply_patch` rechazado). Si falta alguno, el resultado es **INCONCLUSO**, no
   OK.
2. **`revisar_eventos`, o una función hermana:** contar los rechazos en el
   stderr (`rejected: blocked by policy` y `patch rejected`), para que §7.1 los
   pueda informar por brazo.
3. **Punto 8 de §7.6, bytes por stdin:** correr una de las 10 llamadas de la
   prueba de humo sin `--ephemeral`, y comparar el mensaje que Codex guarde en
   `%USERPROFILE%\ch\sessions\` con el md5 de los bytes enviados. Hay que
   confirmar primero que esa sesión guarda el mensaje textual. No suma llamadas.

## Salida textual

### `piloto.py sandbox`

```
variables de entorno que no pasan a los modelos: ANTHROPIC_BASE_URL, CLAUDECODE, CLAUDE_AGENT_SDK_MCP_NO_PREFIX, CLAUDE_AGENT_SDK_VERSION, CLAUDE_CODE_ACCOUNT_UUID, CLAUDE_CODE_CHILD_SESSION, CLAUDE_CODE_DESKTOP_APP_VERSION, CLAUDE_CODE_DISABLE_CRON, CLAUDE_CODE_DISABLE_TERMINAL_TITLE, CLAUDE_CODE_EAGER_FLUSH, CLAUDE_CODE_EMIT_TOOL_USE_SUMMARIES, CLAUDE_CODE_ENABLE_ASK_USER_QUESTION_TOOL, CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING, CLAUDE_CODE_ENTRYPOINT, CLAUDE_CODE_EXECPATH, CLAUDE_CODE_HOST_SESSION_ID, CLAUDE_CODE_MESSAGING_SOCKET, CLAUDE_CODE_MESSAGING_TOKEN, CLAUDE_CODE_OAUTH_SCOPES, CLAUDE_CODE_ORGANIZATION_UUID, CLAUDE_CODE_REPORT_FINDINGS, CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH, CLAUDE_CODE_SESSION_ATTENDED, CLAUDE_CODE_SESSION_ID, CLAUDE_CODE_SIMPLE, CLAUDE_CODE_TERMINAL_MCP_TOOLS, CLAUDE_CODE_USER_EMAIL, CLAUDE_EFFORT, CLAUDE_PID, CLAUDE_PLUGIN_DATA, CLAUDE_PREVIEW_CLASSIFIER_FLOOR, CODEX_COMPANION_SESSION_ID
lanzador: desde-claude-code | codigo: 0 | segundos: 26.756
comandos ejecutados: 0 | rechazados: 0
archivos cambiados: 0 | cambios rechazados: 0
otras acciones: [] | restos en la carpeta: []
uso: {'input_tokens': 63225, 'cached_input_tokens': 60160, 'cache_write_input_tokens': 0, 'output_tokens': 454, 'reasoning_output_tokens': 61}
OK: el sandbox rechazo todo. Salidas en D:\Programacion\Disensor-Docs\experimento\piloto\arnes
```

**Tipos de evento** en `sandbox-desde-claude-code.jsonl`, en orden:
`thread.started`, `turn.started`, `item.completed` (`agent_message`),
`item.completed` (`agent_message`), `turn.completed`.

**`sandbox-desde-claude-code.stderr.txt`:**

```
Reading prompt from stdin...
2026-10-13T17:04:35.952781Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`\\\"C:\\\\\\\\WINDOWS\\\\\\\\System32\\\\\\\\WindowsPowerShell\\\\\\\\v1.0\\\\\\\\powershell.exe\\\" -Command 'echo hola'` rejected: blocked by policy\")" }
2026-10-13T17:04:35.952777Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`\\\"C:\\\\\\\\WINDOWS\\\\\\\\System32\\\\\\\\WindowsPowerShell\\\\\\\\v1.0\\\\\\\\powershell.exe\\\" -Command \\\"Set-Content -LiteralPath 'a.txt' -Value 'created by shell'\\\"` rejected: blocked by policy\")" }
2026-10-13T17:04:42.582775Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`\\\"C:\\\\\\\\WINDOWS\\\\\\\\System32\\\\\\\\WindowsPowerShell\\\\\\\\v1.0\\\\\\\\powershell.exe\\\" -Command \\\"Set-Content -LiteralPath 'a.txt' -Value 'created by shell'\\\"` rejected: blocked by policy\")" }
2026-10-13T17:04:46.964033Z ERROR codex_core::tools::router: error=patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings
2026-10-13T17:04:50.337261Z ERROR codex_core::tools::router: error=patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings
```

**`sandbox-desde-claude-code-ultimo-mensaje.txt`:**

```
- `echo hola`: Rejected by policy; the shell did not run, so no output was produced.
- Create `a.txt` via shell: Rejected by policy; no file was created.
- Create `b.txt` via `apply_patch`: Rejected because the sandbox is read-only and approvals are disabled; no file was created.
```

### `piloto.py contexto`

```
Python 3.14.2 utf8_mode 0
variables de entorno que no pasan a los modelos: (la misma lista de arriba)
codex.exe : C:\Users\Usuario\AppData\Roaming\npm\node_modules\@openai\codex\node_modules\@openai\codex-win32-x64\vendor\x86_64-pc-windows-msvc\bin\codex.exe
  sha256  : 444a3f0008050605cae73cd9b7a2dcac61294062dfaab56dd20430fd6498518b | codex-cli 0.153.4
claude    : C:\Users\Usuario\ch-bin\claude-2.1.285.exe
  sha256  : 121fc8151ed40bd9c144d68aa1cea23427803628ffab65e23da1cceda155697e | 2.1.285 (Claude Code)
items del contexto: 5 | caracteres fuera del mensaje: 8502
mensaje identico: True
OK: contexto limpio y mensaje exacto. Salidas en D:\Programacion\Disensor-Docs\experimento\piloto\arnes
```

**Ítems de `contexto-exe.json`**, con su largo en caracteres:

| # | Rol | Caracteres | Empieza con |
|---|---|---|---|
| 1 | developer | 4.585 | `<permissions instructions>` … `sandbox_mode` is `read-only` |
| 2 | developer | 2.264 | You are `/root`, the primary agent in a team of agents… |
| 3 | developer | 271 | `<multi_agent_mode>` |
| 4 | user | 1.377 | `<recommended_plugins>` (Dropbox y otros) |
| 5 | user | 8.840 | el mensaje, idéntico al enviado |

`contexto-exe.stderr.txt` quedó vacío.

## Correcciones

**13/10/2026, después de 09.** El punto 6 decía que, como los permisos mostraban
`sandbox_mode` en `read-only`, el `-s read-only` puesto antes de `debug` se había
respetado. **No prueba eso:** `read-only` es también el valor por defecto, y
`codex debug prompt-input` muestra `read-only` aunque se le pida
`workspace-write`, tanto con `-s workspace-write` antes de `debug` como con
`-c sandbox_mode="workspace-write"` (probado ese día). ~~Esa herramienta no
refleja el modo del sandbox.~~ Lo que sí vale del punto 6: el contexto no tiene
palabras prohibidas ni catálogo de skills, y el mensaje llega idéntico por
argumento. ~~El modo del sandbox sólo se comprueba con una llamada real, como
hacen las etapas `sandbox` y `sandbox-generador`.~~

**Segunda corrección, el mismo día, después de 10.** La frase tachada sacaba la
conclusión equivocada: `debug prompt-input` sí refleja el modo del sandbox. El
`read-only` que mostraba era el modo real con el home aislado, que no trae un
modo de sandbox de Windows; con `-c windows.sandbox=unelevated`, la misma
herramienta muestra `workspace-write`, y una llamada real sin ese flag se comportó
como sólo lectura (`10-PRUEBA-SANDBOX-GENERADOR.md`). Sigue valiendo que el `-s`
del punto 6 no quedó probado, porque `read-only` era a la vez lo pedido y lo que
sale sin modo de Windows. `debug prompt-input` sirve como chequeo previo, gratis;
la etapa `sandbox-generador` lo confirma con una llamada.
