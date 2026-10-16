# Tercera revisión de la fase 2: Codex, los arreglos de la segunda y los falsos frenos

**16/10/2026.** Codex revisó los arreglos de la segunda ronda (`01514bd..fa37a16`) y,
como pide §14, hizo la pregunta de los falsos frenos sobre todo el arnés de la fase 2,
igual que la séptima ronda de la fase 1: si el código de verificación puede frenar
una corrida legítima. El mismo binario, el mismo `CODEX_HOME` aislado, sólo lectura
con `windows.sandbox=unelevated` y esfuerzo `high`. 27 comandos de lectura, ningún
archivo cambiado, `git status` limpio después; ninguno abrió la prosa de la fase 1 (el
único que la nombra la excluye de una búsqueda). Uso: 2.211.275 tokens de entrada
(2.096.512 de caché) y 35.632 de salida, en 880 segundos. Tres falsos frenos y dos
agujeros; los arreglos de la segunda ronda, verificados, y una receta de
congelamiento que pasa siempre.

**Verificado por Claude Code contra el código:** los cinco se confirman.

| Hallazgo | Qué se hizo |
|---|---|
| Falso freno 1: después de crear el plan, el `git fetch` del ancla opcional (de la fase 1) corre sin tiempo máximo y puede quedarse esperando credenciales | La fase 2 vuelve a anclar con su propia función, `anclar_si_hay_red`: tiempo máximo de 120 segundos y git sin preguntar nada (`GIT_TERMINAL_PROMPT=0`, `GCM_INTERACTIVE=never`). Un remoto que no contesta es un aviso. El `ls-remote` del tag, también con tiempo máximo. Las variables van sólo a esas llamadas de git: puestas en el entorno del proceso le llegarían también al sujeto, que tiene que correr con el arnés de la fase 1 sin cambios. |
| Falso freno 2: una respuesta del canario de Claude que no se lee como veredicto se tomaba como caída del servicio | El canario anda si termina con una respuesta; no se mira qué dice. Una salida que no se lee es una falla del juez. |
| Falso freno 3: reanudar el piloto pedía Codex y `jsonschema` aunque sólo faltaran los jueces | Cada dependencia, sólo si queda trabajo que la usa. |
| Agujero 1 (BLOQUEANTE, según Codex): un solo canario por CLI, de tamaño medio, no cubre una falla que dependa de la familia o del tamaño de la llamada | El canario es de la misma familia que el intento que falló (brazo, Q.2.8, falsos positivos o juez del JSON), sobre el log 003 del piloto, el de log y gemelo más largos de los del piloto con gemelo (3.043 y 4.206 bytes), por encima del percentil 90 de los logs de la corrida, con una respuesta fija de 666 caracteres para los jueces de la prosa. El del juez del JSON usa el caso de prueba de la fase 1, que es del log 000. |
| Agujero 2: `juez-prueba` no miraba una `PARADA` y una red de seguridad del juez no la dejaba | Mira `PARADA` al empezar, y una red de seguridad o un corte por cupo pasan por `cortar`. |

Y un detalle que salió al probar: dos canarios en el mismo milisegundo se pisaban el
registro; ahora el nombre es único.

`prueba_offline2.py`: 48 de 48; ocho mutaciones que deshacen estos arreglos, y las
ocho hacen fallar alguna prueba. La fase 1 sigue en 142 de 142. El protocolo pasa a
la v4: §11 con el canario por familia, el ancla sin red y la receta de congelamiento.

Lo que sigue es la respuesta **textual** de Codex y su consigna.

---

## Respuesta de Codex

No congelaría todavía: encontré tres falsos frenos corregibles y dos agujeros separados. Los otros tres arreglos de la segunda ronda cierran; el canario cierra sólo parcialmente.

## Hallazgos

1. El chequeo remoto “opcional” puede quedar bloqueado después de empezar la corrida.

   - **Gravedad:** DEBERÍA
   - **Tipo:** implementación
   - **Dónde:** [corrida.py:501](/D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:501), [corrida.py:590](/D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:590), [corrida2.py:421](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:421).
   - **El caso legítimo que frena:** después de crear el plan, `jueces`, `validacion` y `analizar` deberían continuar sin red. Eso ocurre si `git fetch` devuelve un error, pero `corrida.git` ejecuta Git sin timeout y heredando la interacción. En Windows, una conexión colgada o Git Credential Manager pidiendo renovar credenciales puede impedir indefinidamente que se alcance la rama que imprime el aviso y continúa. Es especialmente caro en `validacion` o `analizar`.
   - **Evidencia:** `anclar_en_remoto(..., obligatorio=False)` tolera correctamente un código de salida no cero, pero `subprocess.run` no tiene timeout ni modo no interactivo. `git ls-remote` sólo se usa antes del plan; el riesgo tardío es el `fetch` opcional.
   - **El arreglo más chico:** hacer sólo el chequeo posplan mediante un wrapper local de fase 2 con timeout y Git no interactivo (`GIT_TERMINAL_PROMPT=0` y credenciales no interactivas). Sin cambiar código, cancelar el diálogo o renovar las credenciales permite reanudar.

