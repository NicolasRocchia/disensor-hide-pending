# Para Claude Code: correr el piloto

**Qué es.** El experimento de disensor sobre el escenario Hide Pending Tool Call.
El protocolo es `01-PROTOCOLO.md` (v7, no congelado); el arnés está en
`herramientas/` (`arnes.py`, `generador.py`, `piloto.py`, `prueba_offline.py`).
**Desde el 13/10/2026 (protocolo v7), Claude Code escribe y corre el arnés**, por
decisión de Nico: la sesión de difusión lo escribía sin poder ejecutarlo, y cada
error aparecía recién al correrlo. La regla 1 de abajo era la anterior y queda
tachada.

## Reglas

1. ~~**No cambies prompts, esquemas, umbrales ni el protocolo, y no edites los
   scripts de `herramientas/`.** Si algo falla, informá el error, la causa
   probable y el cambio que propondrías. Nico decide, y el cambio lo aplica la
   sesión de difusión, para que los scripts tengan un solo autor.~~
   **Desde la v7:** Claude Code escribe los scripts de `herramientas/` y mantiene
   al día las secciones del protocolo que describen el arnés (§7, §14, §15). Los
   prompts, los esquemas y los umbrales no cambian sin una decisión de Nico, y
   después de congelar sólo por «Enmiendas». Cada cambio a `herramientas/` pasa
   `python -I experimento\herramientas\prueba_offline.py` antes de gastar una
   llamada, y va en su propio commit, separado de las salidas y de los informes.
2. **De a una etapa, en orden, y parás en la primera que falle.**
3. **Cada etapa que llame a un modelo necesita el OK de Nico.** Las dos de abajo
   ya lo tienen: `sandbox` hace una sola llamada a GPT y `contexto` no llama a
   ninguno.
4. **No leas ni resumas lo que el sujeto contesta a los brazos.** La prueba de
   humo, cuando llegue, sólo verifica el arnés y no se juzga (§7.6).
5. **Ninguna credencial pasa por vos:** las dos CLI usan las sesiones de Nico.
   El arnés le saca al entorno de cada llamada las variables que empiezan con
   `CLAUDE`, `ANTHROPIC_`, `CODEX_`, `OPENAI_` y `OTEL_`, y pone las suyas.

## Ahora

1. **`python experimento\herramientas\piloto.py sandbox`**, desde
   `D:\Programacion\Disensor-Docs`. Prueba el sandbox de Codex **con vos como
   proceso padre**: el `AGENTS.md` de Nico dice que `-s read-only` falla desde
   Claude Code, y la receta de disensor lo advierte. Desde una terminal común
   rechazó todo (`06-PRUEBA-SANDBOX-2.md`). **Si imprime FALLA, parás:** las
   etapas que llaman al sujeto se corren entonces desde una terminal común.
2. Si pasó: **`python experimento\herramientas\piloto.py contexto`**. No llama a
   ningún modelo.
3. **Informá a Nico:** lo que imprimió cada etapa, y qué archivos quedaron en
   `experimento\piloto\arnes\`. Con eso, la sesión de difusión escribe la etapa
   siguiente.

## Siguiente: `generar` (13/10/2026)

Aplicados los cambios 1 y 2 de `08-PRUEBA-SANDBOX-3-Y-CONTEXTO.md`, que Nico
aprobó:

- **`arnes.revisar_stderr`** cuenta en el stderr los rechazos del sandbox, una
  línea por intento: shell (`rejected: blocked by policy`), `apply_patch`
  (`error=patch rejected`) y otros errores de herramienta. Probado contra el
  stderr real de 08: 3 de shell (el `echo` y dos de `a.txt`) y 2 de
  `apply_patch`.
- **La etapa `sandbox`** da OK sólo si ve en el stderr los tres intentos (el
  `echo`, la escritura de `a.txt` por shell y un `apply_patch`). Si falta
  alguno, imprime INCONCLUSO y sale con código 2. No hace falta volver a
  correrla: la lógica nueva se probó contra la salida guardada.

**El paso que sigue, con el OK de Nico: `python experimento\herramientas\piloto.py generar`.**
Son las 50 llamadas del generador del piloto (§4.5, punto 1): semilla 20261012,
10 por cada comportamiento de falla.

- **Conviene empezar con `--limite 2`**, mirar lo que imprime y los dos
  `piloto\generador\00N\resumen.json`, y recién después correr el resto. La
  etapa es reanudable: saltea las que ya terminaron, sean `ok` o `fallo` (tres
  intentos sin terminar). Cada llamada puede tardar minutos; si las 48 restantes
  no entran en el tiempo de tu Bash, corrélas en segundo plano o por tandas con
  `--limite`.
- **Para sola** por la red de seguridad de §7.1 (un comando ejecutado, un archivo
  cambiado o la carpeta de trabajo no vacía) y por falta de cupo. Si para por la
  red de seguridad, no la vuelvas a correr: queda trabada hasta que Nico revise.
  Si para por cupo, se retoma más tarde con el mismo comando.
- **Qué informar:** la línea por llamada y el resumen final (estados, promedio de
  tokens y segundos, rechazos de shell y de `apply_patch`). Los rechazos de
  `apply_patch` dicen cuántas veces el generador intentó escribir sus dos
  archivos en vez de imprimirlos, que es lo que decide su sandbox (§4.1, §7.1).
- **Los logs generados no son respuestas a los brazos:** podés abrir uno para
  confirmar el formato. La extracción y los chequeos de §4.2 son la etapa
  siguiente, que todavía no está escrita.

**Resultado** (`09-PILOTO-GENERAR-1.md`): con sólo lectura, el generador no
produjo ningún log. Dispara la contingencia de §7.1.

## Siguiente, con la v7: el generador con `workspace-write` (13/10/2026)

Las dos llamadas con sólo lectura quedaron en `piloto/generador-solo-lectura/`.
Con el OK de Nico, en este orden y parando en la primera que falle:

1. **`python experimento\herramientas\piloto.py sandbox-generador`**: una
   llamada. Comprueba que el generador escribe en su carpeta, no tiene shell y no
   puede escribir en `C:\w` ni en `%TEMP%`. Si da FALLA o INCONCLUSO, no se
   genera.
2. **`python experimento\herramientas\piloto.py generar --limite 2`**: los logs
   `000` y `001` otra vez, ahora con la configuración del generador. Informar el
   estado de cada uno (`archivos`, `mensaje`, `sin_log` o `fallo`) y abrir un log
   para confirmar el formato.
3. Si los dos dan `archivos` o `mensaje`, las 48 restantes, en segundo plano y
   con su propio OK.
