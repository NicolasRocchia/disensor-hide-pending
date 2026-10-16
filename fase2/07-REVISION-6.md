# Sexta revisión de la fase 2: Codex sobre el último arreglo

**16/10/2026.** Codex revisó el arreglo de la quinta ronda (`7acf30a..545231b` y el
protocolo v6). El mismo binario, el mismo `CODEX_HOME` aislado, sólo lectura con
`windows.sandbox=unelevated` y esfuerzo `high`. 22 comandos de lectura, ningún
archivo cambiado, `git status` limpio después; el único que nombra los brazos los
excluye de una búsqueda. Uso: 1.200.606 tokens de entrada (1.121.792 de caché) y
15.706 de salida, en 285 segundos. **Un hallazgo, una NOTA, y ningún bloqueante ni
regresión.**

**Verificado por Claude Code contra el código:** se confirma, pero no es alcanzable
en una corrida legítima. `jueces_que_llaman` trata igual un `json.txt` que no parsea y
uno que dice `null`, y en los dos casos pide el binario de Claude aunque el juez no lo
llame. Pero `json.txt` lo escribe `correr_brazo` sólo a partir de un objeto de nivel
superior con `findings` (`extraccion.extraer`), así que nunca vale `null`; y el error
es del lado seguro (pedir el binario de más no frena nada que vaya a correr). **No se
arregla:** un cambio pediría otra ronda por un caso que no puede pasar.

Con esto las rondas convergieron: la quinta trajo dos hallazgos menores y la sexta,
uno inalcanzable. Lo que queda antes de congelar es de Nico: las seis decisiones de
diseño de `02-REVISION-1.md` (que, si se toman, cambian el código y piden otra
ronda), el login del CLI de Claude para `juez-prueba` y los jueces del piloto, y el
congelamiento.

Lo que sigue es la respuesta **textual** de Codex y su consigna.

---

## Respuesta de Codex

Encontré un solo hallazgo, de alcance marginal. No hay bloqueantes ni regresiones que afecten la confirmatoria.

1. Un JSON válido `null` todavía exige Claude aunque el juez no lo llama.

   - **Gravedad:** NOTA
   - **Tipo:** implementación
   - **Dónde:** [corrida2.py:727](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:727), [piloto.py:795](/D:/Programacion/Disensor-Docs/experimento/herramientas/piloto.py:795), [prueba_offline2.py:769](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/prueba_offline2.py:769).
   - **Evidencia:** `jueces_que_llaman` usa `None` tanto para “no parseó” como para el resultado válido de `json.loads("null")`. Lo reproduje en memoria: con brazo `hecho`, `json_md5` y `json.txt = b"null"`, el predicado incluye el ítem; `piloto.juzgar` devuelve `juzgado / sin textos libres` sin llamar. No afecta una corrida legítima: el escritor sólo crea `json.txt` a partir de un objeto de nivel superior con `findings`, según [extraccion.py:56](/D:/Programacion/Disensor-Docs/experimento/herramientas/extraccion.py:56). Tampoco produce el defecto peligroso inverso.
   - **El arreglo más chico:** usar un centinela distinto de `None` para “no parseó”, aplicar `juez.textos_libres` a todo valor que sí parseó y agregar el caso `null` a la prueba.

Verificado y bien: un objeto con texto libre es incluido por `jueces_que_llaman`; uno formado sólo por valores fijos es excluido y `piloto.juzgar` no llama.

Verificado y bien: no encontré ningún estado estable donde el predicado excluya un ítem que `juzgar_item` lleve a Claude; ambos usan la misma decodificación, `json.loads`, `fijos` y `juez.textos_libres`.

Verificado y bien: un BOM UTF-8, UTF-16, bytes no UTF-8 o JSON inválido se cuentan conservadoramente; luego `juzgar_item` falla durante la misma decodificación o parseo, antes de Claude.

Verificado y bien: si `json_md5` no coincide, `juzgar_item` para antes de Claude; si falta `json_md5` o `json.txt`, tampoco existe una ruta posterior de llamada.

Verificado y bien: `etapa_jueces` usa el predicado sobre todos los jueces pendientes antes de decidir si verifica Claude; `etapa_piloto` usa el mismo predicado.

Verificado y bien: si hipotéticamente se alcanzara una llamada tras omitir la verificación inicial, `una_llamada_claude` ejecuta `verificar_sha` antes de invocar el binario; un SHA cambiado para, y el binario fijado intacto puede ejecutarse. Si aún no existe el registro de binarios, `verificar_binarios` fuerza la verificación de ambos.

Verificado y bien: el protocolo v6 ahora dice correctamente que la versión de `jsonschema` queda en los resultados de A2b y A2.

Verificado y bien: las firmas y los dos sitios de llamada de `jueces_que_llaman` quedaron actualizados, y ambos reciben el mismo `fijos`.

No ejecuté `prueba_offline2.py`; tomé como dato los 50/50 externos. No abrí prosa prohibida ni modifiqué el árbol de trabajo.

## Consigna de Codex

Sos la sexta revisión independiente de la **fase 2** de un experimento preregistrado, antes de congelarla. Las cinco anteriores las hiciste vos, Codex: `fase2/02-REVISION-1.md` a `fase2/06-REVISION-5.md`. La quinta trajo dos hallazgos menores; Claude Code los arregló en `545231b` (código) y `d6574b1` (protocolo). Quedan seis decisiones de diseño para Nico (al final de `02-REVISION-1.md`): no las discutas, salvo que encuentres algo nuevo.

**Actuá como red-team sobre ese diff, no lo apruebes:** `git diff 7acf30a..545231b -- fase2/herramientas` y `git diff 7acf30a..d6574b1 -- fase2/01-PROTOCOLO.md`. ¿El arreglo cierra lo que dice `06-REVISION-5.md`? ¿Rompió algo? En especial: ¿`jueces_que_llaman` puede excluir un ítem que `juzgar_item` sí va a llevar a Claude (un JSON que parsea distinto en `piloto.juzgar`, un `json.txt` con BOM o con otra codificación, un `json_md5` que no coincide)? ¿Y `etapa_jueces` sin el binario de Claude verificado, cuando igual termina llamando, qué hace?

**Reglas de esta sesión:** sólo leés. No escribas, edites, muevas ni borres archivos, ni corras nada que cambie estado (nada de git que escriba, ni `git fetch`; `python -B` con `PYTHONDONTWRITEBYTECODE=1`, sin escribir archivos). Podés usar comandos de lectura y `python -` para importar los módulos y probar funciones puras en memoria. **No abras la prosa de los brazos de la fase 1** (`corrida/brazos/*/prosa.txt` ni sus `intento-*` ni `json.txt`). No corras `corrida.py`, `corrida2.py` ni `piloto.py` con ninguna etapa. `prueba_offline2.py` pasa 50 de 50 fuera de esta sesión.

**Formato de la respuesta, en castellano:** una lista de hallazgos, del más grave al menos grave, con **Gravedad** (BLOQUEANTE, DEBERÍA o NOTA), **Tipo**, **Dónde**, **Evidencia** y **El arreglo más chico**; después, una línea por lo que verificaste y está bien. Si no encontrás nada, decilo así.
