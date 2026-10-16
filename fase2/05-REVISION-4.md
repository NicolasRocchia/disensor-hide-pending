# Cuarta revisión de la fase 2: Codex sobre los arreglos de los falsos frenos

**16/10/2026.** Codex revisó los arreglos de la tercera ronda (`143bef4..195d00a` y el
protocolo v4) y la receta de congelamiento de §11. El mismo binario, el mismo
`CODEX_HOME` aislado, sólo lectura con `windows.sandbox=unelevated` y esfuerzo `high`.
27 comandos de lectura, ningún archivo cambiado, `git status` limpio después. No abrió
la prosa de la fase 1; sí leyó la prosa y el JSON de los brazos del piloto, que §12
permite leer, para medir el tamaño de los pedidos del juez del JSON. Uso: 2.253.890
tokens de entrada (2.146.688 de caché) y 23.403 de salida, en 476 segundos. Cuatro
hallazgos; los arreglos de la tercera ronda, verificados, y la receta pasa.

**Verificado por Claude Code contra el código:** los cuatro se confirman.

| Hallazgo | Qué se hizo |
|---|---|
| 1 (BLOQUEANTE, según Codex): el canario de los brazos era A2 sobre el pendiente (11.668 bytes), y A2 sobre el gemelo es más largo: 59 de los 100 pedidos reales lo superaban | El canario de los brazos es A2 sobre el gemelo del log 003: 12.831 bytes, por encima del percentil 90 que midió Codex (12.633). |
| 2: el canario del juez del JSON (1.236 bytes) quedaba en el medio de los del piloto (1.183 a 1.679) | Un caso congelado, armado a partir del de prueba de la fase 1 con cuatro hallazgos más de texto libre: 1.746 bytes. Y la respuesta fija de los jueces de la prosa pasa de 666 a 2.002 caracteres: Q.2.8 7.902 bytes, falsos positivos 8.600. |
| 3: el piloto pedía `jsonschema` aunque sólo faltaran A0 o A1, y Claude aunque los jueces que faltaban no fueran a llamarlo | `jsonschema` sólo si quedan A2b o A2, también en `brazos`; Claude sólo si algún juez que falta puede llamarlo (`jueces_que_llaman`: el brazo terminó y, en el juez del JSON, hay JSON). |
| 4: a la receta le faltaba decir que C ya dice «congelado» y que R reemplaza «*(ninguna todavía)*» | Dicho en §11. |

Lo que queda, declarado en §13.9: el canario va del lado de arriba de su familia,
pero no llega al pedido más grande de la corrida (A2 sobre el gemelo llega a 15.054
bytes). Una falla del servicio que dependiera del tamaño y quedara entre los dos se
contaría como falla del ítem. Perseguir el máximo exacto obligaría a usar uno de los
100 pares como canario.

`prueba_offline2.py`: 50 de 50; cinco mutaciones que deshacen estos arreglos, y las
cinco hacen fallar alguna prueba. La fase 1 sigue en 142 de 142. El protocolo pasa a
la v5.

Lo que sigue es la respuesta **textual** de Codex y su consigna.

---

## Respuesta de Codex

No congelaría todavía. Encontré un agujero bloqueante en el canario de los brazos y dos problemas menores.

1. El canario de los brazos no cubre el tamaño de A2 sobre los gemelos.

   - **Gravedad:** BLOQUEANTE
   - **Tipo:** diseño
   - **Dónde:** [corrida2.py:193](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:193), [corrida2.py:205](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:205), [01-PROTOCOLO.md:323](/D:/Programacion/Disensor-Docs/experimento/fase2/01-PROTOCOLO.md:323).
   - **Evidencia:** `mensaje_canario("brazo")` usa A2 sobre el **pendiente** del piloto 003 y mide 11.668 bytes. Sobre los 100 pares, los mensajes reales de A2 limpio van de 11.092 a 15.054 bytes, con percentil 90 en 12.633; **59 de 100 son más grandes que el canario**. En cambio, para A2 pendiente el percentil 90 es 11.503. El comentario menciona que el gemelo 003 es el más largo, pero el código nunca lo usa para GPT. Un límite entre 11.668 y 15.054 haría terminar el canario mientras fallan selectivamente llamadas A2 limpio; esas fallas consumirían los tres intentos ordinarios y sacarían logs de C1.
   - **El arreglo más chico:** armar el canario de brazo con `fuente.texto(k, "limpio")`. Da 12.831 bytes y cumple el percentil 90 declarado. Corregir también “A2 sobre el pendiente” en §11. Para cerrar completamente cualquier umbral de tamaño, convendría además congelar margen hasta el máximo real.

