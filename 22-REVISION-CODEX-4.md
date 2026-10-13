# Sexta revisión independiente, por Codex, sobre el diff de la v21

**13/10/2026.** Una ronda corta, por decisión de Nico, antes de congelar. La hizo
`gpt-5.6-sol` por Codex CLI 0.153.4 (el `codex.exe` fijado), con el `CODEX_HOME`
aislado de §7.1, en sólo lectura con `windows.sandbox=unelevated`, y esfuerzo
`high`, sobre el diff `ec6cad4..84a8838`. 22 comandos de lectura, ningún archivo
cambiado, `git status` limpio después; el único comando que nombra `piloto/humo`
es el que lo excluye. Uso: 1.845.341 tokens de entrada (1.703.296 de caché) y
23.716 de salida, en 493 segundos.

**Verificado por Claude Code antes de aceptarlo**, contra el código: los cinco
se confirman. 1: el árbol inicial vive sólo en `plan.json`, y la v21 aceptaba un
árbol nuevo si su md5 aparecía en el protocolo, en contra de §10.1 («si aparece
un bug, la corrida se descarta entera»). 2: los veredictos del juez no guardaban
la lista ni el JSON que juzgaron. 3: el md5, el commit y el árbol se buscaban en
cualquier lugar del protocolo. 4: `git branch -r --contains` mira referencias
locales. 5: reproducido en memoria, «Pending.» y «Unavailable?» salían técnicos, y
«sha256: abcdef», una fecha con espacio y un link con espacio pasaban.

Lo que se hizo con cada hallazgo va en la v22 del protocolo (§15).

Lo que sigue es su respuesta **textual**, y después la consigna que recibió.

---

Encontré dos bloqueantes y tres fallas adicionales.

1. **Gravedad: BLOQUEANTE**

   **Dónde:** [corrida.py:550](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:550), [corrida.py:575](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:575), [corrida.py:638](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:638), [01-PROTOCOLO.md:375](D:/Programacion/Disensor-Docs/experimento/01-PROTOCOLO.md:375), [01-PROTOCOLO.md:1227](D:/Programacion/Disensor-Docs/experimento/01-PROTOCOLO.md:1227), [prueba_offline.py:1226](D:/Programacion/Disensor-Docs/experimento/herramientas/prueba_offline.py:1226).

   **Qué está mal:** el árbol inicial se conserva solamente en `corrida/brazos/plan.json`, que sigue siendo mutable y no está anclado en git. `revisar_plan` confía en `plan["arbol_md5"]`; no contrasta los `arboles` ya guardados en los resultados. Cambiar ese campo al árbol actual evita incluso la supuesta necesidad de una enmienda. Alternativamente, el código autoriza cualquier árbol cuyo hash aparezca en cualquier parte del protocolo. La propia prueba nueva confirma como válido cambiar código y continuar después de agregar el hash. Esto contradice directamente §10.1: ante un bug visto después de resultados, la corrida se descarta entera.

   **Escenario de falla:** se corren 50 pares con árbol A; se modifica y commitea `herramientas/`; se cambia sólo `arbol_md5` del plan existente a B, sin fabricar resultados ni usar otra rama. Como los resultados viejos conservan el mismo `commit_de_la_lista` y sus `arboles` no se revisan, `brazos` continúa con B. Queda una corrida mezclada A/B que pasa `validacion` y `analizar`.

   **El arreglo más chico:** anclar en un archivo commiteado el árbol de la primera llamada y exigir igualdad exacta desde que exista cualquier resultado. Una modificación posterior exige corrida nueva, como dice §10.1. Las enmiendas que sólo cambian el protocolo siguen siendo legítimas porque no alteran `arbol_normativo`.

2. **Gravedad: BLOQUEANTE**

   **Dónde:** [corrida.py:550](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:550), [corrida.py:714](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:714), [corrida.py:805](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:805).

   **Qué está mal:** el congelamiento sólo inspecciona `brazos/*/resumen.json`. Los resultados del juez no guardan `commit_de_la_lista`, y un veredicto terminal se saltea antes de comprobar o agregar el árbol actual. `validacion` reconstruye el mensaje usando los `textos` almacenados por ese mismo juez, no volviendo a derivarlos del JSON actual; por eso la comprobación de `mensaje_md5` es autoconsistente aunque el veredicto sea viejo.

   **Escenario de falla:** parte del juez termina con árbol A; se cambia `juez.py`, se autoriza B por el agujero anterior y se reanuda. Los veredictos terminales A se saltean y los restantes corren con B. También puede sobrevivir un veredicto de otra lista para un log compartido aunque los brazos hayan sido vueltos a correr para la lista actual.

   **El arreglo más chico:** guardar en cada resumen del juez el commit de lista, árbol normativo y `json_md5` fuente; comprobarlos contra el brazo actual antes del `continue` terminal y nuevamente en `verificar_corrida`. Reextraer los textos del `json.txt` actual para verificar el mensaje.