2. Una respuesta sana pero ilegible del canario de Claude se declara “servicio caído”.

   - **Gravedad:** DEBERÍA
   - **Tipo:** diseño
   - **Dónde:** [corrida2.py:187](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:187), [corrida2.py:206](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:206), [prueba_offline2.py:666](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/prueba_offline2.py:666), §11.
   - **El caso legítimo que frena:** una llamada real no termina; el canario sí termina, verificado y con texto, pero Claude devuelve una salida que `leer_q28` no reconoce. El servicio contestó, pero el intento real se marca `caida`, la etapa para y a la tercera queda `PARADA`. Una salida semánticamente ilegible normalmente se trata como falla del juez, no como caída de infraestructura.
   - **Evidencia:** el test exige expresamente que una respuesta `"OK"` terminada dé `False`; la condición final es `leer_q28(texto) is not None`.
   - **El arreglo más chico:** para salud del servicio exigir `termino`, `verificado` y texto no vacío, sin exigir un veredicto Q.2.8. Actualizar la frase correspondiente de §11.

3. La etapa combinada `piloto` exige dependencias de llamadas que ya terminaron.

   - **Gravedad:** DEBERÍA
   - **Tipo:** implementación
   - **Dónde:** [corrida2.py:899](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:899).
   - **El caso legítimo que frena:** los brazos del piloto ya son terminales y sólo faltan jueces o armar el análisis, pero Codex fue actualizado/no está disponible o falta `jsonschema`. La reanudación se detiene en `verificar_binarios(... ambos ...)` o `exigir_jsonschema()` antes de comprobar qué trabajo falta. Restaurar el entorno lo resuelve, pero esas dependencias no intervienen en el trabajo pendiente.
   - **Evidencia:** las verificaciones están en las líneas 904–908, antes de recorrer brazos y jueces; los propios `correr_brazo` y `juzgar_item` sí retornan inmediatamente ante resultados terminales.
   - **El arreglo más chico:** calcular primero brazos y jueces pendientes; exigir Codex/`jsonschema` sólo si queda algún brazo y Claude sólo si queda algún juez.

## Trampas que el arnés todavía deja pasar

1. El único canario por CLI todavía puede dar un falso “anda” sistemático.

   - **Gravedad:** BLOQUEANTE
   - **Tipo:** diseño
   - **Dónde:** [corrida2.py:177](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:177), [corrida2.py:211](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:211).
   - **El agujero:** todos los fallos de Codex usan un A2 fijo y todos los de Claude usan un Q.2.8 fijo, sin considerar el tipo o tamaño de la llamada fallida. Un límite o fallo dependiente del tamaño/contenido puede dejar terminar el canario y hacer que los intentos reales lleguen a `fallo` terminal. Si afecta los jueces FP, C1 puede quedar sin ningún log evaluable.
   - **Evidencia:** medí sin abrir prosas experimentales: el GPT canario tiene 11.035 bytes, contra A2 reales de 10.803–15.054; el Claude canario tiene 5.352, contra Q.2.8 de 5.051–6.067 y FP de 4.863–8.825 aun usando una respuesta fija de sólo cuatro bytes. El juez JSON es además otra familia de prompt. El tope de tres no ayuda porque sólo cuenta falsos `caida`; si el canario termina, los fallos reales se consumen normalmente.
   - **El arreglo más chico:** pasar a `revisar_intento` la familia de llamada y usar canarios congelados representativos del extremo superior para GPT, Q.2.8, FP y juez JSON.

2. `juez-prueba` puede seguir después de una red de seguridad sin revisión.

   - **Gravedad:** DEBERÍA
   - **Tipo:** implementación
   - **Dónde:** [corrida2.py:854](/D:/Programacion/Disensor-Docs/experimento/fase2/herramientas/corrida2.py:854).
   - **El agujero:** la etapa no llama `sin_parada(DIR_PILOTO)`. Una `PARADA` producida por un canario se ignora al reejecutarla. Además, si la llamada del juez devuelve `PARADA`, la línea 885 sólo hace `sys.exit`: no crea el marcador; la siguiente ejecución descarta ese historial porque sólo reutiliza `juzgado` o `juez_fallo`.
   - **El arreglo más chico:** llamar `sin_parada(DIR_PILOTO)` al comienzo y encaminar `v["estado"] == "PARADA"` por `cortar`.

