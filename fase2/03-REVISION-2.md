# Segunda revisión de la fase 2: Codex sobre los arreglos de la primera

**16/10/2026.** Por la regla de la fase 1 (cada arreglo después de una ronda pide
otra), Codex revisó el diff de los arreglos de la primera ronda (`e9425de..853e134`
y el protocolo v2, `33d748d`), con la consigna de atacarlos: si cierran lo que dice
`02-REVISION-1.md`, si rompieron algo y si quedó algo afuera. El mismo binario, el
mismo `CODEX_HOME` aislado, sólo lectura con `windows.sandbox=unelevated` y esfuerzo
`high`. 23 comandos de lectura, ningún archivo cambiado, `git status` limpio después;
ninguno abrió la prosa de la fase 1. Uso: 2.130.780 tokens de entrada (2.000.512 de
caché) y 23.013 de salida, en 466 segundos. Cuatro hallazgos; de los arreglos de la
primera ronda, todos verificados y bien.

**Verificado por Claude Code contra el código:**

| Hallazgo | Qué se hizo |
|---|---|
| 1 (BLOQUEANTE, según Codex): la frase de C1 no significativa no mira si el juez es confiable, y «quedó fuera del informe» | **No es así:** está en la decisión 2 de `02-REVISION-1.md` («Codex 6 y 7»), porque cambia el texto de §9, que hoy dice «como en la fase 1», y la fase 1 hace lo mismo. Sigue para Nico. |
| 2 (BLOQUEANTE): el canario era un mensaje diminuto, no miraba la respuesta, y las caídas repetidas no tenían límite | El canario es ahora un pedido del tamaño de los reales, sobre el log 000 del piloto: A2 sobre el pendiente para GPT, Q.2.8 con una respuesta fija para Claude. Cuenta como que anda sólo si termina con una respuesta, y en Claude si esa respuesta se lee como veredicto. A la tercera caída en un mismo ítem, el arnés deja `PARADA` y no sigue hasta que Nico la revise. |
| 3: el tag se verificaba sólo en local | Al crear el plan, con el ancla obligatoria, el tag tiene que estar publicado en el remoto y apuntar al commit del registro (el commit pelado, si es anotado). |
| 4: el largo de la prosa no salía por condición | Sale por brazo y condición, como el resto de §2.2. |

`prueba_offline2.py`: 44 de 44; siete mutaciones que deshacen estos arreglos, y las
siete hacen fallar alguna prueba. El protocolo pasa a la v3, con §11 al día.

Lo que sigue es la respuesta **textual** de Codex y su consigna.

---

## Respuesta de Codex

No la congelaría todavía. Encontré dos bloqueantes y dos problemas que conviene corregir antes del congelamiento.

1. El resultado nulo sigue afirmándose aunque la validación declare al juez no confiable; este hallazgo de la primera ronda quedó fuera del informe de resolución.

   - **Gravedad:** BLOQUEANTE
   - **Tipo:** implementación
   - **Dónde:** [analisis2.py](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/analisis2.py:385), especialmente líneas 388–400; [01-PROTOCOLO.md](/D:/Programacion/Disensor-Docs/experimento/fase2/01-PROTOCOLO.md:273).
   - **Evidencia:** `frase()` devuelve inmediatamente «no detectamos un efecto» cuando C1 no es significativa, antes de mirar `validacion["juez_no_confiable"]`. Lo reproduje en memoria con 40 pares nulos y cuatro desacuerdos en un estrato de 15: `significativa=False`, `juez_no_confiable=True`, pero la frase empieza «no detectamos un efecto». Es el hallazgo 7 de Codex de la primera ronda. No aparece en «Arreglados», «No se tocaron» ni las seis decisiones. El cambio sí hizo que la coincidencia se calcule con N=0, pero no corrigió la decisión de la frase.
   - **El arreglo más chico:** en `frase`, después de comprobar que hay etiquetas, evaluar `juez_no_confiable` antes de la rama significativa/no significativa. Con juez no confiable, tanto un resultado positivo como uno nulo debe decir que C1 no se afirma.

