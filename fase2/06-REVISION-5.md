# Quinta revisión de la fase 2: Codex sobre los canarios del lado de arriba

**16/10/2026.** Codex revisó los arreglos de la cuarta ronda (`71dfeae..9713fd2` y el
protocolo v5). El mismo binario, el mismo `CODEX_HOME` aislado, sólo lectura con
`windows.sandbox=unelevated` y esfuerzo `high`. 13 comandos de lectura, ningún
archivo cambiado, `git status` limpio después; ninguno nombró la prosa de la fase 1.
Uso: 813.111 tokens de entrada (737.152 de caché) y 14.577 de salida, en 277
segundos. **Dos hallazgos, ninguno bloqueante**, y los arreglos de la cuarta ronda,
verificados.

**Verificado por Claude Code contra el código:** los dos se confirman.

| Hallazgo | Qué se hizo |
|---|---|
| 1: `jueces_que_llaman` contaba un juez del JSON aunque el JSON no tuviera textos libres, que `piloto.juzgar` resuelve sin llamar; y `jueces` pedía el binario de Claude sin mirar | El predicado lee el JSON y cuenta el ítem sólo si `juez.textos_libres` da algo (ante un JSON que no parsea, cuenta: pedir el binario de más no frena nada). `jueces` usa el mismo predicado antes de pedir el binario. |
| 2 (NOTA): §11 decía que la versión de `jsonschema` queda en cada resultado de los brazos, y ahora queda en los de A2b y A2 | Corregido en §11. |

`prueba_offline2.py`: 50 de 50; dos mutaciones que deshacen el arreglo, y las dos
hacen fallar alguna prueba. El protocolo pasa a la v6.

Lo que sigue es la respuesta **textual** de Codex y su consigna.

---

## Respuesta de Codex

Encontré dos hallazgos. No vi una regresión que invalide la confirmatoria.

1. `jueces_que_llaman` todavía puede exigir Claude cuando el juez no lo usará.

   - **Gravedad:** DEBERÍA
   - **Tipo:** implementación
   - **Dónde:** [corrida2.py:714](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:714), [corrida2.py:725](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:725), [corrida2.py:1016](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:1016), [piloto.py:785](/D:/Programacion/Disensor-Docs/experimento/herramientas/piloto.py:785), protocolo §11.
   - **Evidencia:** para un juez JSON, `jueces_que_llaman` considera suficiente que exista `json_md5`. Pero `piloto.juzgar` no llama a Claude cuando el JSON no contiene textos libres. Lo reproduje en memoria con `piloto.CASOS_JUEZ[2]`, `solo-valores-fijos`: `juez.textos_libres` devolvió `[]` y `piloto.juzgar` devolvió `juzgado / sin textos libres` aunque reemplacé `claude_con_reintentos` por una función que explotaba. Para el mismo estado `{estado: "hecho", json_md5: "abc"}`, `jueces_que_llaman` incluyó el ítem. Además, `etapa_jueces` no usa el predicado y verifica Claude incondicionalmente, aunque sólo queden jueces que se resolverán como `sin_llamada` o JSON sin textos. Esto contradice la nueva frase “cada etapa pide […] nada más”. No encontré el defecto inverso: si el predicado excluye un ítem, `juzgar_item` tampoco llega a Claude.
   - **El arreglo más chico:** hacer que el predicado de JSON compruebe también `juez.textos_libres(obj, fijos)`, y usar la misma selección tanto en `etapa_piloto` como en `etapa_jueces` antes de decidir si verificar Claude.

2. La versión de `jsonschema` ya no queda en cada resultado de brazos, contra el protocolo.

   - **Gravedad:** NOTA
   - **Tipo:** implementación
   - **Dónde:** [corrida2.py:587](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:587), [corrida2.py:1010](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:1010), [01-PROTOCOLO.md:342](/D:/Programacion/Disensor-Docs/experimento/fase2/01-PROTOCOLO.md:342).
   - **Evidencia:** si al reanudar todos los A2/A2b son terminales y sólo falta un A0 o A1, `sello` no contiene `jsonschema`; ese resultado nuevo tampoco lo contendrá. El protocolo todavía dice “Su versión queda en cada resultado de los brazos”. No afecta la validación: A0/A1 no usan esa biblioteca.
   - **El arreglo más chico:** cambiar el protocolo a “Su versión queda en cada resultado de A2b y A2”.

Arreglos de la cuarta ronda verificados y correctos:

