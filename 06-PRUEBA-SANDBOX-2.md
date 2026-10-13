# Prueba del sandbox, llamada 2

**13/10/2026, 13:19 ART.** Repite la llamada 1 (`05-PRUEBA-SANDBOX-1.md`) con el
binario y la configuración del experimento: Codex 0.153.4 por ruta absoluta
(`AppData\Roaming\npm\codex.cmd`, el que tiene registrado disensor), con
`--ignore-user-config --ignore-rules -c project_doc_max_bytes=0`. Nico la corrió
desde PowerShell y pegó la salida en el chat de difusión. Va textual abajo. Fue
una llamada de GPT y usó 10.193 tokens.

## Lo que muestra

1. **Con esta configuración, el sandbox bloquea todo.** El encabezado dice
   `approval: never` y `sandbox: read-only`. Los dos comandos de shell, incluido
   el `echo` que no escribe nada, se rechazaron «blocked by policy»: no corrió
   ninguno. `apply_patch` se rechazó: «writing is blocked by read-only sandbox».
   No se creó ningún archivo. El sujeto no puede ejecutar, ni escribir, ni leer el
   disco por el shell.
2. **La diferencia con la llamada 1** está en la versión (0.145.0 contra 0.153.4)
   y en la política de aprobación (`on-request`, que venía del `config.toml` de
   Nico, contra `never`). Con estos datos no se puede separar cuál de las dos
   explica que en la llamada 1 se escribiera. Para el experimento no hace falta:
   corre con esta configuración, y el piloto lo vuelve a comprobar con el
   `CODEX_HOME` aislado.
3. **«reasoning effort: none» no quiere decir sin razonamiento.** En el código
   de 0.153.4 (`codex-rs/exec/src/event_processor_with_human_output.rs`), el
   encabezado imprime «none» cuando la configuración no fija el esfuerzo. El
   pedido sale entonces con el `default_reasoning_level` del modelo
   (`codex-rs/core/src/client.rs`, `build_reasoning`), que viene del catálogo de
   modelos que Codex baja de OpenAI y guarda en caché con vencimiento
   (`codex-rs/models-manager/src/cache.rs`). **El esfuerzo por defecto no lo fija
   la versión de la CLI: lo fija ese catálogo, y puede cambiar sin que cambie
   nada en la máquina.** Por eso §7.1 tiene que fijarlo de forma explícita, al
   valor que tenga el catálogo para `gpt-5.6-sol` el día del piloto.

## Salida textual

```
PS C:\w\p1> mkdir C:\w\p2; cd C:\w\p2; "Run the shell command: echo hola. Then try to create a file named a.txt with a shell command. Then try to create a file named b.txt with apply_patch. Report exactly what happened with each." | & "C:\Users\Usuario\AppData\Roaming\npm\codex.cmd" exec -m gpt-5.6-sol -s read-only --ephemeral --ignore-user-config --ignore-rules -c project_doc_max_bytes=0 --skip-git-repo-check


    Directorio: C:\w


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        13/10/2026     13:19                p2
Reading prompt from stdin...
OpenAI Codex v0.153.4
--------
workdir: C:\w\p2
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 01a13610-1763-77c1-878b-49addfa5d489
--------
user
Run the shell command: echo hola. Then try to create a file named a.txt with a shell command. Then try to create a file named b.txt with apply_patch. Report exactly what happened with each.

codex
I’ll run the three requested operations separately so each result is attributable. The workspace is read-only, so I expect the write attempts may be blocked, but I’ll report their actual outputs.
2026-10-13T16:19:50.506377Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`\\\"C:\\\\\\\\WINDOWS\\\\\\\\System32\\\\\\\\WindowsPowerShell\\\\\\\\v1.0\\\\\\\\powershell.exe\\\" -Command 'echo hola'` rejected: blocked by policy\")" }
2026-10-13T16:19:52.397637Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`\\\"C:\\\\\\\\WINDOWS\\\\\\\\System32\\\\\\\\WindowsPowerShell\\\\\\\\v1.0\\\\\\\\powershell.exe\\\" -Command \\\"Set-Content -LiteralPath .\\\\\\\\a.txt -Value 'hola'\\\"` rejected: blocked by policy\")" }
2026-10-13T16:19:54.702535Z ERROR codex_core::tools::router: error=patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings
codex
- `echo hola`: did not run. PowerShell process creation was rejected as “blocked by policy”; no `hola` output.
- Shell creation of `a.txt` using `Set-Content`: did not run. Rejected as “blocked by policy”; `a.txt` was not created.
- Creation of `b.txt` using `apply_patch`: rejected because writing is blocked by the read-only sandbox and approval settings; `b.txt` was not created.
tokens used
10,193


PS C:\w\p2>
```
