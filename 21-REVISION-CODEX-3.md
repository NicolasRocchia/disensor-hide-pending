# Quinta revisión independiente, por Codex, sobre el diff de la v20

**13/10/2026.** Por decisión de Nico, una ronda más antes de congelar. La hizo
`gpt-5.6-sol` por Codex CLI 0.153.4 (el `codex.exe` fijado), con el `CODEX_HOME`
aislado de §7.1, en sólo lectura con `windows.sandbox=unelevated`, y esfuerzo
`high`, sobre el diff `969ce35..925a162`. 29 comandos de lectura, ningún archivo
cambiado, `git status` limpio después; el único comando que nombra `piloto/humo`
es el que lo excluye. Uso: 2.636.841 tokens de entrada (2.503.680 de caché) y
30.998 de salida, en 659 segundos.

**Verificado por Claude Code antes de aceptarlo**, contra el código:

- **Confirmados los ocho.** 1: `validacion` y `analizar` no llaman al
  congelamiento. 2: borrar `brazos/plan.json` lo regenera, el commit de la lista
  no se exige en el protocolo y no se mira ningún remoto. 3: el `HEAD` de cada
  llamada se guarda pero no se compara. 4: la regla del juez mira sólo las claves
  excluidas, no el formato del valor. 5: la historia no se revisa al empezar
  (intentos agotados, red de seguridad) y los archivos de un intento se escriben
  antes de registrarlo. 6: con las dos correlaciones, el limpio comparte con
  probabilidad ρ·((1−ρc)² + ρc²). 7: con N=0, `analizar` sale antes de validar
  las etiquetas. 8: la expresión del `request_id` toma prefijos.
- **Con evidencia en contra, una parte del 4:** descartar todo string bajo una
  clave contenedora (`"residue": "…"`) haría que A2 pierda un registro escrito ahí
  mientras A2b, donde `residue` es una clave desconocida, lo conserva. Se
  descartan por su formato (hashes, links, fechas, ids), no por su clave. Y el
  filtro de valores de enum se queda: un valor que es exactamente un token del
  esquema (`execution_gap`) no es una frase, y delata al residuo.

Lo que se haga con cada hallazgo va en la v21 del protocolo (§15).

Lo que sigue es su respuesta **textual**, y después la consigna que recibió.

---

Encontré tres bloqueantes y cinco fallas adicionales. No congelaría la v20 así.

## Hallazgos

1. **Gravedad: BLOQUEANTE.**  
   **Dónde:** [corrida.py:526](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:526), [corrida.py:740](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:740), [corrida.py:810](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:810), §4.4.  
   **Qué está mal:** el congelamiento deja de comprobarse después de `juez`. `validacion` y `analizar` no llaman a `congelamiento_en_git`; `leer_incluidos` sólo verifica que el archivo coincida con el `.md5` mutable mediante `.strip()`.  
   **Escenario de falla:** después de terminar el juez y ver indicadores o resultados, se reemplaza `pares-incluidos.json` por un subconjunto favorable de los pares ya corridos y se recalcula su sidecar. `validacion` reconstruye `pares.json` con ese subconjunto y `analizar` comprueba contra esa misma lista adulterada: todo pasa sin commit ni reescritura de historia. Tampoco se exige allí que sigan siendo 100 pares.  
   **El arreglo más chico:** llamar a `congelamiento_en_git()` al principio de `validacion` y `analizar`, exigir exactamente 100 entradas y que `pares.json` registre y coincida con el commit congelado.

2. **Gravedad: BLOQUEANTE.**  
   **Dónde:** [corrida.py:483](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:483), [corrida.py:509](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:509), [corrida.py:516](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:516), [corrida.py:582](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:582), §4.4, líneas 355–372.  
   **Qué está mal:** “un solo commit en la historia” significa sólo la historia alcanzable desde la rama actualmente checkout. Tras resultados parciales se puede volver al commit anterior al congelamiento, crear otra rama, commitear allí una lista distinta una sola vez y pushear esa rama: no se reescribió ni borró la historia original. El código tampoco verifica que el hash del commit esté anotado en «Enmiendas»: busca únicamente el md5 como subcadena en cualquier lugar del protocolo. `plan.json`, que sería el único recuerdo del commit original, es mutable y queda fuera del control de git; borrarlo permite regenerarlo.  
   **Escenario de falla:** se conservan las carpetas de respuestas de los pares convenientes, se crea una rama alternativa con otra lista, se borra `brazos/plan.json` y se reanuda. Las respuestas conservadas se saltean y sólo se llaman los pares nuevos. La nueva rama también tiene una historia de una sola modificación y puede pushearse sin force-push. Además, actualmente `git remote -v` no devuelve ningún remoto, y el arnés no verifica push alguno.  
   **El arreglo más chico:** registrar y parsear el commit esperado junto al md5 en «Enmiendas»; antes de la primera llamada, commitear un plan que fije lista y commit; rechazar cualquier resultado existente cuyo commit de lista no coincida. Si el push va a ser el ancla externa, exigir un remoto/ref concreto y protegido. Un push ordinario no “cubre” por sí solo una historia reescrita ni una rama alternativa.

