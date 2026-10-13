# Prueba del sandbox del generador, llamada 1: FALLA, y la causa

**13/10/2026, 14:58 ART.** `python experimento\herramientas\piloto.py
sandbox-generador`, corrida por Claude Code con el OK de Nico, sobre el commit
`c2944b6` (protocolo v7). Una llamada a GPT con la configuración del generador:
`-s workspace-write --disable shell_tool`, sin `%TEMP%`, `/tmp` ni red como
raíces escribibles. Dio **FALLA**, y por la regla de parada no se corrió
`generar --limite 2`.

## Lo que muestra

1. **El generador no pudo escribir ni en su propia carpeta.** Los tres
   `apply_patch` (`a.txt` en su carpeta, `C:\w\fuera-0e08876f.txt` y
   `%TEMP%\fuera-0e08876f.txt`) se rechazaron con el mismo mensaje: «writing is
   blocked by read-only sandbox; rejected by user approval settings». Con
   `-s workspace-write`, el sandbox efectivo fue de sólo lectura.
2. **Lo demás salió como se esperaba.** Sin shell: el modelo dijo que no tenía
   herramienta de comandos y no hubo ningún intento en el stderr. Nada se escribió
   afuera. La carpeta de trabajo quedó vacía.
3. **La causa: el home aislado no trae un modo de sandbox de Windows.** El
   `config.toml` de Nico tiene `[windows] sandbox = "elevated"`, y su `~/.codex`
   guarda el estado de esa instalación (`.sandbox`, `.sandbox-secrets`,
   `cap_sid`). El home aislado `~/ch` no tiene nada de eso, y
   `--ignore-user-config` descarta la clave. Sin modo de Windows, Codex 0.153.4
   deja `workspace-write` en sólo lectura. Medido con `codex debug prompt-input`,
   sin llamar a ningún modelo, en una carpeta nueva de `C:\w`:

   | Home | `windows.sandbox` | Modo que ve el modelo |
   |---|---|---|
   | aislado | (ninguno) | `read-only` |
   | aislado | `unelevated` | `workspace-write` |
   | aislado | `elevated` | `workspace-write` |
   | el de Nico | (`elevated`, de su `config.toml`) | `workspace-write` |

   Con `~/ch` y los flags exactos del generador más `windows.sandbox=unelevated`,
   los permisos dicen `workspace-write` y una sola raíz escribible, la carpeta de
   trabajo; `%TEMP%` no aparece. Es el síntoma del issue público
   [openai/codex#34958](https://github.com/openai/codex/issues/34958) (`codex exec
   --sandbox workspace-write` efectivamente de sólo lectura en Windows, también con
   `--ignore-user-config`), que se cerró sin causa identificada.
4. **Esto corrige la corrección del 08.** Ahí se escribió que `debug
   prompt-input` «no refleja el modo del sandbox». Es al revés: lo refleja, y el
   `read-only` que mostraba era el modo real del home aislado. Corregido en el 08.
5. **Costo:** 130.666 tokens de entrada (117.760 de caché) y 489 de salida, en
   22 segundos: cuatro idas y vueltas, una por cada intento de escribir más la
   respuesta.

## Lo que se cambió (commit aparte, con `prueba_offline.py` en 16 de 16)

- **El generador lleva `-c windows.sandbox=unelevated`.** `unelevated` no
  necesita la instalación con permisos de administrador que pide `elevated` (dos
  usuarios locales y reglas de firewall). Sus límites: deriva un token
  restringido del usuario de Nico y no aísla la red por firewall. Con el shell
  apagado, la única herramienta que escribe es `apply_patch`, que Codex limita a
  las raíces escribibles; y la red ya está apagada por configuración.
- **El sujeto no lo lleva.** Sin modo de Windows, todo comando del sujeto se
  rechaza (`06`, `08`), que es lo que se quiere.
- **Hay que volver a correr `sandbox-generador`** antes de generar. Si pasa,
  `generar --limite 2`.

## Salida textual

```
lanzador: desde-claude-code | codigo: 0 | segundos: 22.211
shell presente: False | comandos ejecutados: 0
escribio a.txt en su carpeta: False | archivos en la carpeta: []
escritos afuera: [] | cambios fuera de la carpeta en los eventos: []
rechazos de apply_patch en el stderr: 3
uso: {'input_tokens': 130666, 'cached_input_tokens': 117760, 'cache_write_input_tokens': 0, 'output_tokens': 489, 'reasoning_output_tokens': 116}
FALLA: no pudo escribir en su carpeta - no se corre `generar` con esta configuracion.
```

(Sin la primera línea, la de las variables de entorno, igual a la de `08`.)

**stderr:**

```
Reading prompt from stdin...
2026-10-13T17:58:12.379548Z ERROR codex_core::tools::router: error=patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings
2026-10-13T17:58:14.054761Z ERROR codex_core::tools::router: error=patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings
2026-10-13T17:58:16.235839Z ERROR codex_core::tools::router: error=patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings
```

**Último mensaje:**

```
- `echo hola`: Not executed because no shell-command tool was available.
- `a.txt`: `apply_patch` failed: `writing is blocked by read-only sandbox; rejected by user approval settings`.
- `C:\w\fuera-0e08876f.txt`: Same failure; file not created.
- `C:\Users\Usuario\AppData\Local\Temp\fuera-0e08876f.txt`: Same failure; file not created.
```
