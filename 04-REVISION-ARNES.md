# Revisión del arnés de la v3

**Procedencia.** Revisión hecha por Claude Code en la máquina de Nico, sobre
`01-PROTOCOLO.md` v3 (md5 `6cec27936bfea40c9c0215039c9e1c42`), el 13/10/2026.
Nico la pegó en el chat de difusión. Va textual; sólo se agregaron las marcas de
Markdown (títulos y viñetas). No se gastaron llamadas a modelos para hacerla.

---

Revisé 01-PROTOCOLO.md (la v3) y las dos revisiones independientes. La estadística y el diseño ya los trabajaron bien esas dos rondas. Lo que nadie revisó es el arnés de la v3 (§7), porque los revisores no tenían tu máquina. Lo verifiqué acá, sin gastar llamadas a ningún modelo, y aparecieron dos bloqueantes.

## Bloqueantes

### 1. Tu AGENTS.md global le llega al sujeto, y habla de disensor y del residuo.

Lo medí con codex debug prompt-input (codex-cli 0.153.4), desde una carpeta vacía y con -c project_doc_max_bytes=0.

- El contexto del modelo trae “disensor” 6 veces, “residuo” 7 y “red-team” 3, más tus preferencias. Ahí está la sección que describe la herramienta y la declaración de residuo.
- --ignore-user-config no lo saca: es el agujero de #108.

Consecuencia: A2 deja de probar “el esquema tal como sale”. El sujeto lee tu descripción de disensor en los dos brazos, pero solo en A2 recibe el esquema que esa descripción explica. Es una contaminación que se activa en un brazo solo. Toca también al generador y al chequeo de capacidad.

Arreglo, medido: con un CODEX_HOME aislado desaparecen el AGENTS.md y la lista de plugins recomendados (cero apariciones de “Dev solo”, “residuo” y “red-team”). Tres condiciones:

- La carpeta va fuera de %TEMP%. Si no, Codex se niega a crear sus binarios auxiliares (lo avisó en la prueba).
- El nombre de la carpeta tiene que ser neutro: la ruta del home entra al contexto, en la lista de raíces de skills.
- Un codex login propio dentro de ese home, en vez de copiar el tuyo.

Skills: las 26 de ~/.agents/skills siguen entrando aun con el home aislado (review, review-security, review-bugbot…). Ninguna nombra disensor, así que no distinguen brazos. Pero son unos 6.000 tokens por llamada y empujan a los dos brazos hacia el modo revisor.

- -c features.skills=false no hace nada, y no existe un feature skills.
- La vía por ruta, -c skills.config=[{path=…,enabled=false}], funcionó el 1/10. Hay que sacarlas así o declararlas.

### 2. Python en Windows cambia en silencio los bytes que mandás.

Tu Python 3.14.2 corre con utf8_mode=0 y codificación cp1252.

Con subprocess.run(..., text=True) pasan dos cosas:

- La entrada sale en cp1252, así que las comillas curvas y las rayas del prompt generador le llegan a Codex como UTF-8 inválido.
- Cada \n sale como \r\n.

Así, el md5 congelado no coincide con lo que recibe el modelo. Además, el diff línea por línea de §4.4.2 puede marcar todas las líneas si un archivo quedó en CRLF y el otro en LF.

Arreglo: todo en bytes.

- Mandar input=msg.encode("utf-8").
- Decodificar las salidas como UTF-8.
- Escribir los archivos en binario o con newline="".
- Registrar el md5 de los bytes exactos que se mandan y compararlo en cada llamada con el congelado.

## Para cerrar §14 (las preguntas 1 y 2)

### 3. El modelo de GPT.

En tu máquina, disensor corre Codex con -m gpt-5.6-sol: está registrado en ~/.disensor/reviewers.json. No usa el gpt-6-astra en xhigh de tu config.toml, porque --ignore-user-config descarta ese archivo.

- Qué significa “como disensor corre GPT”: gpt-5.6-sol, con el esfuerzo por defecto de la CLI, que no es xhigh.
- Si eligen Astra: ya no es “como disensor”, y por token cuesta 5 veces Sol, así que el presupuesto cambia.