3. **Gravedad: BLOQUEANTE.**  
   **Dónde:** [corrida.py:519](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:519), [corrida.py:523](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:523), [corrida.py:586](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:586), [corrida.py:606](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:606), §0 y §10.  
   **Qué está mal:** se exige que el código esté commiteado, pero no que sea el mismo commit durante toda la corrida. El plan fija sólo `commit_de_la_lista`; cada llamada agrega el `HEAD` actual a `commits`, pero jamás lo compara con los anteriores.  
   **Escenario de falla:** después de 50 pares se cambia `herramientas/`, un esquema o un prompt, se commitea y se reanuda. `congelamiento_en_git` pasa: no hay cambios sucios y la lista sigue teniendo un solo commit. La mitad de los brazos corre con una implementación y la otra mitad con otra, pese a que §10 obliga a descartar la corrida si un cambio relevante ocurre después de ver resultados.  
   **El arreglo más chico:** fijar en `plan.json` el `HEAD` —o los hashes de los árboles normativos— de la primera llamada y rechazar cualquier diferencia mientras existan resultados. Una enmienda anterior a la primera llamada puede producir un plan nuevo; una posterior requiere otra corrida. El `.md5` con salto final sí está bien: el escritor lo agrega y `leer_incluidos` usa `.strip()`.

4. **Gravedad: DEBERÍA.**  
   **Dónde:** [juez.py:25](D:/Programacion/Disensor-Docs/experimento/herramientas/juez.py:25), [juez.py:60](D:/Programacion/Disensor-Docs/experimento/herramientas/juez.py:60), §6.2 líneas 594–617 y §12.11.  
   **Qué está mal:** `CAMPOS_DE_PROSA` no participa en la extracción. La implementación sólo pregunta si la clave está en `CLAVES_EXCLUIDAS`; por eso una clave conocida como contenedor, pero escrita con tipo incorrecto, se trata como prosa. También cualquier clave inventada deja pasar hashes, URLs, fechas o identificadores, contradiciendo “sin hashes, links, fechas ni ids”. Finalmente, el filtro global `obj not in fijos` elimina valores válidos de campos de prosa cuando coinciden con un enum. Reproduje:

   - `{"residue":"sha256:000…","findings":[]}` → el hash llega al juez.
   - `{"evidence":"https://only-a2.example/item"}` → el link llega.
   - `{"sha256":"sha256:111…"}` → el hash bajo clave inventada llega.
   - `{"description":"execution_gap"}` → la prosa desaparece.

   Esto importa porque el cumplimiento de esquema es sólo descriptivo: esos JSON legibles siguen entrando en C2.  
   **Escenario de falla:** A2 escribe `residue` como string o usa un nombre alternativo para el hash; el juez recibe un texto exclusivo o un formato revelador del brazo. En sentido contrario, el único texto relevante queda en `description: "pending_in_diff_gate"` y se cuenta como “sin textos libres”.  
   **El arreglo más chico:** hacer operativas tres categorías: campos de prosa, campos no textuales y contenedores. Un string sólo pasa si su clave está en `CAMPOS_DE_PROSA`, o si la clave es realmente desconocida y el valor no tiene formato técnico reconocible. Quitar la exclusión global por valor de enum: los enums ya quedan excluidos por su clave.