## Verificado y sin falso freno

- **Canario de tamaño real:** el mensaje dejó de ser diminuto; sus tamaños caen dentro de la distribución real. Queda el agujero de cobertura señalado arriba.
- **Tope por ítem:** las caídas quedan persistidas y la tercera crea `PARADA`; Claude cambia la etiqueta y GPT marca `sin_cupo` sin consumir los tres intentos ordinarios.
- **Tag remoto:** acepta correctamente tags livianos y anotados —usa el commit pelado— y rechaza tag ausente o movido.
- **Prosa por condición:** `largo_de_la_prosa` quedó bajo `pendiente` y `limpio`, sólo sobre llamadas `hecho`; no encontré consumidores del formato agregado anterior.
- **Receta de congelamiento:** pasa si se hace un commit `C` con código, prompts y cuerpo final del protocolo; luego un commit `R` que agrega en «Enmiendas» el registro de `C`; el tag se crea explícitamente sobre `C`, no sobre `R`; finalmente se empujan `main` —conteniendo `R`— y el tag antes de `brazos`.
- **CRLF y Unicode:** `registro_fase2` y `cuerpo_del_protocolo` dieron exactamente lo mismo con LF, CRLF y la tilde en NFD/NFC.
- **Clon limpio:** un clon completo normal obtiene el tag y conserva los bytes por `* -text`; un clon `--no-tags` debe traer el tag y uno superficial es rechazado deliberadamente.
- **Red al crear el plan:** `fetch` y `ls-remote` son obligatorios antes de la primera llamada; un fallo ahí no pone en riesgo una corrida empezada. Después no vuelve a ejecutarse `ls-remote`.
- **Rama e historia:** HEAD igual al ancla o descendiente pasa; otra rama no descendiente frena. `git -G` recibe argumentos directos, sin interpretación de PowerShell.
- **Resultados terminales adversos:** `fallo`, `sin_llamada`, `juez_fallo`, `fallo_verificacion` e `interrumpido` llegan a `armar_pares` y al análisis como exclusiones, sin convertirlos en negativos.
- **JSON ilegible:** queda con `json_md5=None`; el juez JSON devuelve “no registra” sin llamada y la comparación `None == None` es válida.
- **Prosa vacía:** se puede juzgar, se audita con largo cero y la planilla muestra `(vacía)`; no encontré un traceback.
- **Análisis con terminales mixtos:** lo probé en memoria; produjo C1 no evaluable y la exclusión correspondiente, sin reventar.
- **`jueces` reanudado:** los terminales se omiten y `en_curso`/`sin_cupo` conservan lecturas e intentos.
- **`validacion` repetida:** regenera determinísticamente pares, clave y planillas, pero no pisa archivos de etiquetas existentes, incluidos los parcialmente completados.
- **`analizar` con etiquetas parciales:** frena antes de C1 con la cantidad faltante. Ejecutarlo sin haber corrido siquiera `validacion` puede dar un `FileNotFoundError`, pero no escribe el informe ni altera resultados.
- **`canarios/` y `PARADA`:** no entran en los glob de resultados ni en `armar_pares`; sólo se leen rutas esperadas bajo `brazos/` y `jueces/`.

No ejecuté `prueba_offline2.py`, clones temporales ni CLI reales por la restricción de escritura. Tampoco pude observar el comportamiento concreto del gestor de credenciales vencidas; el riesgo indicado surge de que Git se ejecuta interactivo y sin timeout. No abrí ninguna prosa prohibida y el estado del repositorio quedó igual que al inicio.

## Consigna de Codex

Sos la tercera revisión independiente de la **fase 2** de un experimento preregistrado, antes de congelarla. Las dos anteriores las hiciste vos, Codex (la primera junto con un agente de Claude): `fase2/02-REVISION-1.md` y `fase2/03-REVISION-2.md`, con qué se hizo con cada hallazgo. La segunda trajo cuatro; Claude Code arregló tres en `fa37a16` y el protocolo pasó a la v3 en `9f22316`. Quedan seis decisiones de diseño para Nico (al final de `02-REVISION-1.md`): no las discutas, salvo que encuentres algo nuevo.

**Esta ronda tiene dos partes.**

