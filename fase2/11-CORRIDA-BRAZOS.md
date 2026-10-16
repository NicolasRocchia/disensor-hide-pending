# La corrida de la fase 2: `brazos`

**16/10/2026, 09:32 a 11:44 ART** (12:32 a 14:44 UTC), con el protocolo congelado
(`09cc6c3`, registro `fffd244`, tag `protocolo-fase2-congelado`) y el OK de Nico.
Claude Code no abrió ninguna prosa, ningún JSON ni ninguna validación de los brazos:
este informe sale sólo de los datos del arnés (estados, intentos, tokens, comandos).

## Lo que pasó

- **El plan** se escribió antes de la primera llamada, con el ancla verificada:
  commit del registro `09cc6c3`, HEAD `fffd244`, árbol
  `532d092cb5dea971c8738246bc824ee2`, el remoto de GitHub y el tag publicado ahí.
  800 llamadas, las ocho de cada log seguidas, en el orden sorteado con la semilla
  20261015.
- **Una caída del servicio a las 88 llamadas.** El ítem `013-A2-limpio` no terminó:
  *«Selected model is at capacity. Please try a different model.»* El canario de los
  brazos dio lo mismo 18 segundos después, así que el arnés lo tomó como caída
  (§11): el intento quedó marcado `caida`, no gastó reintentos, y la etapa paró. Una
  sonda aparte, fuera de la corrida, encontró la capacidad de vuelta un minuto y
  medio después, y la etapa se reanudó desde ese ítem.
- **Un corte intermitente más:** `018-A2-limpio` falló con el mismo mensaje, pero el
  canario terminó dos segundos después, así que contó como falla del ítem (uno de
  sus tres intentos), como pide §11; el reintento terminó.
- **800 de 800 terminados:** 798 en el primer intento, 2 en el segundo (los de
  arriba). Ningún comando ejecutado, ningún archivo cambiado, ningún rechazo,
  ninguna red de seguridad, ninguna `PARADA`.
- **Un log partido:** el 013, cuyas ocho llamadas quedaron repartidas entre las dos
  sesiones por la caída. Va a la sensibilidad sin pares partidos (§6.1, como en la
  fase 1).
- **Uso:** 10.910.858 tokens de entrada (8.542.848 de caché) y 185.364 de salida, en
  todos los intentos, más dos canarios. Del orden de 4,5 puntos de la semana de GPT
  de Nico con la calibración de la fase 1.

## Lo que sigue

`jueces` (1.200 ítems con Claude, unos USD 27 a precio de API), después de que se
renueve la semana de Max de Nico, el 17/10 a las 9:00 ART, como se acordó; después
`validacion`, que arma las dos planillas de Nico, y `analizar` con sus etiquetas.