2. El canario del juez JSON tampoco representa el extremo superior de su familia.

   - **Gravedad:** DEBERÍA
   - **Tipo:** diseño
   - **Dónde:** [corrida2.py:197](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:197).
   - **Evidencia:** el mensaje construido con `piloto.CASOS_JUEZ[0]` mide 1.236 bytes. Reconstruí en memoria los ocho mensajes JSON de los brazos ya hechos del piloto de fase 2: miden entre 1.183 y 1.679 bytes, y cuatro superan al canario. Por lo tanto, un fallo dependiente del tamaño todavía puede afectar llamadas reales mientras el canario termina. Esto no entra en C1, pero puede perder o sesgar la descriptiva del JSON.
   - **El arreglo más chico:** congelar un caso JSON con suficientes textos libres para superar al extremo superior observado —sin depender de las salidas no versionadas del piloto— y agregar una prueba explícita de tamaño.

3. La selección de dependencias del piloto sigue siendo más amplia que el trabajo que realmente las usa.

   - **Gravedad:** DEBERÍA
   - **Tipo:** implementación
   - **Dónde:** [corrida2.py:980](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:980), [corrida2.py:984](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:984), [corrida2.py:988](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:988), [corrida2.py:649](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:649).
   - **Evidencia:** el caso denunciado en la tercera ronda sí quedó cerrado: sin brazos pendientes no se pide Codex ni `jsonschema`. Pero si sólo quedan brazos A0/A1, todavía se exige `jsonschema`, aunque esos brazos no lo usan. Además, cualquier juez pendiente exige Claude, aun si corresponde a un brazo terminal no hecho y `juzgar_item` sólo va a escribir `sin_llamada`, sin llamar al modelo.
   - **El arreglo más chico:** exigir `jsonschema` sólo si queda algún A2/A2b; exigir Claude sólo si algún juez pendiente puede llegar realmente a `claude_con_reintentos`.

4. La receta de congelamiento pasa mecánicamente, pero le faltan dos instrucciones editoriales.

   - **Gravedad:** NOTA
   - **Tipo:** implementación
   - **Dónde:** [01-PROTOCOLO.md:3](/D:/Programacion/Disensor-Docs/experimento/fase2/01-PROTOCOLO.md:3), [01-PROTOCOLO.md:315](/D:/Programacion/Disensor-Docs/experimento/fase2/01-PROTOCOLO.md:315), [01-PROTOCOLO.md:421](/D:/Programacion/Disensor-Docs/experimento/fase2/01-PROTOCOLO.md:421).
   - **Evidencia:** la secuencia C → R → tag sobre C → push satisface `congelamiento_fase2`, `commits_registrados`, el tag remoto y el ancla de `plan_congelado`. Pero el cuerpo actual todavía dice “borrador, NO congelado”; como `cuerpo_del_protocolo` queda fijado en C, eso debe cambiarse en C, no en R. Además, “R sólo agrega” permite dejar `*(ninguna todavía)*` junto al registro, cosa que el parser acepta.
   - **El arreglo más chico:** decir expresamente que C cambia el estado a congelado y que R **reemplaza** `*(ninguna todavía)*` por el registro.

Arreglos de la tercera ronda verificados:

- **Ancla opcional:** bien. `fetch` y `ls-remote` tienen 120 segundos; `GIT_TERMINAL_PROMPT=0` y `GCM_INTERACTIVE=never` se pasan sólo al subproceso Git. `anclar_si_hay_red` conserva las demás comprobaciones de `anclar_en_remoto(..., obligatorio=False)`.
- **Canario ilegible:** bien. Una respuesta Claude terminada, verificada y no vacía cuenta como servicio sano sin pasar por `leer_q28` ni otro lector.
- **Canario por familia:** el cableado está bien: `q28`, `fp` y `json` llegan desde `juzgar_item`; `juez-prueba` pasa `q28`/`fp`; GPT cae en `brazo`. Quedan los dos problemas de tamaño anteriores.
- **Archivos del canario:** los cuatro `mensaje_canario` se construyen correctamente con el repo actual. El GPT canario corre en una carpeta temporal, con sandbox de sólo lectura, y sólo escribe su salida y auditoría bajo `canarios/`; no puede tocar `fase2/corrida/brazos/`, y los chequeos de la corrida no consumen `canarios/`.
- **Dependencias del piloto:** el caso exacto denunciado —reanudar sólo jueces— quedó arreglado; quedan los casos más finos del hallazgo 3.
- **`juez-prueba` y `PARADA`:** bien. Revisa `sin_parada(DIR_PILOTO)` al comenzar y tanto una red de seguridad del juez como una del canario terminan pasando por `cortar`.
- **Congelamiento:** C/R, tag liviano o anotado, publicación del tag, descendencia y ancla de `main` son coherentes entre §11 y el código; queda únicamente la precisión textual del hallazgo 4.