- **Canario de brazos:** usa A2 sobre el gemelo 003 y mide 12.831 bytes, por encima del percentil 90 declarado de 12.633.
- **`JSON_CANARIO` y respuestas fijas:** importa correctamente desde `piloto.CASOS_JUEZ`; conserva `residue`, agrega cuatro hallazgos y `juez.textos_libres` obtiene nueve textos, no lo filtra entero. Los mensajes miden JSON 1.746, Q.2.8 7.902 y FP 8.600 bytes; `PROSA_CANARIO` tiene 2.002 caracteres.
- **Condición de `jsonschema`:** se exige únicamente si queda algún A2b/A2, tanto en `etapa_brazos` como en el piloto. Que el chequeo quede después de `plan_congelado` no modifica el orden ni el ancla; puede dejar el plan creado antes de frenar, pero ninguna llamada ocurre antes del chequeo.
- **Receta y §13.9:** C ya debe decir “congelado”, R reemplaza el marcador de Enmiendas, y tag/push son coherentes con el arnés. La limitación del canario por tamaño quedó declarada.

No pude correr `prueba_offline2.py` por la falta de temporal escribible; tomé como dato los 50/50 externos. Tampoco probé binarios, sesiones ni red reales. No abrí ninguna prosa prohibida ni modifiqué archivos.

## Consigna de Codex

Sos la quinta revisión independiente de la **fase 2** de un experimento preregistrado, antes de congelarla. Las cuatro anteriores las hiciste vos, Codex: `fase2/02-REVISION-1.md` a `fase2/05-REVISION-4.md`, con qué se hizo con cada hallazgo. Claude Code arregló los cuatro de la cuarta en `9713fd2` y el protocolo pasó a la v5 en `e9cc38b`. Quedan seis decisiones de diseño para Nico (al final de `02-REVISION-1.md`): no las discutas, salvo que encuentres algo nuevo.

**Actuá como red-team sobre ese diff, no lo apruebes:** `git diff 71dfeae..9713fd2 -- fase2/herramientas` y `git diff 71dfeae..e9cc38b -- fase2/01-PROTOCOLO.md`. Dos preguntas:

1. **¿Cada arreglo cierra lo que dice `05-REVISION-4.md`?** El canario de los brazos sobre el gemelo, `JSON_CANARIO` y la respuesta fija de los jueces de la prosa, `jueces_que_llaman` y las condiciones de `jsonschema` en `etapa_brazos` y `etapa_piloto`, y la receta y el límite §13.9 en el protocolo.
2. **¿Rompieron algo?** Regresiones y falsos frenos nuevos. Por ejemplo: ¿`JSON_CANARIO` se arma bien al importar el módulo (lee `piloto.CASOS_JUEZ`)? ¿`juez.textos_libres` lo acepta y no lo filtra entero? ¿Mover `exigir_jsonschema` después de `plan_congelado` en `etapa_brazos` cambia algo del ancla o del plan? ¿`jueces_que_llaman` puede dejar sin verificar el binario de Claude cuando `juzgar_item` igual lo va a llamar?

**Reglas de esta sesión:** sólo leés. No escribas, edites, muevas ni borres archivos, ni corras nada que cambie estado (nada de git que escriba, ni `git fetch`; `python -B` con `PYTHONDONTWRITEBYTECODE=1`, sin escribir archivos). Podés usar comandos de lectura y `python -` para importar los módulos y probar funciones puras en memoria. **No abras la prosa de los brazos de la fase 1** (`corrida/brazos/*/prosa.txt` ni sus `intento-*` ni `json.txt`). No hace falta mirar `ayudas/`, `corrida/gemelos/revision-gpt/` ni `corrida/gemelos/PRECHEQUEO-C.md`. No corras `corrida.py`, `corrida2.py` ni `piloto.py` con ninguna etapa. `prueba_offline2.py` necesita un directorio temporal escribible que esta sesión no tiene: pasa 50 de 50 fuera de esta sesión.

**Formato de la respuesta, en castellano:** una lista de hallazgos, del más grave al menos grave. Cada uno con **Gravedad** (BLOQUEANTE si puede tirar una corrida legítima o invalida la confirmatoria, DEBERÍA si conviene arreglarlo antes de congelar, NOTA), **Tipo** (implementación o diseño), **Dónde**, **Evidencia** y **El arreglo más chico**. Después, una línea por cada arreglo de la cuarta ronda que verificaste y está bien. Si no encontrás nada, decilo así. Si algo no lo pudiste verificar, decilo.