El esfuerzo, dos opciones:

- Fijarlo con -c model_reasoning_effort=…, y declarar que la receta no lo fija.
- Dejar el valor por defecto y registrarlo. Ese valor cambia con la versión de la CLI, así que esto descansa en que la versión quede fija.

### 4. Los flags de claude -p, confirmados en tu 2.1.285:

- --safe-mode: apaga CLAUDE.md, skills, plugins, hooks y MCP.
- --tools "": sin herramientas. Desde Python como argumento de lista funciona; desde Git Bash el argumento vacío se pierde.
- --no-session-persistence y --output-format json.
- --model con el ID explícito. En esta versión el alias haiku resuelve a 4.5 y sonnet a claude-sonnet-5-5.
- --effort existe, y el protocolo no lo menciona: la temperatura no se puede fijar, pero el esfuerzo del juez sí.

Queda sin poder sacarse: el prompt de sistema del arnés, unos 1.500 tokens. Va declarado, igual que las instrucciones de Codex.

Para probar en el piloto (sin verificar): si --system-prompt reemplaza también ese bloque, el juez queda más cerca de una llamada al modelo pelado.

### 5. Versiones congeladas (§7.3).

Claude Code se actualiza solo, y el binario de ~/.local/bin es el mismo que usan tus sesiones interactivas. Una actualización desde cualquiera de ellas lo cambia en plena corrida, y DISABLE_AUTOUPDATER=1 en el entorno del arnés no lo evita.

- Arreglo: llamar directo al binario versionado, ~/.local/share/claude/versions/2.1.285, que ya está en tu máquina.
- Codex por npm no se actualiza solo. El registro de disensor fija codex.CMD por sha256: sirve como control en cada llamada.

## Riesgo alto del piloto

### 6. El sandbox de solo lectura (§7.4.1) probablemente no arranque.

Tu AGENTS.md documenta que -s read-only falla desde Claude Code, y la propia receta lo advierte.

- Corré el arnés desde una terminal común, y probá esto primero con una sola llamada, antes de escribir todo lo demás.
- Si falla, hay alternativa para proponer antes de congelar: --disable shell_tool. El feature existe y viene activo en 0.153.4; apagarlo le quita al sujeto la herramienta de ejecutar comandos.
- El límite de esa alternativa: apply_patch no tiene interruptor. Sin sandbox, el sujeto podría escribir archivos. Habría que revisar la carpeta después de cada llamada, como hace disensor, y contar cualquier escritura como falla.

## Lo que verifiqué y está bien

- El esquema y rules.py no cambiaron entre de14e5c y main (1064ef6). Fijar ese commit es lo mismo que usar el esquema actual.
- Los flags de Codex que cita §7.1 existen en 0.153.4.
- El presupuesto (~760 llamadas de GPT y ~520 de Claude) entra:
  - GPT: en la semana actual (99% libre) más los 3 restablecimientos.
  - Claude: entre 2% y 11% de una semana, así que entra incluso antes del viernes.
  - Con gpt-5.6-sol queda holgado; con Astra, lo decide el piloto.
- Un pedido para el piloto: que informe los tokens por tipo de llamada. El generador escribe logs largos y pesa bastante más que una llamada de brazo.

## Una corrección de texto

§7.1 dice que a la receta se le cambia “una sola cosa”. Con lo de arriba son al menos tres: el sandbox, el CODEX_HOME aislado y las skills, más el shell si el sandbox no arranca. Hay que reescribir también la frase “como disensor corre GPT”: disensor, tal como corre hoy, filtra tu AGENTS.md (#108). El experimento lo corrige a propósito, y eso va declarado.

El paso 3 del protocolo pide una tercera revisión independiente antes de congelar. Las dos anteriores las hicieron agentes de Claude sobre un protocolo que escribió Claude, así que Codex sería el revisor más decorrelacionado. Costaría una o dos llamadas de tu semana de GPT, y la corro solo con tu OK. También puedo dejar esta revisión como 04-REVISION-ARNES.md en la carpeta del experimento, para que Claude chat la incorpore.
