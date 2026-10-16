# Séptima revisión de la fase 2: Codex sobre las decisiones 6 a 13

**16/10/2026.** Nico tomó las siete decisiones de diseño que quedaban, todas como
estaban recomendadas (§15, 6 a 13). Codex revisó su implementación (`ddcba94..31b4465`
y el protocolo v8, `9c0e260`), con la consigna de atacar si el código y el texto hacen
lo que cada decisión dice, sin discutir las decisiones. El mismo binario, el mismo
`CODEX_HOME` aislado, sólo lectura con `windows.sandbox=unelevated` y esfuerzo `high`.
31 comandos de lectura, ningún archivo cambiado, `git status` limpio después; ninguno
nombró la prosa de la fase 1. Uso: 1.992.970 tokens de entrada (1.757.056 de caché) y
24.634 de salida, en 474 segundos. Cinco hallazgos; las decisiones 6, 8, 9, 10, 11 y
12, verificadas y bien implementadas.

**Verificado por Claude Code contra el código:** los cinco se confirman.

| Hallazgo | Qué se hizo |
|---|---|
| 1 (BLOQUEANTE): la frase «hizo que la respuesta dijera…» miraba sólo las componentes con las etiquetas de los jueces; si Nico bajaba todas las marcas de A2 y C1 seguía dando por los gemelos, la frase salía igual | Las componentes se calculan también en las dos recalculaciones con las etiquetas de Nico, y esa frase va sólo si la del pendiente tiene el signo de C1 en las tres; si no, la de los falsos positivos. Dicho en §9. |
| 2: el canario de los brazos era byte por byte el pedido del ítem `003-A2-limpio`, que con la decisión 13 es del piloto | El canario lleva un marcador neutro al final del log (`[canary request]`, 12.849 bytes): ya no es el pedido de ningún ítem. |
| 3 (NOTA): con C1 sumando cero, «en contra del signo» tomaba el positivo | Con suma cero, las dos recalculaciones no aplican (C1 tampoco da). Dicho en §8. |
| 4 (NOTA): al ampliar el piloto, los pares 000 y 001 se reusan con su orden, no con el del plan nuevo; tres docstrings decían «dos pares» | Dicho en §12 y en la docstring de la etapa; las tres corregidas. |
| 5 (NOTA): §6.1 decía que la prosa vacía sólo puede pasar en A2b y A2 | «Se espera sobre todo en A2b y A2»; la regla vale para los cuatro brazos. |

Además, `juez-prueba` con el caso nuevo de la decisión 6, una negativa por cautela que
no dice que falte un dato: el juez la clasificó como categoría 3 y no es falso
positivo. **7 de 7**, en una llamada, USD 0,0300.

`prueba_offline2.py`: 61 de 61; tres mutaciones que deshacen estos arreglos, y las tres
hacen fallar alguna prueba. La fase 1 sigue en 142 de 142.

Lo que sigue es la respuesta **textual** de Codex y su consigna.

---

## Respuesta de Codex

1. La frase mecanística puede sobrevivir aunque Nico elimine toda la señal del pendiente.

   - **Gravedad:** BLOQUEANTE
   - **Tipo:** implementación
   - **Dónde:** [analisis2.py:328](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/analisis2.py:328), [analisis2.py:346](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/analisis2.py:346), [analisis2.py:448](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/analisis2.py:448), protocolo §8–§9.
   - **Evidencia:** reproduje 40 pares: ocho marcas de A2 en el pendiente y doce falsos positivos de A1. C1 original dio suma 20, componentes `pendiente=8`, `gemelo=12`. Nico cambió las ocho marcas de A2 de 3 a 2. Las dos recalculaciones adversas quedaron significativas con suma 12, por lo que `sensible_al_juez=False`; el estrato tenía N=8, así que tampoco activó la compuerta. Aunque la componente validada del pendiente quedó exactamente en cero, `frase()` consultó la componente original y publicó «hizo que la respuesta dijera…». Es el mismo tipo de atribución falsa que la decisión 7 debía cerrar.
   - **El arreglo más chico:** calcular las componentes también para `h` y `hd`, y permitir la frase del pendiente sólo si esa componente tiene el signo de C1 en el original y en ambas recalculaciones adversas. Si no, usar la frase de falsos positivos. Dejar explícita esta condición en §9.

