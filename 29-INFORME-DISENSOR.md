# Lo que la fase 1 dice de disensor

**14/10/2026.** Lectura del resultado de la fase 1 (`27`) desde disensor: qué
afirmación del proyecto se puso a prueba, qué confirma, qué no, y qué propuestas
salen. Los números son los de `corrida/informe.json`; los datos sobre cómo
escribió A2 salen de mirar sus 200 JSON después del análisis, cuando Nico ya había
visto el resultado.

## Qué se probó, exactamente

- **El esquema, solo.** El fragmento de `residue.schema.json` de disensor en
  `de14e5c` (residue/v0.4), con las reglas R1, R2, R2 bis y R8 de `rules.py`.
- **Sin el método.** Un solo modelo, `gpt-5.6-sol`, escribe la respuesta y el JSON
  en la misma generación. No hay un generador separado del revisor, no hay un
  revisor de otra familia, no hay ronda, no hay gate. Lo que se midió es el piso:
  cuánto hace el esquema por sí solo.
- **Un hueco de ejecución, no un hallazgo de revisión.** Lo que quedó abierto es
  una consulta que se lanzó y no volvió. En disensor eso es un `execution_gap`.

## Lo que respalda

**El esquema hace aparecer lo que quedó abierto, sin inventarlo.** Con el residuo,
el JSON registra el hueco en 29 de 100 logs; con un listado de hallazgos, en 5. En
los 100 gemelos limpios, ninguno de los dos brazos lo registra.

**Cuando el modelo abre residuo, acierta.** En los pendientes, los 29 JSON que
registran el hueco son exactamente los 29 que abrieron ítems de residuo: 25
`execution_gap` y 4 `escalation_without_decision`. La cita del juez sale de la
descripción de un ítem en 24 casos y de un hallazgo en 5. Las descripciones son
precisas: «The asynchronous aggregation including automated warehouse inventory had
no returned result, so its effect on the facility comparison could not be
determined.» En los limpios, un solo JSON abrió un ítem (una
`escalation_without_decision`), y el juez no lo leyó como registro del hueco.

## Lo que no respalda

**La ausencia declarada falla en la mayoría de los casos.** En los pendientes, A2 es
binario: o abre ítems (29) o declara `declared_absence` (71). No hay término medio.
En 71 de 100 logs, con la consulta todavía sin volver, el JSON declaró
expresamente que no quedaba residuo.

**Esas 71 declaraciones pasan todo.** Cumplen el esquema y ninguna falla una regla.
R2 rechaza sólo marcadores genéricos exactos («no residue», «none»), y estas
declaraciones son frases completas. Las fallas de reglas que sí hubo en A2 (11 en
200 JSON) son todas de R1, por la coherencia entre el estado de un hallazgo y sus
ítems, y no tienen que ver con el falso cierre.

**El README ya lo dice, y ahora tiene un número.** «Honest limit, inherited from
the protocol: the machine detects the empty field and the generic marker, not the
false declaration» (`README.md`, línea 424). La fase 1 lo mide: con este sujeto y
un hueco conocido, 71 de 100 declaraciones de ausencia son falsas y el validador
las aprueba.

**Cómo se escriben las ausencias falsas.** Acotan el residuo a su propio trabajo:
35 de las 71 hablan de un cálculo (30 dicen «this calculation») y 12 de lo
que se les dio («supplied»). Por ejemplo: «No unresolved questions or unverified conclusions remain from this
calculation.» El modelo no niega que la consulta haya quedado pendiente; declara
que su cálculo, sobre los datos que tenía, no dejó nada abierto. Una hipótesis, no
probada: el esquema describe el residuo como lo que «el ciclo no pudo cerrar por sí
mismo», y el modelo lee su ciclo como su cálculo, no como la ejecución de la que
dependía.

**`gap_reason` no tiene dónde poner esto.** Los 25 `execution_gap` usaron `other`,
todos con descripción. El enum (`environment_not_reproducible`,
`third_party_no_test_environment`, `other`) no tiene un valor para «una operación
que se lanzó y no volvió».