2. El canario cierra sólo parcialmente la falla sistemática: puede dar falso «anda», falso «caída» y admite reanudaciones ilimitadas.

   - **Gravedad:** BLOQUEANTE
   - **Tipo:** diseño
   - **Dónde:** [corrida2.py](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:176), líneas 176–224; [corrida.py](/D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:89), líneas 89–123; [piloto.py](/D:/Programacion/Disensor-Docs/experimento/herramientas/piloto.py:734), líneas 734–782.
   - **Evidencia:** el canario usa un mensaje diminuto y considera éxito únicamente `reg["termino"]`; ni verifica que la respuesta sea `OK` ni ejercita el tamaño de los pedidos reales. Un servicio que acepte mensajes mínimos pero rechace sistemáticamente los pedidos reales por longitud, carga o alguna ruta dependiente del contenido hará que todos los canarios den «anda» y que los intentos reales lleguen a `fallo` terminal. En sentido contrario, un único timeout aleatorio del canario convierte una falla ordinaria del ítem en `caida`, regala el intento y frena la etapa. Además, al marcar GPT como `sin_cupo` o cambiar en Claude `q28-1` a `q28-1-caida`, cada reanudación vuelve a tener cero intentos contables: no existe ningún límite acumulado. La propia prueba nueva repite cuatro caídas y espera cuatro entradas `q28-1-caida`, demostrando el bucle posible.
   - **El arreglo más chico:** exigir que el canario devuelva exactamente `OK`, agregar un canario congelado representativo del tamaño/ruta de los pedidos reales y persistir un umbral de caídas consecutivas que, sin volver terminal al ítem, cambie el mensaje a «requiere decisión de Nico» en vez de seguir ofreciendo reanudación indefinida.

3. El tag se comprueba sólo localmente; el arnés permite empezar sin haberlo publicado.

   - **Gravedad:** DEBERÍA
   - **Tipo:** implementación
   - **Dónde:** [corrida2.py](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:300), líneas 300–302 y 368–375; [corrida.py](/D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:590), líneas 590–617; [01-PROTOCOLO.md](/D:/Programacion/Disensor-Docs/experimento/fase2/01-PROTOCOLO.md:302).
   - **Evidencia:** `rev-parse refs/tags/...^{commit}` sólo mira el tag local. El ancla remota verifica que los commits sean ancestros de `FETCH_HEAD`, pero nunca que `origin` publique el tag. Por lo tanto, un tag creado únicamente en la máquina de la corrida pasa; un clon limpio posterior no tendrá ese tag y frenará. El resto del mecanismo sí resiste un congelamiento rehecho con otro commit: `git log -G` se invoca con argumentos directos, funciona en Windows, inspecciona los snapshots seleccionados y acumula los commits nombrados. La corrección de una errata del árbol conserva un solo commit nombrado; reemplazarlo por otro deja dos.
   - **El arreglo más chico:** durante el anclaje remoto obligatorio, consultar `git ls-remote --tags origin` para el tag y su `^{}` y exigir que el commit pelado sea el registrado.

4. El largo de la prosa no se informa por condición, contra la nueva redacción de §2.2.

   - **Gravedad:** DEBERÍA
   - **Tipo:** implementación
   - **Dónde:** [analisis2.py](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/analisis2.py:239), líneas 239–259; [01-PROTOCOLO.md](/D:/Programacion/Disensor-Docs/experimento/fase2/01-PROTOCOLO.md:95).
   - **Evidencia:** `largo_de_la_prosa` mezcla en un único conjunto las prosas pendientes y limpias de cada brazo. Los bloques descriptivos por `pendiente` y `limpio` sí separan auditoría, legibilidad, esquema, reglas y juez, pero no el largo. §2.2 ahora exige esas descriptivas «por brazo y condición». Los restantes denominadores revisados son correctos: auditoría sobre llamadas `hecho`, esquema/reglas sobre JSON legibles, cierre sobre JSON legibles con `residue`, rescate sólo con veredicto JSON y C2 sólo con sus cuatro veredictos.
   - **El arreglo más chico:** mover `_largos` al bloque de cada condición y calcularlo sobre `hechas`; opcionalmente conservar el agregado conjunto con otro nombre si se desea.