5. **Gravedad: DEBERÍA.**  
   **Dónde:** [corrida.py:77](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:77), [piloto.py:693](D:/Programacion/Disensor-Docs/experimento/herramientas/piloto.py:693), [piloto.py:316](D:/Programacion/Disensor-Docs/experimento/herramientas/piloto.py:316), [piloto.py:674](D:/Programacion/Disensor-Docs/experimento/herramientas/piloto.py:674), §7.7.  
   **Qué está mal:** los prechequeos sólo detectan un intento previo exitoso; no detectan cupos ya agotados. En memoria pasé tres fallas GPT persistidas y la función hizo una cuarta llamada. Pasé dos terminaciones Claude no verificadas y realizó una tercera antes de devolver `fallo_verificacion`. Además, la salida cruda se escribe antes de agregar el intento al resumen: un corte entre esas operaciones pierde igualmente el intento y el próximo arranque pisa sus archivos.  
   **Escenario de falla:** el tercer intento GPT falla, se guarda y el proceso cae antes de guardar `estado="fallo"`; al volver recibe un cuarto. Lo mismo después del segundo no verificado o tercero no terminado de Claude. Un corte después de escribir el stream pero antes del callback también concede otra oportunidad. Tras una red de seguridad ocurre lo contrario de un falso `interrumpido`: el intento se ignora y, una vez borrada `PARADA`, se llama otra vez.  
   **El arreglo más chico:** antes del bucle, devolver `fallo`, `fallo_verificacion` o `PARADA` si la historia ya alcanzó esos estados. Persistir un marcador de intento “iniciado” antes de lanzar el proceso; si queda sin registro final al reanudar, tratarlo conservadoramente como `interrumpido` o reconstruirlo de los artefactos existentes.

6. **Gravedad: DEBERÍA.**  
   **Dónde:** [analisis.py:163](D:/Programacion/Disensor-Docs/experimento/herramientas/analisis.py:163), §6.4 líneas 733–748.  
   **Qué está mal:** la bandera compartida corrigió el pendiente, pero `rho_condiciones` sobrescribe luego el uniforme limpio por separado en cada brazo. Con ambas correlaciones positivas, los brazos ya no comparten el limpio con probabilidad `rho_brazos`. La probabilidad efectiva es aproximadamente  
   `rho_brazos × ((1-rho_condiciones)² + rho_condiciones²)`.  
   Medí 0,3466 para `rho_brazos=0,6`, `rho_condiciones=0,3`, y 0,3146 para 0,6/0,6, no 0,6. La prueba sólo cubre el pendiente con `rho_condiciones=0`.  
   **Escenario de falla:** las celdas se presentan como correlaciones 0,6 entre brazos, aunque el limpio comparte apenas 31–35% de los sorteos. Además, la salida publicada tiene una fila que pasa de 50% a 58% al variar sólo `rho_condiciones`; “casi no la mueve” no es fiel a esa salida. Con 20.000 réplicas obtuve 51,8% frente a 55,9%, así que no es únicamente el ruido de 1.000 réplicas.  
   **El arreglo más chico:** usar un modelo conjunto coherente —por ejemplo, una cópula con correlaciones definidas— o describir estos parámetros como probabilidades de dos mecanismos secuenciales y publicar sus correlaciones efectivas. Después, regenerar la grilla y suavizar la frase sobre condiciones.

7. **Gravedad: NOTA.**  
   **Dónde:** [analisis.py:296](D:/Programacion/Disensor-Docs/experimento/herramientas/analisis.py:296), [analisis.py:316](D:/Programacion/Disensor-Docs/experimento/herramientas/analisis.py:316), §8.1.  
   **Qué está mal:** `analizar` retorna antes de verificar las etiquetas si ningún par quedó incluido. Puede haber una muestra no vacía formada por llamadas juzgadas de logs luego excluidos, pero `analizar(pares, [])` no frena, pese a que §8.1 afirma que una lista vacía o parcial siempre frena. La ruta oficial de `corrida.py` sí la valida antes.  
   **Escenario de falla:** todos los logs se excluyen porque falta una de sus cuatro llamadas, pero existen numerosos veredictos en las otras llamadas; el CLI directo omite toda la validación humana y devuelve C2 no evaluable. No crea una afirmación positiva, pero incumple el contrato nuevo.  
   **El arreglo más chico:** validar `items_de_la_planilla` antes del retorno de N=0, o documentar expresamente la excepción.

8. **Gravedad: NOTA.**  
   **Dónde:** [gemelos.py:95](D:/Programacion/Disensor-Docs/experimento/herramientas/gemelos.py:95), §12.9.  
   **Qué está mal:** `request[ _-]?id` detecta prefijos, no necesariamente un identificador. Coincide con “request identity” y “request-idle”.  
   **Escenario de falla:** un gemelo dice “request identification is disabled” sin conservar identificador alguno y entra en el estrato “con request_id”. Sólo afecta una descriptiva.  
   **El arreglo más chico:** exigir un límite después de `id`, por ejemplo `(?![A-Za-z0-9])`, y agregar esos negativos a la prueba.

## Estado de los 14 hallazgos de la cuarta revisión

