# Séptima revisión independiente, por Codex: los falsos frenos de la v22

**13/10/2026.** Por decisión de Nico, una ronda enfocada antes de congelar, con la
pregunta inversa a las anteriores: si el código de verificación puede frenar una
corrida legítima, que desde la v22 obliga a descartarla (§10.1). La hizo
`gpt-5.6-sol` por Codex CLI 0.153.4 (el `codex.exe` fijado), con el `CODEX_HOME`
aislado de §7.1, en sólo lectura con `windows.sandbox=unelevated`, y esfuerzo
`high`, sobre la v22 (`9cec941`). 45 comandos de lectura, ningún archivo
cambiado, `git status` limpio después; ningún `git fetch`; el único comando que
nombra `piloto/humo` es el que lo excluye. Uso: 1.359.353 tokens de entrada
(1.252.096 de caché) y 25.616 de salida, en 526 segundos.

**Verificado por Claude Code antes de aceptarlo**, contra el código: los siete
hallazgos y las dos trampas se confirman. 1: `escribir_json` usaba `write_bytes`,
que trunca antes de escribir. 2: el `fetch` era obligatorio en las cuatro etapas.
3: `verificar_binarios` exigía los dos binarios en todas. 4: `diff --quiet` y
`ls-files` leían cualquier código distinto de cero como «cambió», y un `git log`
fallido como historia vacía. 5: `leer_json` decodificaba UTF-8 estricto. 6:
Claude Code lo había visto mientras corría la ronda (CRLF); Codex agregó la tilde
en NFD. 7: el «listo» del juez no miraba si faltaban veredictos. Las trampas: un
`arboles` vacío pasaba `any(...)`, y sólo se exigía en el remoto el commit de la
lista.

Lo que se hizo con cada hallazgo va en la v23 del protocolo (§15).

Lo que sigue es su respuesta **textual**, y después la consigna que recibió.

---

Encontré un bloqueante, cinco falsos frenos corregibles sin cambiar código y una nota operativa.

1. **Gravedad: BLOQUEANTE**

   **Dónde:** [piloto.py:88](D:/Programacion/Disensor-Docs/experimento/herramientas/piloto.py:88), [corrida.py:74](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:74), [corrida.py:109](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:109), [piloto.py:742](D:/Programacion/Disensor-Docs/experimento/herramientas/piloto.py:742).

   **El caso legítimo que frena:** los checkpoints JSON no se escriben atómicamente: `escribir_json` llama directamente a `Path.write_bytes`, que primero trunca el archivo existente. Un Ctrl+C, apagado o error de disco durante cualquiera de las frecuentes escrituras puede dejar `resumen.json`, `plan.json` o `pares.json` vacío o truncado. Al reanudar, `leer_json` ejecuta inmediatamente `json.loads`; falla antes de que `cerrar_intentos_en_vuelo` pueda convertir el intento en `interrumpido`.

   La ventana más cara es la escritura posterior a una llamada: ya existen los artefactos crudos, pero el resumen anterior quedó destruido. El código no puede distinguir ni recuperar ese estado sin editar datos a mano; repetir la llamada daría una segunda oportunidad. Esto puede obligar a descartar una corrida legítima, pese a que §7.7 promete recuperación ante apagados.

   **El arreglo más chico:** escribir cada checkpoint en un temporal hermano, hacer `flush`/`fsync` y `os.replace` sobre el destino. Así un corte conserva o el JSON anterior completo —incluido el marcador en vuelo— o el nuevo completo. Aplicarlo al menos a `resumen.json`, `plan.json`, `pares.json`, `clave.json` e `informe.json`.

2. **Gravedad: DEBERÍA**

   **Dónde:** [corrida.py:552](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:552), [corrida.py:571](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:571), [corrida.py:580](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:580), [corrida.py:616](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:616).

   **El caso legítimo que frena:** `brazos`, `juez`, `validacion` y `analizar` hacen obligatoriamente un `git fetch origin main`. Una caída de red, DNS, GitHub, un token vencido o un remoto privado sin la credencial disponible frena incluso `validacion` o `analizar`, aunque el ancla se hubiera comprobado antes de la primera llamada y nada local haya cambiado. El error descarta además el `stderr` de Git y sólo informa “No se pudo traer”.

   Se puede reanudar sin cambiar código restaurando red/credenciales y repitiendo la etapa; por eso no lo clasifico bloqueante.

   **El arreglo más chico:** mantener el `fetch` obligatorio antes de crear el plan/primera llamada, pero no convertir una indisponibilidad posterior en inconsistencia experimental. Guardar en el plan la URL y el tip remoto comprobados; en etapas posteriores, usar esa prueba previa y tratar un `fetch` fallido como diagnóstico reanudable. Como mínimo, mostrar `stderr` y diferenciar “remoto inaccesible” de “commit ausente”.

