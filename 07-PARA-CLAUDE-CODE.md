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
   `python experimento\herramientas\prueba_offline.py` antes de gastar una
   llamada, y va en su propio commit, separado de las salidas y de los informes.
   Sin `-I` desde la v16: el validador de §5.3 usa `jsonschema`, que está en el
   site de usuario.
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

**Primera corrida del paso 1: FALLA** (`10-PRUEBA-SANDBOX-GENERADOR.md`): sin
modo de sandbox de Windows, `workspace-write` quedó en sólo lectura. Corregido en
la v8 con `-c windows.sandbox=unelevated`; el paso 1 se repite antes del 2.

**Hecho** (`11-PILOTO-GENERAR-Y-CHEQUEAR.md`): el paso 1 pasó, los 50 logs dejaron
sus dos archivos y los 50 pasan `chequear` (§4.2).

## La corrida (desde la v17)

El piloto terminó (`11` a `14`). La corrida real es `herramientas\corrida.py`, y
**no se corre antes de congelar el protocolo** (§0, paso 4: la tercera revisión).
Sus etapas, en orden, cada una con el OK de Nico si llama a un modelo: `logs`,
`gemelos`, `incluir`, `brazos`, `juez`, `validacion` y `analizar` (§0). Entre
`gemelos` e `incluir`, Nico anota sus decisiones en
`corrida\gemelos\decisiones.json`; entre `validacion` y `analizar`, sus etiquetas
en `corrida\validacion\etiquetas.json`. **Claude Code no lee las respuestas a los
brazos ni el informe antes que Nico.**

**Lo que agrega la v19** (tercera revisión, `16`):

- Cada gemelo lleva la casilla **C** (completitud), que decide siempre Nico; las
  decisiones valen sólo con los valores exactos («aprobada», «rechazada», «si»,
  «no»).
- Después de `incluir`, la lista, su md5 y `decisiones.json` se commitean, y el md5
  y el commit van en «Enmiendas»: `brazos` no corre si no están commiteados y sin
  cambios.
- El juez y la planilla de validación ven sólo los textos libres del JSON, con
  etiquetas opacas (§6.2); las etiquetas de Nico son booleanos JSON.

**Lo que agrega la v20** (cuarta revisión, `19`):

- `--objetivo` de `logs` nunca baja de 110: las tandas van con `--limite`.
- Después de `incluir`: commitear juntos la lista, su md5 y `decisiones.json`;
  anotar el md5 y ese commit en «Enmiendas»; commitear el protocolo y **pushear**.
  `brazos` y `juez` no corren con la lista commiteada más de una vez, con el md5
  fuera del protocolo commiteado, ni con cambios sin commitear en el protocolo,
  `herramientas\`, `prompts\` o `esquemas\`.
- Cada ítem guarda su historia después de cada intento. Un ítem cortado de golpe
  entre la llamada y el registro queda `interrumpido`, terminal: no se vuelve a
  llamar.

**Lo que agrega la v21** (quinta revisión, `21`):

- `brazos`, `juez`, `validacion` y `analizar` verifican el congelamiento.

**Lo que agrega la v22** (sexta revisión, `22`):

- En «Enmiendas» va un solo registro, con este formato exacto:
  `- Congelamiento de la lista: md5 <md5>, commit <commit entero>, árbol <md5>.`
  El árbol sale de `corrida.arbol_normativo()` sobre el commit de la lista.
- El commit tiene que estar en `origin/main` (se hace `fetch` en cada etapa) y
  `origin` no puede ser una ruta local: hace falta el remoto del experimento.
- Un cambio de código después de la primera llamada a los brazos descarta la
  corrida (§10.1): ninguna enmienda lo autoriza.

**Lo que agrega la v23** (séptima revisión, `23`):

- Antes de la primera llamada a los brazos, `origin/main` tiene que tener el
  commit de la lista y el HEAD con el registro: pushear después de commitear el
  registro. Después, sin red la corrida sigue con un aviso.
- No actualizar Codex mientras corren `logs` o `brazos`; después no importa.
- Los JSON que edita Nico se pueden guardar con BOM; en UTF-16, no.

## Estado y siguiente (15/10/2026)

**La fase 1 terminó el 14/10/2026.** El protocolo quedó congelado el 13/10, en la
v23 (tag `protocolo-congelado`). La corrida: `logs` (`24`), `gemelos` (`25`), la
lista de 100 pares (`238c1df`, con su registro en «Enmiendas» en `7d02634`),
`brazos` (`26`), `juez`, `validacion` y `analizar`. El resultado está en `27`, y
los informes en `28` (lista del W3C, en inglés), `29` (disensor) y `30` (autores
del paper, en inglés). El repo es público,
`github.com/NicolasRocchia/disensor-hide-pending`, con un README en inglés.

**Una corrección posterior al resultado:** de las 71 ausencias falsas, las 71
cumplen el esquema pero 69 pasan las cuatro reglas; las de `002` y `081` caen por
R1, no por la ausencia. Está corregido en `29` (`6b989b7`) y en los issues #134 y
#137 de disensor, y el cruce se rehace con `cruces/ausencias_y_reglas.py`.

**El árbol de la fase 1 no se toca.** `corrida.py analizar` vuelve a verificar
que `herramientas/`, `prompts/` y `esquemas/` sean el árbol del registro de
«Enmiendas». Un cambio ahí hace que un clon nuevo deje de reproducir el análisis.
Lo nuevo va en otra carpeta (como `cruces/`) o en otra rama; si algún día hace
falta tocar ese árbol, antes hay que fijar con un tag el commit que reproduce la
fase 1 y cambiar las instrucciones del README y de `28` para que lo usen.

**Lo que queda:**

- Las respuestas de la lista del W3C y de los autores del paper, a los mails del
  14/10.
- En disensor, los issues #134 a #139 que salieron del informe `29`.
- **La fase 2** (§13): si la prosa, no el JSON, dice más seguido que la consulta no
  volvió. Va con su propio protocolo, su revisión y su congelamiento. La prosa de
  las 400 llamadas de la fase 1 ya está guardada (`corrida/brazos/*/prosa.txt`);
  hacen falta los brazos A0 y A1, el juez del paper (Q.2.8) sobre la prosa y el de
  falsos positivos sobre los gemelos. Si compara contra A2, o vuelve a correr A2
  intercalado en su propia ventana, o declara la confusión por fecha.
- **El método entero** (#139 de disensor): sobre los mismos 100 pares, un
  generador declara el residuo, un revisor de otra familia lo ataca, y se mide
  cuántos falsos cierres sobreviven a la ronda.