1. **Cerrado:** la recalculada adicional usa sólo los decisivos y evita la compensación de la muestra.  
2. **A medias:** se excluyeron las claves técnicas previstas, pero los contenedores mal tipados, las claves inventadas y el filtro global de enums dejan caminos incorrectos. La razón para excluir `origin` se sostiene como contrato semántico del esquema; la cita trivial también se sostiene como decisión mecánica respaldada por la revisión humana de todos los decisivos.  
3. **Cerrado:** la nula ahora declara invariancia conjunta e independencia entre logs como supuesto.  
4. **Abierto:** el congelamiento puede alterarse después del juez, cambiarse en otra rama sin reescritura y no fija el código durante la corrida.  
5. **Cerrado:** la planilla usa los textos almacenados y comprueba el md5 del mensaje cuando hubo llamada.  
6. **Cerrado para la afirmación original; con una salvedad:** listas vacías/parciales frenan cuando hay incluidos, pero N=0 retorna antes de esa validación.  
7. **Abierto por decisión:** el contenedor truncado todavía deja pasar el objeto interior. La razón sí se sostiene contra el arreglo ingenuo: confirmé que seguir cualquier `[` ocultaría el JSON posterior a “Regions [standard, regional”.  
8. **A medias:** se guarda cada intento terminado, pero todavía hay ventanas y estados agotados que habilitan otra llamada.  
9. **A medias:** `rho_brazos` funciona aisladamente, pero deja de tener el significado declarado al combinarlo con `rho_condiciones`. La razón para conservar “un poco conservadora” sí se sostiene para el tamaño de la prueba independiente.  
10. **Cerrado:** `--objetivo` no baja de 110, el piloto incluye fallas en el denominador y el sorteo agotado ya no pide más logs.  
11. **A medias:** se inspecciona el bloque nuevo y se cubren `request_id`, `requestId` y “request id”, pero la regex tiene falsos positivos de prefijo.  
12. **Cerrado:** la hoja no trunca el alcance y la metadata se verifica por md5.  
13. **Cerrado:** se corrigieron las frases viejas sobre JSON y sensibilidad.  
14. **Cerrado:** todos los caminos GPT relevantes guardan un `tipo` explícito.

## Verificaciones que dieron bien

- La sensibilidad con etiquetas sólo en decisivos detecta el caso de compensación de la revisión anterior.
- Un decisivo sin textos igualmente aparece entre los cuatro ítems de la planilla; no se omite por no haber llamado al juez.
- La segunda vuelta del juez usa `juez-2` y no dispara `interrumpido` por el éxito de `juez-1`.
- La planilla reutiliza los textos del veredicto y reconstruye el mismo `mensaje_md5`.
- La definición textual de la nula ya no confunde simetría marginal con invariancia conjunta.
- El sidecar escrito con salto de línea se acepta correctamente mediante `.strip()`.
- Los números independientes reproducidos son 84,4%, 79,2%, 77,6%, 98,9%, 44,9% y 86,9%.
- Con brazos iguales, la salida es 3,1%, 3,6% y 3,7%; “un poco conservadora” describe correctamente esos tamaños discretos.
- La primera fila correlacionada imprime efectivamente 83% sin correlación y 96–97% con `rho_brazos=0,6`.
- La metadata se verifica tanto antes de llamar al armador como al construir la hoja completa.
- El detector de `request_id` cubre las formas positivas declaradas.
- No corrí `prueba_offline.py`, conforme a la consigna; no verifiqué localmente el “131 de 131”.
- No ejecuté el ataque con ramas ni pushes porque requeriría cambiar estado; se desprende del alcance de `git log`, del plan mutable y de la ausencia de verificación remota.
- No abrí respuestas ni eventos de humo, ni sesiones guardadas, ni hice llamadas a modelos.
- El worktree permaneció limpio.

---

## La consigna

Sos la quinta revisión independiente de un protocolo experimental, la última antes de congelarlo. La tercera y la cuarta las hiciste vos, Codex: `16-REVISION-CODEX.md` (sobre la v18) y `19-REVISION-CODEX-2.md` (sobre el diff de la v19, 14 hallazgos). Claude Code los corrigió como v20, con una decisión del autor del experimento (Nico) sobre el juez. **Tu tarea es atacar el diff de la v20: que cada arreglo cierre de verdad lo que decía tu hallazgo, que no haya metido fallas nuevas, y que las razones para no aceptar algunos puntos se sostengan.** Actuá como red-team: atacá supuestos, agujeros, riesgos y casos borde. No aprobás nada; buscás fallas.

**Reglas de esta sesión:** sólo leés. No escribas, edites, muevas ni borres archivos, ni corras nada que cambie estado (nada de git que escriba, nada de `python` que escriba archivos; usá `PYTHONDONTWRITEBYTECODE=1` y `python -B`). Podés usar comandos de lectura (`rg`, `Get-Content`, `git log`, `git show`, `git diff`) y `python -` para importar los módulos de `herramientas/` y probar funciones puras en memoria. **No abras las respuestas de la prueba de humo** (`piloto/humo/*/intento-*-ultimo-mensaje.md`, `piloto/humo/*/intento-*-eventos.jsonl` ni la sesión guardada en `%USERPROFILE%\ch\sessions`). No corras `piloto.py` ni `corrida.py` con ninguna etapa (llaman a modelos). `prueba_offline.py` necesita un directorio temporal escribible que esta sesión no tiene: no hace falta que la corras (pasa 131 de 131 fuera de esta sesión).

**El diff a atacar:** `git diff 969ce35..HEAD` (commits `4ae9c6a` código y pruebas, `91a147b` protocolo v20 y `07`, `925a162` informe `20-RESPUESTA-A-LA-REVISION-2.md`). La tabla que cruza tus 14 hallazgos con lo que se hizo está en `01-PROTOCOLO.md`, §15, «De la v19 a la v20».

**Decisión de Nico, tomada (no la relitigues; sí decí si su implementación tiene un agujero):** para el hallazgo 2, el juez ve una lista de campos, no una llamada por texto. La regla está en `juez.CLAVES_EXCLUIDAS` y `juez.CAMPOS_DE_PROSA`, y en §6.2. La cantidad y el contenido de los textos quedan declarados como limitación 11 de §12.

**Lo que Claude Code no aceptó, con su razón (atacá la razón si no se sostiene):**
- Hallazgo 7 (contenedores sin cerrar): seguir la anidación sobre texto que no parsea haría que un corchete suelto de la prosa escondiera un JSON válido que viene después; queda declarado en §6.1.
- `origin` como texto libre (parte del 2): el esquema la define como «reviewer_id of the reviewer that produced it».
- La guarda que acepta una cita trivial (parte del 2): mecánica por diseño desde la v14; lo semántico lo controla §8.1.
- «Es un poco conservadora» en §6.4 (parte del 9): habla del tamaño de la prueba, no del supuesto de independencia.

**Atacá en especial:**
1. **El congelamiento nuevo** (`corrida.congelamiento_en_git`, §4.4): ¿se puede burlar sin reescribir la historia? ¿Frena algo legítimo (por ejemplo, una enmienda posterior al protocolo, o el `.md5` con salto de línea)? ¿El push como cobertura de la historia reescrita está bien dicho?
2. **El estado `interrumpido`** (`gpt_con_reintentos`, `piloto.claude_con_reintentos`, `piloto.juzgar`, `corrida.etapa_juez`): ¿hay un camino normal que lo dispare por error (por ejemplo, después de una red de seguridad, de un `fallo_verificacion`, o en la segunda vuelta del juez)? ¿Un corte de golpe todavía puede dar una segunda oportunidad?
3. **La sensibilidad con los decisivos solos y las etiquetas exactas** (`analisis.analizar`): ¿se puede esquivar o disparar mal? ¿Qué pasa si un decisivo no tiene textos (no llamó al juez)?
4. **La lista de claves del juez**: ¿hay una clave de los esquemas mal clasificada, o una forma de JSON que el sujeto pueda escribir y que la regla trate mal?
5. **La grilla rehecha** (`analisis.uniformes_de_un_log`): ¿modela ahora lo que dice §6.4? ¿La frase de §6.4 es fiel a la salida de `python -B herramientas/analisis.py potencia`? (Tarda unos minutos; no escribe archivos.)
6. **Fallas nuevas** en el diff: caminos sin prueba, diferencias entre el texto de la v20 y el código.

**Formato de la respuesta, en castellano:** una lista de hallazgos, del más grave al menos grave. Cada uno con:
- **Gravedad:** BLOQUEANTE (no se puede congelar así), DEBERÍA (corregir antes de congelar) o NOTA.
- **Dónde:** archivo y línea, o sección del protocolo.
- **Qué está mal**, con la evidencia que leíste (citá lo justo).
- **Escenario de falla:** qué dato o qué caso lleva a un resultado equivocado.
- **El arreglo más chico.**

Al final, una línea por cada uno de tus 14 hallazgos de la cuarta revisión diciendo si quedó cerrado, a medias o abierto (y, para los no aceptados, si la razón se sostiene), y una línea por cada cosa que verificaste y está bien. Si algo no lo pudiste verificar, decilo.