3. **Gravedad: DEBERÍA**

   **Dónde:** [corrida.py:696](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:696), [corrida.py:767](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:767), [arnes.py:139](D:/Programacion/Disensor-Docs/experimento/herramientas/arnes.py:139), [arnes.py:161](D:/Programacion/Disensor-Docs/experimento/herramientas/arnes.py:161).

   **El caso legítimo que frena:** `verificar_binarios` siempre exige los dos binarios. Por eso `juez`, que sólo llama a Claude, no puede continuar si Codex fue actualizado, desinstalado o movido después de terminar los brazos. También compara la ruta absoluta de `codex.exe`, aunque el sha256 y la versión sean idénticos; en cambio no compara `claude_exe`. Una reanudación en otra cuenta o máquina con el mismo ejecutable queda bloqueada únicamente por la ruta.

   Se resuelve restaurando Codex 0.153.4 en exactamente la ruta anterior, sin tocar el árbol, pero es una dependencia innecesaria y especialmente cara entre `brazos` y `juez`.

   **El arreglo más chico:** verificar sólo Codex en las etapas GPT y sólo Claude en `juez`/gemelos. Para identidad, comparar versión y sha256; conservar la ruta real en cada intento como dato de auditoría, no como parte de la identidad del binario.

4. **Gravedad: DEBERÍA**

   **Dónde:** [corrida.py:529](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:529), [corrida.py:533](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:533), [corrida.py:582](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:582).

   **El caso legítimo que frena:** el verificador presupone una copia completa de la historia. En un clon superficial, `git log -- <ruta>` puede atribuir la incorporación de la lista al commit frontera o no encontrar su commit real; `merge-base --is-ancestor` también puede devolver falso simplemente porque falta el tramo histórico. El `fetch origin main` ordinario no garantiza convertir el clon en completo. Los bytes, el HEAD y los resultados pueden ser legítimos y aun así aparecer “lista rehecha” o “commit ausente”.

   También se ignoran los códigos de salida de varios comandos Git; errores operativos como `safe.directory`, repositorio inaccesible o Git faltante se transforman en aparentes inconsistencias.

   **El arreglo más chico:** detectar `git rev-parse --is-shallow-repository` y pedir explícitamente completar la historia antes de verificar; centralizar `git()` para revisar `returncode` y reportar `stderr`. Completar el clon o configurar `safe.directory` permite reanudar sin cambiar código.

5. **Gravedad: DEBERÍA**

   **Dónde:** [piloto.py:92](D:/Programacion/Disensor-Docs/experimento/herramientas/piloto.py:92), [corrida.py:418](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:418), [corrida.py:927](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:927).

   **El caso legítimo que frena:** todos los JSON se decodifican con `utf-8` estricto. Si un editor de Windows guarda `decisiones.json` o, más caro, `validacion/etiquetas.json` como UTF-8 con BOM, `json.loads` falla con `Unexpected UTF-8 BOM`. Con PowerShell 5 también es fácil producir UTF-16LE. El contenido semántico puede ser exactamente la planilla solicitada.

   Lo reproduje en memoria: los mismos bytes fallan con `decode("utf-8")` y se leen correctamente con `decode("utf-8-sig")`. Se resuelve volviendo a guardar el archivo como UTF-8 sin BOM.

   **El arreglo más chico:** aceptar `utf-8-sig` para los JSON editados a mano y detectar UTF-16 con un mensaje explícito de recodificación. No hace falta flexibilizar la estructura ni los booleanos.

6. **Gravedad: DEBERÍA**

   **Dónde:** [corrida.py:70](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:70), [corrida.py:556](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:556), [corrida.py:559](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:559).

   **El caso legítimo que frena:** el registro visible correcto deja de reconocerse si el blob del protocolo usa CRLF: el `\r` impide que coincida tanto `## Enmiendas` como el registro. También se rechaza `árbol` en normalización Unicode NFD (`a` + acento combinante), visualmente indistinguible.

   Lo reproduje con `registro_de_congelamiento`: LF/NFC pasa; CRLF falla diciendo que no existe la sección; NFD encuentra la sección pero cero registros. En cambio, sin punto final y con espacios finales sí pasa. Un espacio antes de `:` o dos espacios internos falla, pero eso sí es consistente con la exigencia explícita de “formato exacto”.

   Normalmente se detectaría antes del primer brazo. También puede aparecer más tarde si una enmienda sólo al protocolo convierte todo el archivo a CRLF; volver a LF permite reanudar sin alterar el árbol normativo.

   **El arreglo más chico:** normalizar `\r\n`/`\r` a `\n` y Unicode a NFC antes de parsear. Después aplicar el formato exacto.