**1. Los arreglos de la segunda ronda** (`git diff 143bef4~3..fa37a16 -- fase2/herramientas`): el canario de tamaño real (`mensaje_canario`, `canario`), el tope de caídas por ítem en `revisar_intento`, `exigir_tag_en_el_remoto` en `plan_congelado` y el largo de la prosa por condición. ¿Cierran lo que dicen? ¿Rompieron algo?

**2. Los falsos frenos, sobre todo el arnés de la fase 2.** Hasta ahora se buscó sobre todo que el arnés no deje pasar una trampa. La pregunta al revés: ¿puede el código de verificación frenar una corrida legítima? §10 dice que un cambio de código después de la primera llamada descarta la corrida entera, así que un falso freno que aparezca recién en `jueces`, `validacion` o `analizar` es caro: arreglarlo cambia el árbol y obliga a tirar la corrida. Actuá como red-team sobre esa pregunta: casos borde, supuestos sobre git, Windows, rutas, codificaciones, el orden de las etapas, las reanudaciones, la red. Lo que hay que mirar: `fase2/herramientas/corrida2.py` entero (`congelamiento_fase2`, `commits_registrados`, `cuerpo_del_protocolo`, `registro_fase2`, `exigir_tag_en_el_remoto`, `exigir_descendencia`, `plan_congelado`, `verificar`, `revisar`, `exigir_misma_fuente`, `veredicto`, `armar_pares`, `revisar_intento`, `canario`, cada `etapa_*`), lo que usa de la fase 1 (`herramientas/corrida.py`: `congelamiento_en_git`, `anclar_en_remoto`, `gpt_con_reintentos`, `leer_incluidos`, `texto_de_entrada`; `herramientas/piloto.py`: `claude_con_reintentos`, `cerrar_intentos_en_vuelo`, `una_llamada_claude`, `una_llamada_gpt`, `juzgar`), y §0, §10 y §11 de `fase2/01-PROTOCOLO.md`. Ejemplos de lo que buscamos (no te limites a estos):
- El congelamiento hecho a mano, como lo describe §11: el orden de los commits (código y protocolo, el registro en un commit posterior, el tag, el push), un registro con CRLF o con la tilde en otra forma Unicode, el tag anotado o liviano, un clon limpio después. ¿Hay una secuencia legítima que no pase? ¿Se puede escribir en §11 una receta que pase siempre?
- `git ls-remote` sin red o con credenciales vencidas al crear el plan; después, sin red: ¿frena una etapa que debería poder seguir?
- Un brazo `fallo`, un juez `sin_llamada`, `juez_fallo`, `interrumpido` o `fallo_verificacion`, un JSON ilegible, una prosa vacía: ¿algo de `revisar`, `armar_pares`, `analisis2.analizar` o las planillas revienta o frena con eso?
- Correr `jueces` dos veces, `validacion` dos veces (con las etiquetas a medio llenar), `analizar` antes de que estén las etiquetas, y la etapa `piloto` reanudada.
- `canarios/` y `PARADA` dentro de `fase2/corrida/`: ¿algún chequeo los lee como resultados?

**Reglas de esta sesión:** sólo leés. No escribas, edites, muevas ni borres archivos, ni corras nada que cambie estado (nada de git que escriba, ni `git fetch`; `python -B` con `PYTHONDONTWRITEBYTECODE=1`, sin escribir archivos). Podés usar comandos de lectura y `python -` para importar los módulos y probar funciones puras en memoria. **No abras la prosa de los brazos de la fase 1** (`corrida/brazos/*/prosa.txt` ni sus `intento-*` ni `json.txt`). No hace falta mirar `ayudas/`, `corrida/gemelos/revision-gpt/` ni `corrida/gemelos/PRECHEQUEO-C.md`. No corras `corrida.py`, `corrida2.py` ni `piloto.py` con ninguna etapa. `prueba_offline2.py` necesita un directorio temporal escribible que esta sesión no tiene: pasa 44 de 44 fuera de esta sesión.

**Formato de la respuesta, en castellano:** una lista de hallazgos, del más caro al menos caro. Cada uno con **Gravedad** (BLOQUEANTE si puede tirar una corrida legítima o invalida la confirmatoria, DEBERÍA si frena pero se resuelve sin cambiar código o conviene arreglarlo antes de congelar, NOTA), **Tipo** (implementación o diseño), **Dónde**, **El caso legítimo que frena** (o el agujero), con la evidencia, y **El arreglo más chico**. Si encontrás una trampa que el arnés deja pasar, ponela aparte, al final. Después, una línea por cada cosa que verificaste y no frena en falso. Si algo no lo pudiste verificar, decilo.