3. **Gravedad: DEBERÍA**

   **Dónde:** [corrida.py:529](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:529), [corrida.py:556](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:556), §4.4 y `## Enmiendas`.

   **Qué está mal:** no se parsea «Enmiendas». El md5 de la lista, su commit y los árboles se aceptan si aparecen como subcadena en cualquier lugar de `01-PROTOCOLO.md`. La prueba sólo cubre ausencia total, no un hash ubicado fuera de la sección correcta.

   **Escenario de falla:** se agrega el árbol nuevo a §15, a una nota o a cualquier texto sin fecha ni motivo. `revisar_plan` lo trata como enmienda válida. Un hash de árbol anotado por una enmienda antigua también autoriza volver a ese código en cualquier momento.

   **El arreglo más chico:** parsear exclusivamente `## Enmiendas` y exigir registros estructurados que distingan lista, commit y árbol, con fecha y motivo. Agregar negativos con los mismos hashes fuera de esa sección.

4. **Gravedad: DEBERÍA**

   **Dónde:** [corrida.py:534](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:534), §4.4 y §12.12.

   **Qué está mal:** `git branch -r --contains` consulta referencias remotas locales, no el remoto. Un remoto recién agregado que ya contiene el commit da falso negativo hasta hacer `fetch` o `push`; una referencia obsoleta puede dar falso positivo después de que el remoto haya borrado o reescrito la rama. Además, la prueba usa un repositorio bare local, que pasa aunque §4.4 dice que el ancla no debe depender de esta máquina.

   **Escenario de falla:** se configura el remoto público después de que otro clon ya pusheó el commit: el congelamiento frena pese a que el commit existe. A la inversa, `origin/main` queda cacheada después de un force-push remoto y el chequeo sigue pasando.

   **El arreglo más chico:** fijar remoto y ref concretos, rechazar URLs locales para el ancla externa y verificar/fetchear esa ref antes de evaluar `--contains`. Documentar que configurar sin `fetch` no alcanza.

5. **Gravedad: DEBERÍA**

   **Dónde:** [juez.py:42](D:/Programacion/Disensor-Docs/experimento/herramientas/juez.py:42), [juez.py:76](D:/Programacion/Disensor-Docs/experimento/herramientas/juez.py:76), §6.2.

   **Qué está mal:** `es_tecnico` confunde puntuación con formato técnico y sólo reconoce formatos técnicos sin espacios. Reproduje en memoria:

   - `"Pending."` y `"Unavailable?"` se eliminan, aunque son frases que contestan directamente la pregunta del juez.
   - `"sha256: abcdef"`, `"2026-10-13 10:00:00Z"`, `"https://example.test/a b"` y `"req abc"` pasan.
   - Por tanto, no se cumple la afirmación de que no llegan hashes, links, fechas ni ids.

   La función es la misma para ambos brazos y la decisión sobre claves contenedoras sí quedó simétrica. No obstante, si los brazos difieren en estilo —por ejemplo, `Pending.` frente a `Pending`— el filtro convierte esa diferencia superficial en una diferencia de resultado.

   **Escenario de falla:** A2 escribe `declaration: "Pending."`; el único texto positivo desaparece y cuenta como «no registra». A2b escribe `description: "Pending"` y llega al juez. En sentido contrario, un id con espacio llega y puede revelar formato o brazo.

   **El arreglo más chico:** reconocer formatos concretos —hash, URL, fecha e id— aun con espacios opcionales, y decidir si una cadena es palabra después de retirar puntuación terminal. Agregar pruebas para frases de una palabra con `.?!` y formatos técnicos con espacios.

### Estado de los ocho hallazgos de la quinta

1. **Cerrado:** `validacion` y `analizar` vuelven a comprobar el congelamiento y `leer_incluidos` exige 100 entradas.
2. **A medias:** se frena la regeneración del plan con resultados de brazos y éstos guardan la lista, pero los resultados del juez no; el remoto tampoco se verifica realmente.
3. **Abierto:** todavía se puede cambiar código a mitad de la corrida, incluso editando sólo el árbol del plan.
4. **A medias:** se filtran los formatos compactos previstos, pero se pierde prosa con puntuación y pasan formatos técnicos con espacios.
5. **Cerrado:** los límites, la red de seguridad y el marcador en vuelo se revisan antes de llamar.
6. **Cerrado:** las dos probabilidades de compartir conservan ahora su significado simultáneamente.
7. **Cerrado:** las etiquetas se validan antes del retorno con N=0.
8. **Cerrado:** los falsos positivos de sufijo señalados (`request identity`, `request-idle`, `request identification`) ya no coinciden.

### Verificaciones que dieron bien