2. El canario de brazos es exactamente uno de los nuevos ítems del piloto.

   - **Gravedad:** DEBERÍA
   - **Tipo:** diseño
   - **Dónde:** [corrida2.py:181](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:181), [corrida2.py:218](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:218), [corrida2.py:256](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:256), protocolo §11–§12.
   - **Evidencia:** comprobé igualdad byte por byte entre `mensaje_canario("brazo")` y el mensaje real del nuevo ítem `003-A2-limpio`. Si ese ítem falla sistemáticamente por su contenido, el canario repite el mismo pedido y falla también: el arnés lo clasifica como caída del servicio, no consume el reintento ordinario y, después de tres reanudaciones, deja `PARADA`. Los canarios de los jueces no tienen esta identidad exacta porque usan respuestas fijas.
   - **El arreglo más chico:** usar un pedido canario congelado y distinto de los 80 del piloto, por ejemplo una variante sintética del 003 con un marcador neutro fijo, verificando nuevamente que quede por encima del percentil 90. Actualizar §11.

3. Con C1 exactamente empatada, «en contra del signo» toma arbitrariamente el signo positivo.

   - **Gravedad:** NOTA
   - **Tipo:** implementación
   - **Dónde:** [analisis2.py:348](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/analisis2.py:348).
   - **Evidencia:** `signo = 1 if c1["suma"] >= 0 else -1`; con suma cero conserva únicamente etiquetas que empujan hacia negativo y descarta las que empujan hacia positivo. Cero no tiene el signo positivo que promete §8. Esto no puede producir `sensible_al_juez`, porque esa bandera exige que C1 original sea significativa, pero deja dos recalculaciones publicadas cuya dirección depende de una convención no preregistrada.
   - **El arreglo más chico:** con suma cero, marcar las recalculaciones unilaterales como no aplicables —la versión tal cual ya queda disponible— y decirlo en §8.

4. La reanudación conserva los resultados viejos, pero no un único orden sorteado de jueces para los diez logs.

   - **Gravedad:** NOTA
   - **Tipo:** implementación
   - **Dónde:** [corrida2.py:435](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:435), [corrida2.py:446](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:446), [corrida2.py:1029](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:1029).
   - **Evidencia:** los 16 brazos y 24 jueces de 000/001 están terminales y se reutilizan; los 16 mensajes de brazos todavía coinciden con su `mensaje_md5`. El plan de brazos viejo es exactamente el prefijo del nuevo plan de 80. En cambio, al ampliar y volver a mezclar globalmente los 120 jueces, el orden de 000/001 filtrado del plan nuevo no coincide con el viejo. La secuencia efectivamente realizada será los 24 viejos en su orden anterior y los 96 nuevos en el nuevo orden, no el plan fresco de diez logs. No afecta la confirmatoria y el piloto no hace inferencia.
   - **El arreglo más chico:** documentar que la ampliación reusa los dos logs y conserva su orden histórico. Además, actualizar las tres docstrings que todavía dicen «dos pares».

5. El protocolo afirma demasiado al decir que la prosa vacía sólo puede ocurrir en A2/A2b.

   - **Gravedad:** NOTA
   - **Tipo:** diseño
   - **Dónde:** [01-PROTOCOLO.md:169](/D:/Programacion/Disensor-Docs/experimento/fase2/01-PROTOCOLO.md:169), [jueces2.py:107](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/jueces2.py:107).
   - **Evidencia:** el arnés considera terminada una salida GPT si el archivo tiene algún byte; una salida compuesta sólo por espacios puede quedar `hecho`. `prosa_vacia()` usa `strip()`, por lo que aplicaría correctamente la regla también a A0 o A1. El código es más general que el texto.
   - **El arreglo más chico:** reemplazar «Sólo puede pasar» por «Se espera principalmente en A2b y A2, por la extracción».

Decisiones verificadas y bien implementadas:

- **Decisión 6:** `es_fp` usa exclusivamente `major_hallucinated_claim`; la negativa queda descriptiva. La regla vacía queda atada al md5, entra como categoría 1/FP falso en C1 y descriptivas, cuenta `prosa_vacia`, se excluye de las muestras y sólo puede reaparecer en planilla si el log es decisivo. `armar_pares` deriva nuevamente el FP desde la categoría.
- **Decisión 8:** en los estratos 1 y 2, 1↔2 cuenta como acuerdo binario; sólo el cruce 3↔no-3 desacuerda. La coincidencia exacta queda separada y descriptiva.
- **Decisión 9, cuando C1 tiene signo no nulo:** verifiqué los cuatro pesos: A2-pendiente `+`, A1-pendiente `−`, A2-gemelo `−`, A1-gemelo `+`. Un ítem que también pertenece a la muestra aparece una sola vez. No encontré falsos positivos o negativos de `sensible_al_juez` para C1 significativa, fuera de la atribución de la frase señalada arriba.
- **Decisión 10:** no se agregaron señuelos; las planillas siguen siendo la unión sin duplicados de decisivos y muestras, y §13.7 declara el límite.
- **Decisión 11:** elimina el log completo si cualquiera de las cuatro prosas A2/A1 contiene un objeto `findings` o `residue`; el subconjunto vacío se procesa sin excepción.
- **Decisión 12:** las seis filas reproducen 29,0%, 57,9%, 81,3%, 24,7%, 51,8% y 79,1%; `FILAS_6_6` tiene trece filas y la frase nula incluye las trece con A1/A2 y el efecto correspondiente.

