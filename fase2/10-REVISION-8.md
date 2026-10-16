# Octava revisión de la fase 2: Codex sobre los arreglos de la séptima

**16/10/2026.** Codex revisó los arreglos de la séptima ronda (`9c0e260..4c3a31b` y
`a106d25`). El mismo binario, el mismo `CODEX_HOME` aislado, sólo lectura con
`windows.sandbox=unelevated` y esfuerzo `high`. 14 comandos de lectura, ningún archivo
cambiado, `git status` limpio después; ninguno nombró la prosa de la fase 1. Uso:
811.329 tokens de entrada (736.640 de caché) y 12.148 de salida, en 377 segundos.
**Un hallazgo, de texto**; los arreglos de la séptima ronda, verificados (entre ellos,
que las componentes suman la suma de C1 en 2.304 combinaciones de veredictos y
etiquetas parciales).

**Verificado por Claude Code:** se confirma. §11 no decía que el canario de los brazos
lleva el marcador `[canary request]` al final del gemelo 003. Ahora lo dice. Es un
cambio sólo de texto: no pide otra ronda.

Lo que sigue es la respuesta **textual** de Codex y su consigna.

---

## Respuesta de Codex

1. El protocolo no registra que el canario de brazos usa un log 003 modificado.

   - **Gravedad:** DEBERÍA
   - **Tipo:** diseño
   - **Dónde:** [01-PROTOCOLO.md:371](D:/Programacion/Disensor-Docs/experimento/fase2/01-PROTOCOLO.md:371), [corrida2.py:183](D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:183), [corrida2.py:221](D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:221).
   - **Evidencia:** el arreglo pedido por `09-REVISION-7.md` incluía actualizar §11, pero `a106d25` no toca esa sección. El protocolo todavía dice que el canario corre «sobre el log 003 del piloto», sin declarar que el código agrega `\n\n[canary request]` al final del log. Byte a byte, el mensaje real `003-A2-limpio` mide 12.831 bytes y el canario 12.849; quitando esos únicos 18 bytes, ambos son idénticos. La instrucción A2 y el esquema permanecen byte por byte iguales, y el canario no coincide con ninguno de los 80 ítems del piloto. El marcador también cambia necesariamente el contenido visible y el tamaño, no sólo el hash; no altera ningún ítem real ni otra ruta del arnés.
   - **El arreglo más chico:** agregar en §11 que el canario de brazos usa el gemelo 003 con el marcador fijo `[canary request]` agregado al final del log, para distinguirlo de `003-A2-limpio`.

Verificado y bien: `_c1` calcula las componentes en todas sus invocaciones, incluida la versión tal cual y las dos recalculaciones adversas; en 2.304 combinaciones de veredictos y etiquetas parciales, `pendiente + gemelo == suma`.

Verificado y bien: las etiquetas que `_en_contra` deja afuera vuelven al veredicto del juez mediante el fallback de `marca`/`fp`; sólo las modificaciones individualmente contrarias al signo se aplican.

Verificado y bien: `frase` no accede a las recalculaciones sin etiquetas, porque retorna antes en [analisis2.py:444](D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/analisis2.py:444).

Verificado y bien: con suma cero las recalculaciones quedan como `aplica: false`, y `frase` tampoco las indexa: la prueba bilateral da `p=1`, por lo que retorna por la rama no significativa antes de ese acceso.

Verificado y bien: la frase mecanística exige ahora que la componente del pendiente tenga el signo de C1 en el original y en ambas recalculaciones; el caso de la revisión 7 cae en la frase de falsos positivos.

Verificado y bien: el canario conserva el armado A2, la instrucción y el esquema, queda por encima del percentil 90 y ya no es idéntico a ningún ítem del piloto.

Verificado y bien: las tres docstrings y §12 documentan los diez pares y que 000/001 conservan sus resultados y orden históricos.

Verificado y bien: §6.1 ya no afirma que la prosa vacía sólo pueda ocurrir en A2/A2b; declara correctamente que la regla cubre los cuatro brazos.

El piloto ampliado confirma 80/80 brazos y 120/120 jueces, pero no ejerció el canario en vivo porque no hubo fallas; de éste pude verificar sólo su construcción pura y las invariantes anteriores.

## Consigna de Codex

Sos la octava revisión independiente de la **fase 2** de un experimento preregistrado, antes de congelarla. Las anteriores las hiciste vos, Codex (`fase2/02-REVISION-1.md` a `fase2/09-REVISION-7.md`). La séptima revisó las decisiones 6 a 13 de Nico (§15 de `fase2/01-PROTOCOLO.md`) y trajo cinco hallazgos; Claude Code los arregló en `4c3a31b` (código) y `a106d25` (protocolo). Después corrió el piloto ampliado (`fase2/08-PILOTO.md`), que se puede leer.

**Actuá como red-team sobre ese diff, no lo apruebes:** `git diff 9c0e260..4c3a31b -- fase2/herramientas` y `git diff 9c0e260..a106d25 -- fase2/01-PROTOCOLO.md`. ¿Cada arreglo cierra lo que dice `09-REVISION-7.md`? ¿Rompió algo? En especial: ¿`_c1` con las componentes en las tres versiones de C1 es correcto con etiquetas parciales y con las que `_en_contra` deja afuera? ¿`frase` puede acceder a `c1_con_etiquetas_de_nico` cuando no aplica (suma cero) o cuando no hay etiquetas? ¿El marcador del canario de los brazos cambia algo más que su identidad con el ítem 003?

**Reglas de esta sesión:** sólo leés. No escribas, edites, muevas ni borres archivos, ni corras nada que cambie estado (nada de git que escriba, ni `git fetch`; `python -B` con `PYTHONDONTWRITEBYTECODE=1`, sin escribir archivos). Podés usar comandos de lectura y `python -` para importar los módulos y probar funciones puras en memoria. **No abras la prosa de los brazos de la fase 1** (`corrida/brazos/*/prosa.txt` ni sus `intento-*` ni `json.txt`). No corras `corrida.py`, `corrida2.py` ni `piloto.py` con ninguna etapa. `prueba_offline2.py` pasa 61 de 61 fuera de esta sesión.

**Formato de la respuesta, en castellano:** una lista de hallazgos, del más grave al menos grave, con **Gravedad** (BLOQUEANTE, DEBERÍA o NOTA), **Tipo**, **Dónde**, **Evidencia** y **El arreglo más chico**; después, una línea por lo que verificaste y está bien. Si no encontrás nada, decilo así.
