# Para Claude Code: correr el piloto

**Qué es.** El experimento de disensor sobre el escenario Hide Pending Tool Call.
El protocolo es `01-PROTOCOLO.md` (v5, no congelado); el arnés está en
`herramientas/` (`arnes.py`, `generador.py`, `piloto.py`). Los escribe la sesión
de difusión (Claude en Cowork), que no puede ejecutar nada en Windows. **Tu
parte es correr las etapas en la máquina de Nico e informar lo que salió.**

## Reglas

1. **No cambies prompts, esquemas, umbrales ni el protocolo, y no edites los
   scripts de `herramientas/`.** Si algo falla, informá el error, la causa
   probable y el cambio que propondrías. Nico decide, y el cambio lo aplica la
   sesión de difusión, para que los scripts tengan un solo autor.
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