No ejecuté etapas ni la suite, porque escriben archivos; tomé como dato los 59/59 externos. Tampoco pude verificar el piloto ampliado de punta a punta: en disco sólo están completos los dos pares anteriores y el nuevo caso `fp-cautela`. No abrí ninguna prosa ni JSON de los brazos de fase 1 y el `git status` quedó igual que al inicio.

## Consigna de Codex

Sos la séptima revisión independiente de la **fase 2** de un experimento preregistrado, antes de congelarla. Las seis anteriores las hiciste vos, Codex (`fase2/02-REVISION-1.md` a `fase2/07-REVISION-6.md`), y el piloto está en `fase2/08-PILOTO.md`. Nico tomó ahora las siete decisiones de diseño que quedaban, todas como estaban recomendadas: son las 6 a 13 de §15 de `fase2/01-PROTOCOLO.md` (v8). Claude Code las implementó en `31b4465` y el protocolo en `9c0e260`.

**Actuá como red-team sobre ese diff, no lo apruebes:** `git diff ddcba94..31b4465 -- fase2/herramientas` y `git diff ddcba94..9c0e260 -- fase2/01-PROTOCOLO.md`. Las decisiones ya están tomadas: no discutas si conviene tomarlas; atacá si el código y el texto hacen lo que cada una dice, y qué rompen. En especial:

1. **Decisión 6** (`fp_prosa` sólo la categoría 1; la prosa vacía por regla): `jueces2.es_fp`, `VEREDICTO_PROSA_VACIA`, la regla en `juzgar_item`, `jueces_que_llaman`, `armar_pares` (que ahora deriva el falso positivo de la categoría) y las muestras de §8 sin los veredictos por regla. ¿Un veredicto por regla puede quedar inconsistente con la prosa (por ejemplo, si la prosa cambia)? ¿Entra bien a C1, a las descriptivas y a las planillas?
2. **Decisión 7** (la frase sale del pendiente): `c1["componentes"]` y `frase`. ¿Las componentes suman la suma de C1? ¿La condición elige bien la frase en contra, con empates y con la componente del pendiente en cero? ¿El agregado a la frase nula cuando el juez no es confiable?
3. **Decisión 8** (compuerta binaria): `_validacion`. ¿Los estratos 1 y 2 miden lo que tienen que medir?
4. **Decisión 9** (las etiquetas sólo en contra): `_en_contra` y cómo la usan las dos recalculaciones. ¿Los signos de cada ítem (A2 y A1, pendiente y gemelo) están bien? ¿Una etiqueta de un ítem decisivo y de la muestra a la vez? ¿Puede `_en_contra` hacer que «sensible al juez» no salte cuando debería, o al revés?
5. **Decisiones 11, 12 y 13:** la sensibilidad sin restos de JSON, las filas nuevas de `FILAS_6_6` (¿la frase nula queda bien con trece filas?) y `LOGS_DEL_PILOTO` con diez logs (¿reanudar el piloto sobre los dos que ya corrieron reusa sus resultados, con el mismo orden sorteado? ¿Algo del canario, que usa el log 003, choca con que el 003 ahora sea del piloto?).

**Reglas de esta sesión:** sólo leés. No escribas, edites, muevas ni borres archivos, ni corras nada que cambie estado (nada de git que escriba, ni `git fetch`; `python -B` con `PYTHONDONTWRITEBYTECODE=1`, sin escribir archivos). Podés usar comandos de lectura y `python -` para importar los módulos y probar funciones puras en memoria. **No abras la prosa de los brazos de la fase 1** (`corrida/brazos/*/prosa.txt` ni sus `intento-*` ni `json.txt`). Lo de `fase2/piloto/` se puede leer (§12). No corras `corrida.py`, `corrida2.py` ni `piloto.py` con ninguna etapa. `prueba_offline2.py` pasa 59 de 59 fuera de esta sesión.

**Formato de la respuesta, en castellano:** una lista de hallazgos, del más grave al menos grave. Cada uno con **Gravedad** (BLOQUEANTE si invalida la confirmatoria o puede tirar una corrida legítima, DEBERÍA si conviene arreglarlo antes de congelar, NOTA), **Tipo** (implementación o diseño), **Dónde**, **Evidencia** y **El arreglo más chico**. Después, una línea por cada decisión que verificaste y está bien implementada. Si algo no lo pudiste verificar, decilo.