No ejecuté los 48 tests porque necesitan escribir un temporal, ni probé red, credenciales o los CLI reales. Todas las pruebas adicionales fueron imports con `python -B`, sin bytecode y cálculos puros en memoria.

## Consigna de Codex

Sos la cuarta revisión independiente de la **fase 2** de un experimento preregistrado, antes de congelarla. Las tres anteriores las hiciste vos, Codex: `fase2/02-REVISION-1.md`, `fase2/03-REVISION-2.md` y `fase2/04-REVISION-3.md`, con qué se hizo con cada hallazgo. La tercera fue la de los falsos frenos; Claude Code arregló sus cinco hallazgos en `195d00a` y el protocolo pasó a la v4 en `af57b95`. Quedan seis decisiones de diseño para Nico (al final de `02-REVISION-1.md`): no las discutas, salvo que encuentres algo nuevo.

**Actuá como red-team sobre ese diff, no lo apruebes:** `git diff 143bef4..195d00a -- fase2/herramientas` y `git diff 143bef4..af57b95 -- fase2/01-PROTOCOLO.md`. Tres preguntas:

1. **¿Cada arreglo cierra lo que dice `04-REVISION-3.md`?** `anclar_si_hay_red` y `git_remoto` (tiempo máximo, git sin pedir credenciales, que el entorno del sujeto no cambie), el canario por familia (`mensaje_canario`, `canario`, el parámetro `familia` de `revisar_intento` y quién lo pasa), las dependencias del piloto, y `juez-prueba` con `PARADA`.
2. **¿Rompieron algo?** Regresiones y falsos frenos nuevos. Por ejemplo: ¿`anclar_si_hay_red` reproduce lo que hacía `corrida.anclar_en_remoto(..., obligatorio=False)` en todo lo demás (`herramientas/corrida.py`)? ¿`mensaje_canario` puede fallar con los archivos del piloto que hay en el repo (`piloto/logs/003`, `piloto/gemelos/003`, `piloto/chequeo`, `piloto.CASOS_JUEZ`)? ¿Un canario que falla por eso se toma como caída del servicio y frena en falso? ¿Algo del canario de GPT (una llamada real del sujeto sobre un log del piloto) puede tocar `fase2/corrida/brazos/` o un chequeo de la corrida?
3. **¿La receta de congelamiento de §11 es correcta y completa?** Contra `congelamiento_fase2`, `commits_registrados`, `exigir_tag_en_el_remoto`, `plan_congelado` y `corrida.congelamiento_en_git`.

**Reglas de esta sesión:** sólo leés. No escribas, edites, muevas ni borres archivos, ni corras nada que cambie estado (nada de git que escriba, ni `git fetch`; `python -B` con `PYTHONDONTWRITEBYTECODE=1`, sin escribir archivos). Podés usar comandos de lectura y `python -` para importar los módulos y probar funciones puras en memoria. **No abras la prosa de los brazos de la fase 1** (`corrida/brazos/*/prosa.txt` ni sus `intento-*` ni `json.txt`). No hace falta mirar `ayudas/`, `corrida/gemelos/revision-gpt/` ni `corrida/gemelos/PRECHEQUEO-C.md`. No corras `corrida.py`, `corrida2.py` ni `piloto.py` con ninguna etapa. `prueba_offline2.py` necesita un directorio temporal escribible que esta sesión no tiene: pasa 48 de 48 fuera de esta sesión.

**Formato de la respuesta, en castellano:** una lista de hallazgos, del más grave al menos grave. Cada uno con **Gravedad** (BLOQUEANTE si puede tirar una corrida legítima o invalida la confirmatoria, DEBERÍA si conviene arreglarlo antes de congelar, NOTA), **Tipo** (implementación o diseño), **Dónde**, **Evidencia** y **El arreglo más chico**. Después, una línea por cada arreglo de la tercera ronda que verificaste y está bien. Si no encontrás nada, decilo así. Si algo no lo pudiste verificar, decilo.
