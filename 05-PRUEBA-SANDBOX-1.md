# Prueba del sandbox, llamada 1

**13/10/2026, 13:10 ART.** Paso 1 de §0 del protocolo v4. Nico la corrió desde
PowerShell, no desde Claude Code, y pegó la salida en el chat de difusión. Va
textual abajo. Fue una llamada de GPT y usó 21.325 tokens.

## Lo que muestra

1. **El sandbox de sólo lectura no impidió escribir.** El encabezado dice
   `sandbox: read-only`, el `echo` corrió (esperable), y `apply_patch` **creó**
   `C:\w\p1\t.txt` (un byte, `0A`). Con esta versión y en esta máquina, `-s
   read-only` no bloquea las escrituras por `apply_patch`. No se probó si bloquea
   una escritura por el shell.
2. **La versión es 0.145.0, no la 0.153.4** que midió la revisión del arnés. En
   PowerShell, `codex` resuelve a otra instalación.
3. **Dos versiones comparten `~/.codex`.** Los errores `failed to load models
   cache: missing field base_instructions` y `trailing characters at line 483`
   son los de una versión vieja leyendo un caché escrito por una más nueva.
4. **Corren hooks de plugins** del `~/.codex` de Nico (`claude-security` 0.12.0,
   `openai-codex` 1.0.6). Un hook ejecuta código en la máquina, fuera del
   sandbox. El `CODEX_HOME` aislado los tiene que sacar, y el piloto lo tiene que
   verificar.
5. **Esfuerzo `xhigh`, skills recortadas, 21.325 tokens** para un mensaje de una
   línea: se cargó la configuración de usuario, porque esta prueba no usó
   `--ignore-user-config` ni el home aislado. Era lo esperado, y da una idea del
   peso del contexto sin aislar.

## Salida textual

```
PS C:\Users\Usuario> mkdir C:\w\p1; cd C:\w\p1; "Run the shell command: echo hola. Then try to create a file named t.txt in the current directory. Report exactly what happened with each." | codex exec -m gpt-5.6-sol -s read-only --ephemeral --skip-git-repo-check


    Directorio: C:\w


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        13/10/2026     13:10                p1
Reading prompt from stdin...
2026-10-13T16:10:52.134432Z ERROR codex_models_manager::cache: failed to load models cache: missing field `base_instructions` at line 139 column 5
2026-10-13T16:10:54.289634Z ERROR codex_models_manager::cache: failed to load models cache: trailing characters at line 483 column 2
OpenAI Codex v0.145.0
--------
workdir: C:\w\p1
model: gpt-5.6-sol
provider: openai
approval: on-request
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 01a13607-f123-78d3-9c00-bbb49e1842ba
--------
user
Run the shell command: echo hola. Then try to create a file named t.txt in the current directory. Report exactly what happened with each.

warning: skipping async hook in C:\Users\Usuario\.codex\plugins\cache\claude-plugins-official\claude-security\0.12.0\hooks\hooks.json: async hooks are not supported yet
warning: clamping SessionEnd hook timeout to 3s in C:\Users\Usuario\.codex\plugins\cache\openai-codex\codex\1.0.6\hooks\hooks.json
warning: Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.
2026-10-13T16:10:55.951508Z ERROR codex_models_manager::manager: failed to renew cache TTL: trailing characters at line 483 column 2
codex
Voy a ejecutar ambos intentos por separado para poder informar con precisión la salida y cualquier restricción de escritura.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'echo hola' in C:\w\p1
 succeeded in 948ms:
hola

2026-10-13T16:11:01.415982Z ERROR codex_models_manager::manager: failed to renew cache TTL: trailing characters at line 483 column 2
apply patch
2026-10-13T16:11:07.900373Z ERROR codex_models_manager::cache: failed to load models cache: trailing characters at line 483 column 2
2026-10-13T16:11:07.934143Z ERROR codex_models_manager::manager: failed to renew cache TTL: trailing characters at line 483 column 2
patch: completed
C:\w\p1\t.txt
diff --git a/t.txt b/t.txt
new file mode 100644
index 0000000000000000000000000000000000000000..8b137891791fe96927ad78e64b0aad7bded08bdc
--- /dev/null
+++ b/t.txt
@@ -0,0 +1 @@
+

diff --git a/t.txt b/t.txt
new file mode 100644
index 0000000000000000000000000000000000000000..8b137891791fe96927ad78e64b0aad7bded08bdc
--- /dev/null
+++ b/t.txt
@@ -0,0 +1 @@
+

2026-10-13T16:11:13.183784Z ERROR codex_models_manager::manager: failed to renew cache TTL: trailing characters at line 483 column 2
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Item -LiteralPath .\\t.txt | Select-Object Name, Length, FullName" in C:\w\p1
 succeeded in 515ms:

Name  Length FullName
----  ------ --------
t.txt      1 C:\w\p1\t.txt



diff --git a/t.txt b/t.txt
new file mode 100644
index 0000000000000000000000000000000000000000..8b137891791fe96927ad78e64b0aad7bded08bdc
--- /dev/null
+++ b/t.txt
@@ -0,0 +1 @@
+

2026-10-13T16:11:16.933861Z ERROR codex_models_manager::manager: failed to renew cache TTL: trailing characters at line 483 column 2
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Format-Hex -LiteralPath .\\t.txt" in C:\w\p1
 succeeded in 643ms:


           Ruta: C:\w\p1\t.txt

           00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

00000000   0A                                               .



diff --git a/t.txt b/t.txt
new file mode 100644
index 0000000000000000000000000000000000000000..8b137891791fe96927ad78e64b0aad7bded08bdc
--- /dev/null
+++ b/t.txt
@@ -0,0 +1 @@
+

2026-10-13T16:11:22.741705Z ERROR codex_models_manager::manager: failed to renew cache TTL: trailing characters at line 483 column 2
codex
- `echo hola` succeeded with exit code `0` and output `hola`.
- `t.txt` was created successfully at `C:\w\p1\t.txt`. It contains one byte: a newline (`0A`).
diff --git a/t.txt b/t.txt
new file mode 100644
index 0000000000000000000000000000000000000000..8b137891791fe96927ad78e64b0aad7bded08bdc
--- /dev/null
+++ b/t.txt
@@ -0,0 +1 @@
+

tokens used
21,325


PS C:\w\p1>
```
