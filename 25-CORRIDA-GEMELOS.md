# Corrida: `gemelos` (§4.4 y §8.2)

**14/10/2026, 00:30 a 01:08 ART.** `python experimento\herramientas\corrida.py
gemelos`, con el OK de Nico, sobre los 110 logs que pasaron `logs` (`24`). Un
gemelo limpio por log, armado por Claude Opus con el prompt congelado
(`prompts/gemelo.txt`).

## Lo que dio

- **109 gemelos hechos y 1 que falló la verificación** (`096`).
- **De los 109, 106 pasan los chequeos automáticos de §4.4**; 3 no (`027`, `034`
  y `097`) y quedan descartados sin pasar por Nico.
- **La hoja de Nico** (`corrida/gemelos/PARA-NICO.md`, con
  `corrida/gemelos/decisiones.json`): 106 logs y 181 ítems, que son las 106
  casillas C y 75 más:
  - 63 señales de pendiente que la expresión de §4.4 encuentra en líneas ajenas a la
    consulta (`start=` en los parámetros de otra llamada, «queue-lag warnings»,
    «acknowledged», «incomplete: 0»);
  - 6 líneas cambiadas fuera del evento: el armador reescribió frases del asistente
    que anunciaban la espera («while that rollup is processed») como neutras
    («I'll also check system health.»);
  - 6 casillas 4 (la respuesta vieja sigue valiendo).

  En el piloto, 10 gemelos dejaron una sola línea además de C; los logs de la
  corrida, más largos y variados, dejan más.
- **Costo:** USD 7,47 a precio de API, en 38 minutos.

## Los descartes

- **`027`, `034` y `097`, chequeo 4:** el armador decoró el nombre de la entidad
  en el bloque nuevo («Fab Line F3» pasó a «Wafer Fabs / Fab Line F3»;
  «reticle-cloud-gateway» a «reticle-cloud-gateway (external)»; «edge-sw-17» a
  «edge-sw-17 (standard-compute-pools)»), y el chequeo por estructura no reconoce la
  entidad. Son falsos negativos de una regla automática y pre-registrada: quedan
  descartados, sin tocar el chequeo.
- **`096`, un clasificador de seguridad:** en los dos intentos, un clasificador
  cortó la respuesta («stopped by a safety classifier») y la CLI siguió en un
  segundo turno: en el primero escribió un gemelo después de un
  `model_refusal_fallback`, que pudo venir de otro modelo; en el segundo, se negó.
  La verificación de §7.2 los rechazó por tener dos turnos, que es lo que tenía
  que pasar, y el log queda descartado por §4.4. **Lo mismo puede pasarle al
  juez**: la misma verificación lo frena, y el ítem termina en «juez falló» (§6.2).

## Lo que sigue

1. **Nico llena la hoja**: «aprobada» o «rechazada» en cada línea, «si» o «no» en
   4 y en C, en `decisiones.json`. Para C, abre el gemelo y mira que el bloque nuevo
   cubra todo el alcance ampliado.
2. **`incluir`**, sin modelos: los primeros 100 pares que pasan todo. Hay 106
   candidatos; si Nico descarta más de 6, faltan pares, y se vuelve a `logs` con un
   objetivo mayor y a `gemelos` sólo para los nuevos.
3. El commit de la lista, el registro en «Enmiendas» y el push a `origin/main`
   antes de `brazos` (§4.4).