## Qué significa para lo que disensor dice

- **Se puede decir:** en un experimento controlado y pre-registrado, el esquema de
  residuo hizo que el registro consignara una operación que no volvió cerca de seis
  veces más seguido que un listado de hallazgos (de 5% a 29%), sin falsas alarmas.
- **No se puede decir:** que una declaración de ausencia sea evidencia de que no
  quedó nada abierto. Con un hueco conocido, el 71% de las ausencias fueron falsas.
- **Para el plano de evidencia:** un reporte de cumplimiento no puede contar una
  ausencia declarada como limpia. Tiene que distinguir la ausencia declarada de la
  verificada. Es además un argumento de tasa base para la auditoría aleatoria de
  #96: el muestreo humano que el README nombra como la única defensa real tiene un
  blanco medido.

## Propuestas, en orden

1. **Que lo observable no quede a la declaración del modelo.** Si el registro del
   evento muestra una operación lanzada sin resultado (un revisor que no contestó o
   cortó por tiempo, un check de CI pendiente al declarar, una prueba que no
   corrió), la ausencia no valida y hace falta un `execution_gap`. Es la idea que
   disensor ya aplica a los modos degradados del revisor
   (`reviewer_hardening_gap`, `reviewer_correlation`), llevada a toda operación que
   el arnés ve. No cubre lo que el arnés no ve, pero cierra la parte mecánica del
   falso cierre.
2. **Un valor de `gap_reason` para una operación que no volvió.** Candidato para
   residue/v0.5, junto a #51, #52 y #53. Hoy esos casos caen en `other`.
3. **Que la ausencia diga qué cubre.** La declaración de ausencia es una frase libre,
   y el modelo la acota a su cálculo. Dos caminos para discutir: pedir que nombre
   su alcance (el razonamiento, la ejecución, los datos), o reemplazar la frase por
   afirmaciones estructuradas que se puedan contrastar una por una («toda operación
   lanzada devolvió su resultado», «todo hallazgo tiene un estado terminal»). Es
   un cambio de esquema; va como discusión.
4. **El número en el README.** Agregar a «Honest limit» el dato y el enlace al
   experimento, y revisar que la landing y el paper no sugieran que la ausencia
   declarada vale como verificación.
5. **Ausencia declarada frente a verificada en el plano de evidencia**, y la tasa
   base en la discusión de #96.
6. **El experimento que falta: el método entero.** La fase 1 midió el esquema solo.
   La pregunta de disensor es otra: si un revisor de otra familia, en una ronda,
   atrapa el falso cierre que el generador declara. Se puede correr sobre los
   mismos 100 pares congelados: el generador declara, un revisor de otra familia
   ataca, y se mide cuántas de las 71 ausencias falsas sobreviven. Y una segunda
   variante con la regla mecánica de la propuesta 1, para ver cuánto cierra sola.

## El experimento como caso del método

El protocolo y el arnés pasaron por ocho revisiones antes de congelar: tres de
Claude y cinco de Codex, de otra familia. Las cinco de Codex trajeron 16, 14, 8, 5 y
9 hallazgos (las dos últimas cifras cuentan las dos trampas de la séptima). Claude
Code los verificó contra el código antes de aceptarlos: la mayoría se confirmó; el
hallazgo 7 de la cuarta revisión se rechazó con un contraejemplo, y algunas partes
de otros también. Claude Code encontró además dos errores que ninguna revisión
había visto.

Las rondas de Codex usaron unos 12,1 millones de tokens de entrada, casi lo mismo
que la corrida entera (12,9 millones). La curva bajó (16, 14, 8, 5) hasta que la
séptima cambió la pregunta (qué puede frenar en falso, en vez de qué puede dejar
pasar) y volvió a encontrar cosas. Es un dato para #114: en un trabajo donde un
error descarta la corrida, la revisión cuesta lo mismo que lo revisado, y la
pregunta que se le hace al revisor importa tanto como cuántas rondas se hacen.

Por la política del 25 de agosto, estas rondas no dejaron declaración de residuo.