Arreglos de la primera ronda verificados y bien:

- **Red de seguridad:** `revisar_intento` no consulta sesión ni canario cuando el intento trae `red_de_seguridad`; la `PARADA` queda a cargo del arnés heredado.
- **GPT sin sesión/caída:** el intento recibe `sin_cupo=True`, por lo que `gpt_con_reintentos` no lo cuenta.
- **Chequeo inicial de sesión:** fue eliminado de `brazos`, `jueces`, piloto y `juez-prueba`; los ítems que no requieren modelo no quedan frenados.
- **Fuente de cada veredicto:** `revisar`, `juzgar_item`, `veredicto` y `armar_pares` comparan `fuente_md5`. Un brazo `fallo`, un `sin_llamada` y un JSON ilegible pasan legítimamente con `None == None`; una prosa o JSON rehechos no.
- **Estado del juez JSON:** se conserva en `juez_json`; C2, tasas y rescate no convierten `juez_fallo` en negativo.
- **Esquema, reglas y cierre:** se transportan `cumple_esquema`, `cumple_reglas` y `tiene_residue`; los cierres usan `is True` y el denominador de fase 1.
- **Descriptivas sin pruebas:** los cuatro contrastes y C2 repetida usan `_sin_prueba`; no publican `p` ni `significativa`.
- **Intervalos de sensibilidades:** ambas sensibilidades pasan por `_c1` e incluyen `ic95_bootstrap`.
- **Lector de jueces:** busca el último objeto de nivel superior con `score` y `category`; en pruebas puras coincidió con la regla de `extraccion.ultimo_objeto_con`, incluidos objetos posteriores incompletos y arreglos.
- **Sin análisis provisional:** `corrida2 analizar` exige las dos planillas completas y ya no acepta `--sin-etiquetas`.
- **Información de las planillas:** Q.2.8 recibe la misma metadata en juez y planilla; los fragmentos textuales de ambas rúbricas se extraen correctamente de los prompts congelados y no contienen marcadores, nombres de brazo ni `Be honest`.
- **`jsonschema`:** se comprueba antes de la primera llamada de brazos y piloto, y su versión queda registrada en los resultados.
- **Ids desconocidos:** `leer_etiquetas` los rechaza con el mensaje del arnés antes de indexar `clave`.
- **Cuenta de validación:** imprime únicamente el total de ítems.
- **Tabla 5:** el informe incorpora los valores de A0/A1, N=200 y la aclaración de que son contexto.
- **Auditoría de extracción:** vacío, objeto con `findings`/`residue` y mención de JSON se cuentan correctamente por brazo y condición.
- **Textos de §2.2, §11, §12 y §16:** reflejan los módulos heredados, el criterio 6/6, «omite/matiza» y las cotas con reintentos.
- **Limitaciones declaradas:** quedaron explicitadas la exclusión diferencial y la ceguera sólo formal de las planillas.

No pude ejecutar el congelamiento real ni probar un clon limpio porque la fase 2 todavía no tiene registro ni tag. Tampoco repetí `prueba_offline2.py`: respeté la restricción de no crear un temporal y tomé como dato los 43/43 informados. No ejecuté los CLI reales ni abrí ninguna prosa prohibida. El estado de trabajo quedó igual que al empezar.

## Consigna de Codex

Sos la segunda revisión independiente de la **fase 2** de un experimento preregistrado, antes de congelarla. La primera la hiciste vos, Codex, en paralelo con un agente de Claude: `fase2/02-REVISION-1.md` tiene los 38 hallazgos de las dos, qué se hizo con cada uno y seis decisiones de diseño que quedan para Nico. Claude Code arregló los de implementación en `853e134` y pasó el protocolo a la v2 en `33d748d`. El diff de esos arreglos es `git diff e9425de..853e134 -- fase2/herramientas` y el del protocolo `git diff e9425de..33d748d -- fase2/01-PROTOCOLO.md`.