- Una enmienda commiteada que sólo toca el protocolo no cambia `arbol_normativo`; puede continuar legítimamente.
- Borrar `plan.json` cuando hay resultados de brazos frena; el agujero es modificar su árbol, no borrarlo.
- Un resultado de brazo cuyo `commit_de_la_lista` difiere frena.
- Una excepción o `SystemExit` dentro de `una_llamada_gpt` deja persistido el marcador en vuelo; `cortar` se ejecuta después de reemplazarlo por el registro real.
- Los cortes por cupo siguen siendo reanudables y no consumen el cupo de tres intentos.
- `intento-1-*` no confunde `intento-1` con `intento-10`; cubre los nombres que escriben ambas funciones. La ventana anterior a la primera escritura cuenta como intento no terminado, sin exceder el límite.
- La grilla completa dio exactamente los números publicados: primera fila 83%→97%, quinta 47%→54% al variar condiciones, y brazos iguales 2,7%–3,0%.
- En 200.000 sorteos con ρ=0,6/0,3 medí 0,603 y 0,601 de compartición entre brazos, y 0,299 de repetición pendiente–limpio en ambos brazos.
- La descripción de §6.4 es fiel a `python -B herramientas/analisis.py potencia`.
- El filtro trata una frase bajo `residue` igual en ambos brazos y conserva la decisión de excluir los tokens exactos del esquema.
- `git diff --check` no encontró errores y el worktree quedó limpio.
- No abrí respuestas/eventos de humo ni sesiones guardadas, ni ejecuté etapas de `piloto.py` o `corrida.py`.
- No ejecuté `prueba_offline.py`; no pude verificar localmente los 136/136 por la restricción de escritura.
- No pude probar un remoto recién configurado sin modificar estado; el repositorio actual no tiene remotos.

---

## La consigna

Sos la sexta revisión independiente de un protocolo experimental, una ronda corta antes de congelarlo. La quinta la hiciste vos, Codex (`21-REVISION-CODEX-3.md`, 8 hallazgos sobre el diff de la v20). Claude Code los corrigió como v21. **Tu tarea es atacar sólo el diff de la v21: que cada arreglo cierre lo que decía tu hallazgo y que no haya metido fallas nuevas.** Actuá como red-team: atacá supuestos, agujeros, riesgos y casos borde. No aprobás nada; buscás fallas. No vuelvas sobre lo que ya quedó cerrado o aceptado en la quinta.

**Reglas de esta sesión:** sólo leés. No escribas, edites, muevas ni borres archivos, ni corras nada que cambie estado (nada de git que escriba; `python -B` con `PYTHONDONTWRITEBYTECODE=1`, sin escribir archivos). Podés usar comandos de lectura y `python -` para importar los módulos de `herramientas/` y probar funciones puras en memoria. **No abras las respuestas de la prueba de humo** (`piloto/humo/*/intento-*-ultimo-mensaje.md`, `piloto/humo/*/intento-*-eventos.jsonl` ni `%USERPROFILE%\ch\sessions`). No corras `piloto.py` ni `corrida.py` con ninguna etapa. `prueba_offline.py` necesita un directorio temporal escribible que esta sesión no tiene: pasa 136 de 136 fuera de esta sesión.

**El diff a atacar:** `git diff ec6cad4..HEAD` (commits `2f58e2a` código y pruebas, `84a8838` protocolo v21 y `07`). La tabla de lo que se hizo con cada hallazgo de la quinta está en `01-PROTOCOLO.md`, §15, «De la v20 a la v21»; lo que no se aceptó del hallazgo 4, y por qué, está ahí y en el encabezado de `21-REVISION-CODEX-3.md`.

**Atacá en especial:**
1. **El congelamiento de la v21** (`corrida.congelamiento_en_git`, `revisar_plan`, `verificar_corrida`, `plan_congelado`, `arbol_normativo`, §4.4 y limitación 12 de §12): ¿frena algo legítimo (una enmienda posterior al protocolo que no toca el código, los resultados de `juez` frente al árbol, `git branch -r --contains` con el remoto recién configurado)? ¿Queda alguna forma de reusar resultados de otra lista o de cambiar el código a mitad de la corrida sin fabricar archivos ni usar otra rama?
2. **El intento «en vuelo»** (`piloto.INTENTO_EN_VUELO`, `cerrar_intentos_en_vuelo`, `claude_con_reintentos`, `corrida.gpt_con_reintentos`): ¿hay un camino normal que deje un intento en vuelo sin un corte (una excepción de `una_llamada_*`, un `sys.exit` de `cortar`)? ¿El glob de archivos `intento-N-*` puede dar un falso positivo o negativo? ¿La revisión previa de la historia rompe la reanudación tras un corte por cupo?
3. **El filtro de valores técnicos del juez** (`juez.es_tecnico`, `RE_PALABRA`): ¿saca algo que es una frase, o deja pasar algo técnico? ¿Afecta distinto a un brazo que al otro?
4. **La grilla** (`analisis.uniformes_de_un_log`): ¿modela ahora lo que dice §6.4? ¿La frase de §6.4 es fiel a `python -B herramientas/analisis.py potencia`? (Tarda unos minutos.)
5. **Fallas nuevas** en el diff: caminos sin prueba, diferencias entre el texto de la v21 y el código.

**Formato de la respuesta, en castellano:** una lista de hallazgos, del más grave al menos grave. Cada uno con **Gravedad** (BLOQUEANTE, DEBERÍA o NOTA), **Dónde**, **Qué está mal** con la evidencia, **Escenario de falla** y **El arreglo más chico**. Al final, una línea por cada uno de los 8 hallazgos de la quinta (cerrado, a medias o abierto) y una línea por cada cosa que verificaste y está bien. Si algo no lo pudiste verificar, decilo.
