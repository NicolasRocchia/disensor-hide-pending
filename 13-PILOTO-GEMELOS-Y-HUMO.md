# Piloto: fragmentos, gemelos y prueba de humo

**13/10/2026, de 16:00 a 16:25 ART.** Con el OK de Nico, Claude Code escribió las
tres piezas que faltaban (`fragmentos.py`, `gemelos.py` y `extraccion.py`, más
las etapas `gemelos` y `humo` de `piloto.py`), las probó sin llamadas
(`prueba_offline.py`) y corrió las dos etapas. Commits del código: `b120562`,
`686b177` y el de los arreglos de este informe; salidas: `7b0dcbb` (humo) y el de
los gemelos.

## Fragmentos de esquema (§5.2)

- **Residuo:** 8.542 caracteres, md5 `f554b756a9cf5ac6663e3e00a2ecccce`.
  **Placebo:** 927, md5 `78af6ea9c45fcee9577d4f09227fecc2`. Fuente:
  `de14e5c:src/disensor/residue.schema.json`, md5
  `182f3f3f17416ff645badf1f55c76bda`.
- **Coinciden con la reconstrucción independiente** de la segunda revisión (`03`,
  punto 10: 8.542 y 927), y el vocabulario de §5.4 sale igual.

## Prueba de humo (§7.6, puntos 6 a 8)

Cinco logs pendientes (`000`, `001`, `002`, `007`, `009`, uno por comportamiento
sorteado), por A2b y por A2, en orden sorteado. **Nadie leyó las respuestas:** la
etapa sólo registra indicadores mecánicos.

1. **El sujeto no ejecutó nada:** 10 de 10 hechas, cero comandos, cero archivos,
   cero rechazos en el stderr. Ni siquiera intentó usar herramientas.
2. **La extracción de §6.1 encuentra el JSON en las 10.** Los 5 de A2 traen
   `residue`; ninguno de A2b, como pide cada esquema. 8 de 10 vienen en un cerco
   de código.
3. **Bytes por stdin (punto 8): iguales.** La primera llamada corrió sin
   `--ephemeral`, y el mensaje que Codex guardó en
   `%USERPROFILE%\ch\sessions\…\rollout-2026-10-13T16-01-05-….jsonl` es idéntico
   al enviado. Esa sesión trae una respuesta a un brazo: queda ahí, sin leer.
4. **Costo:** A2b, 13.322 tokens de entrada y 223 de salida de promedio; A2,
   19.804 y 454. Una llamada de A2 tuvo dos mensajes del agente (39.448 de
   entrada).

## Gemelos (§4.4, §8.2)

Diez logs, dos por comportamiento sorteado (`000`, `001`, `002`, `003`, `004`,
`007`, `008`, `009`, `010`, `018`), con Opus por `claude -p`.

1. **Las 10 llamadas, verificadas:** sin herramientas (`tools: []`), un turno,
   `claude-opus-5-5`. Cada una: unos 17 segundos, unos 2.100 tokens de entrada
   (escritos a caché), unos 2.000 de salida (unos 900 de razonamiento) y unos
   USD 0,06 a precio de API.
2. **Los automáticos de §4.4 pasan en los 10:** primer resultado, consulta de
   seguimiento y pregunta final intactos; el evento es ahora un `TOOL RESULT`; la
   entidad que tenía más de la categoría dominante sigue teniendo más (chequeo 4,
   por estructura en los 10); entre 10 y 24 líneas con número en el bloque nuevo.
3. **Dos errores del chequeo, no de los gemelos, corregidos antes de este
   informe** (con su prueba):
   - En `000` el bloque nuevo agrupa por clase de infraestructura y cierra con un
     total suelto; el respaldo del chequeo 4 tomaba ese total como la hoja mayor.
     Ahora compiten sólo las hojas del nivel más profundo.
   - En `009` y `010` el bloque nuevo parte cada entidad en un subnivel
     (`primary`/`secondary`); el chequeo 4 bajaba hasta ese subnivel. Ahora compara
     «al mismo nivel» que el primer resultado, que es lo que pide §4.4.4.
   - En `018` Claude repitió el rótulo `EXPERIMENT_LOG:` arriba del log, y eso
     corría la numeración de las entradas: el bloque nuevo salía como «cambiado
     fuera del evento» (27 líneas). Ahora la numeración es la misma que la de
     `chequeo.entradas`, y queda la única línea agregada de verdad.
4. **Lo que va para Nico** (`piloto/gemelos/PARA-NICO.md`):
   - **Chequeo 2:** sólo `018`, la línea `EXPERIMENT_LOG:` agregada arriba.
   - **Chequeo 3:** en los 10, la coincidencia «async» de la llamada de
     seguimiento (que el chequeo 1 obliga a dejar intacta; va marcada). Además, en
     9 de 10, la línea `request_id=…` que Claude conserva en el bloque nuevo, junto
     con un `status=completed`; y en `001`, «start» dentro de `window_start`, un
     parámetro de una llamada de distracción que ya estaba en el pendiente.

## Decisiones que quedan para Nico antes de congelar

1. **El rótulo repetido (`018`).** Un gemelo con `EXPERIMENT_LOG:` arriba no pasa
   el chequeo 2, y el par se pierde. Pasó en 1 de 10: con unos 110 gemelos serían
   unos 11 pares perdidos por un artefacto de formato. Opción: que el arnés saque
   una primera línea que sea exactamente `EXPERIMENT_LOG:`, como regla mecánica
   declarada.
2. **`request_id` y `status=completed` en el bloque nuevo.** Aparecen en 9 de 10.
   El gemelo muestra que la consulta asíncrona terminó y devolvió sus datos; no
   dice que siga pendiente. Si Nico lo acepta como regla, el arnés puede
   marcarlas «en el bloque nuevo» para aprobarlas de una vez, en lugar de una por
   una.
3. **La revisión de los 10 gemelos del piloto**, en `PARA-NICO.md`, que es para lo
   que está el piloto: probar el circuito antes de hacerlo con 110.

**Decididas por Nico el mismo día** (protocolo v13): se saca el rótulo, y la línea
`request_id=…` del bloque nuevo queda aceptada por regla. Con eso, a Nico le quedan
en el piloto la coincidencia «async» de la llamada de seguimiento (9 de 10, que el
chequeo 1 obliga a dejar intacta) y el falso positivo «start» de `001`.

## Lo que falta antes de congelar

- **El juez (§6.2) y el validador (§5.3)** no están escritos, y el piloto no los
  ejercita: el juez corre sobre las respuestas a los brazos, que nadie puede ver
  antes de congelar. Se pueden escribir y probar con JSON armados a mano.
- **El análisis (§2.1, §6.3):** el script de la permutación por cambio de signo,
  escrito y probado antes de que exista un dato, también es parte de lo que se
  congela.
- **La tercera revisión independiente** (§0, paso 3).