**Actuá como red-team sobre el diff, no lo apruebes.** Tres preguntas:

1. **¿Cada arreglo arregla lo que dice el informe?** Para cada fila de «Arreglados» de `02-REVISION-1.md`, si el código nuevo cierra el hallazgo de verdad, del todo o a medias.
2. **¿Los arreglos rompieron algo?** Regresiones, casos borde nuevos y, sobre todo, falsos frenos: desde la v2, un cambio de código después de la primera llamada descarta la corrida, así que un freno de más que aparezca recién en `jueces`, `validacion` o `analizar` es caro. Mirá en especial:
   - `canario` y `revisar_intento`: ¿un canario puede dar un falso «caída» o un falso «anda»? ¿Marcar `sin_cupo` en GPT o cambiar la `etiqueta` en Claude interactúa mal con `gpt_con_reintentos`, `claude_con_reintentos` o `cerrar_intentos_en_vuelo` de la fase 1 (`herramientas/corrida.py` y `herramientas/piloto.py`)? ¿Puede haber un bucle de reanudaciones sin fin?
   - `congelamiento_fase2`, `commits_registrados`, `cuerpo_del_protocolo`, el tag y `exigir_descendencia`: ¿`git log -G` hace lo que se supone en Windows y con la historia real de este repo? ¿Un congelamiento legítimo, hecho como dice §11, pasa? ¿Un clon limpio pasa? ¿Se puede rehacer un congelamiento sin que se vea?
   - `exigir_misma_fuente` en `revisar` y `armar_pares`: ¿hay un resultado legítimo que no pase (un brazo `fallo` sin md5, un juez `sin_llamada`, un JSON ilegible)?
   - `armar_pares`, `auditar_prosa` y las descriptivas nuevas de `analisis2.py`: ¿los denominadores y las cuentas son los que dice §2.2?
   - Las planillas con la rúbrica textual y la metadata: ¿algo delata el brazo? ¿`rubrica_textual` puede fallar con los prompts congelados?
   - `jueces2.ultimo_objeto_con_todas` contra `extraccion.ultimo_objeto_con`.
3. **¿Algo de la primera ronda quedó afuera sin decirlo?** Sin volver a discutir las seis decisiones de diseño, salvo que encuentres algo nuevo sobre ellas.

**Reglas de esta sesión:** sólo leés. No escribas, edites, muevas ni borres archivos, ni corras nada que cambie estado (nada de git que escriba, ni `git fetch`; `python -B` con `PYTHONDONTWRITEBYTECODE=1`, sin escribir archivos). Podés usar comandos de lectura y `python -` para importar los módulos y probar funciones puras en memoria. **No abras la prosa de los brazos de la fase 1** (`corrida/brazos/*/prosa.txt` ni sus `intento-*` ni `json.txt`). No hace falta mirar `ayudas/`, `corrida/gemelos/revision-gpt/` ni `corrida/gemelos/PRECHEQUEO-C.md`. No corras `corrida.py`, `corrida2.py` ni `piloto.py` con ninguna etapa. `prueba_offline2.py` necesita un directorio temporal escribible que esta sesión no tiene: pasa 43 de 43 fuera de esta sesión. `fase2/piloto/` tiene los brazos de un piloto (§12 permite leerlos), pero no hace falta.

**Formato de la respuesta, en castellano:** una lista de hallazgos, del más grave al menos grave. Cada uno con **Gravedad** (BLOQUEANTE si invalida la confirmatoria o puede tirar una corrida legítima, DEBERÍA si conviene arreglarlo antes de congelar, NOTA), **Tipo** (implementación o diseño), **Dónde** (archivo y línea), **Evidencia** (qué leíste o probaste) y **El arreglo más chico**. Después, una línea por cada arreglo de la primera ronda que verificaste y está bien. Si algo no lo pudiste verificar, decilo.