7. **Gravedad: NOTA**

   **Dónde:** [corrida.py:790](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:790), [corrida.py:826](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:826), [corrida.py:840](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:840).

   **El caso legítimo que frena:** `juez --limite N` imprime siempre “listo para `validacion`”, aun cuando sólo procesó N ítems. Si se sigue esa instrucción, `validacion` termina con `FileNotFoundError` al armar pares, no con un diagnóstico de juez incompleto. No daña resultados: completar `juez` y repetir funciona.

   **El arreglo más chico:** imprimir “listo” sólo si los 400 veredictos son terminales; en `validacion`, comprobar primero faltantes/no terminales y emitir “terminar juez”.

### Trampas que todavía pasan

- [corrida.py:603](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:603): un resultado con `commit_de_la_lista` correcto pero sin `arboles`, o con `arboles: []`, pasa porque `any(...)` sobre una lista vacía es falso. La afirmación de que cada resultado necesariamente acredita su árbol no se cumple. El arreglo es exigir una lista no vacía antes de comprobar que todos sus valores son el árbol congelado.

- [corrida.py:582](D:/Programacion/Disensor-Docs/experimento/herramientas/corrida.py:582): el remoto sólo debe contener el commit anterior de la lista. El commit posterior que incorpora el registro de «Enmiendas» y su árbol puede no haber sido pusheado y `brazos` igualmente arranca, aunque §4.4 dice que se commitea y pushea el protocolo. El ancla externa no acredita qué código quedó congelado. Hay que comprobar también el commit que contiene el registro y guardar su identificador.

### Verificaciones que no frenan en falso

- Un brazo `fallo` o `interrumpido` sin `json_md5` y su juez `sin_llamada` son coherentes: ambos conservan `json_md5=None`, pasan la revisión y el análisis excluye el par.
- `juez_fallo`, `fallo_verificacion` e `interrumpido` son terminales y no se vuelven a llamar al reanudar.
- Repetir `juez` después de completarlo saltea los terminales; `sin_cupo` y `en_curso` conservan las lecturas y continúan.
- `validacion` antes de que Nico etiquete es el orden previsto: crea la plantilla con `null` y no la pisa al repetir.
- `analizar --sin-etiquetas` funciona después de `validacion` sin leer ni exigir las etiquetas; antes de `validacion` debe frenar porque todavía no existe `pares.json`.
- Exigir exactamente 100 pares no bloquea un análisis parcial legítimo: §4.4 prescribe que, si los 1.000 sorteos no alcanzan, se para y se informa; no define una corrida confirmatoria con N menor.
- `arbol_normativo` no depende de los bytes del checkout: usa el árbol de `HEAD`. En este repositorio dio el mismo md5 con `core.autocrlf` verdadero/falso y `core.quotePath` verdadero/falso; todos los nombres normativos actuales son ASCII.
- `.gitattributes` contiene `* -text`, por lo que otro checkout conserva además los finales de línea commiteados.
- `git gc` no debería modificar el resultado de `ls-tree`: cambia almacenamiento, no los OID ni el árbol. No lo ejecuté porque cambiaría estado.
- El punto final del registro es opcional en el regex, y los espacios/tabuladores finales se aceptan; no generan falso freno.
- `cerrar_intentos_en_vuelo` distingue `intento-1-*` de `intento-10-*`, y los resultados normales crean un artefacto con el prefijo esperado.
- La reextracción de `textos_libres` en `validacion` usa el mismo JSON, esquemas y código cuyo árbol se vuelve a comprobar; no encontré un estado normal de `sin_llamada` o JSON ilegible que intente abrir un `json.txt` inexistente.

No ejecuté las etapas, no abrí artefactos de humo ni sesiones, y no corrí `prueba_offline.py`; tomo como dato los 137/137 externos. Tampoco probé un remoto real ni reproduje un clon superficial porque ambas pruebas requerían cambiar estado. El worktree quedó limpio.

---

## La consigna

Sos la séptima revisión independiente de un protocolo experimental, una ronda enfocada antes de congelarlo. Las anteriores las hiciste vos, Codex (la sexta: `22-REVISION-CODEX-4.md`, 5 hallazgos sobre el diff de la v21); Claude Code las corrigió como v22.

**Esta ronda tiene una sola pregunta, al revés de las anteriores: ¿puede el código de verificación frenar una corrida legítima?** Hasta ahora se buscó que el arnés no dejara pasar una trampa. Desde la v22, el arnés frena (`sys.exit`) ante cualquier inconsistencia, y §10.1 dice que un cambio de código después de la primera llamada a los brazos descarta la corrida entera. Entonces un falso freno que aparezca recién en `juez`, `validacion` o `analizar` es caro: arreglarlo cambia el árbol y obliga a tirar la corrida. Buscá esos falsos frenos. Actuá como red-team sobre esa pregunta: casos borde, supuestos sobre git, Windows, rutas, codificaciones, el orden de las etapas, reanudaciones.

**Reglas de esta sesión:** sólo leés. No escribas, edites, muevas ni borres archivos, ni corras nada que cambie estado (nada de git que escriba, ni `git fetch`; `python -B` con `PYTHONDONTWRITEBYTECODE=1`, sin escribir archivos). Podés usar comandos de lectura y `python -` para importar los módulos de `herramientas/` y probar funciones puras en memoria. **No abras las respuestas de la prueba de humo** (`piloto/humo/*/intento-*-ultimo-mensaje.md`, `piloto/humo/*/intento-*-eventos.jsonl` ni `%USERPROFILE%\ch\sessions`). No corras `piloto.py` ni `corrida.py` con ninguna etapa. `prueba_offline.py` necesita un directorio temporal escribible que esta sesión no tiene: pasa 137 de 137 fuera de esta sesión.

**Lo que hay que mirar:** `herramientas/corrida.py` (sobre todo `congelamiento_en_git`, `registro_de_congelamiento`, `remoto_contiene`, `arbol_normativo`, `revisar_plan`, `verificar_corrida`, `plan_congelado`, `leer_incluidos`, `etapa_brazos`, `etapa_juez`, `etapa_validacion`, `etapa_analizar`, `gpt_con_reintentos`), `herramientas/piloto.py` (`claude_con_reintentos`, `cerrar_intentos_en_vuelo`, `juzgar`), `herramientas/juez.py` (`textos_libres`, `es_tecnico`) y §4.4, §7.7 y §10 de `01-PROTOCOLO.md`. El diff de la v22 es `git diff 5b779ce..HEAD`; el resto del arnés ya pasó por las rondas anteriores.

**Ejemplos de lo que buscamos** (no te limites a estos):
- `git fetch origin main` sin red, con credenciales vencidas o con un remoto de GitHub privado: ¿frena una etapa que debería poder seguir? ¿Hay una forma de reanudar sin cambiar código?
- El registro de «Enmiendas» escrito a mano: ¿un espacio, un final de línea CRLF, una tilde en «árbol» con otra normalización Unicode, un punto final, lo rechazan?
- `arbol_normativo` en otra máquina, con `core.autocrlf`, o después de un `git gc`: ¿cambia el md5 sin que cambie el código?
- Los resultados que se escriben entre etapas (`plan.json`, `resumen.json` de brazos y juez) y lo que `revisar_plan` exige de ellos: ¿hay un resultado legítimo que no pase (un brazo `fallo` sin `json_md5`, un veredicto `sin_llamada`, un ítem `interrumpido`)?
- `leer_incluidos` exige 100 pares: ¿hay un camino legítimo a menos (el sorteo agotado) que después no se pueda analizar?
- El orden y la reanudación: correr `juez` dos veces, `validacion` antes de que Nico etiquete, `analizar --sin-etiquetas`.

**Formato de la respuesta, en castellano:** una lista de falsos frenos, del más caro al menos caro. Cada uno con **Gravedad** (BLOQUEANTE si puede tirar una corrida legítima, DEBERÍA si frena pero se resuelve sin cambiar código, NOTA), **Dónde**, **El caso legítimo que frena**, con la evidencia, y **El arreglo más chico**. Si encontrás además una trampa que el arnés deja pasar, ponela aparte, al final. Después, una línea por cada cosa que verificaste y no frena en falso. Si algo no lo pudiste verificar, decilo.
