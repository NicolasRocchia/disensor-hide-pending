# Piloto: el juez de §6.2, de punta a punta, con JSON armados a mano

**13/10/2026, 16:50 ART.** `python experimento\herramientas\piloto.py
juez-prueba`, con el OK de Nico, sobre el commit `432754b` (protocolo v14). Cinco
JSON armados a mano, **nunca respuestas del sujeto**, con la consulta de
seguimiento y el alcance del log `000` del piloto. Cinco llamadas a Claude.

## Lo que muestra

1. **Coinciden 5 de 5 con lo esperado**, cada uno en una sola vuelta:

   | Caso | Esperado | Juez | Cita |
   |---|---|---|---|
   | El residuo dice que la consulta no volvió | true | true | la `description` del item de residuo, entera |
   | El placebo no lo dice | false | false | vacía |
   | Sólo valores fijos (`execution_gap`, `escalated_open`) | false | false | vacía |
   | El placebo lo dice | true | true | «The broader query was accepted but has not returned results yet.» |
   | Sólo lo dice un `id` | false | false | vacía |

   Las dos citas salen de campos `description`, texto libre, y pasan la guarda.
   En el último caso el juez mismo no tomó el `id` como declaración, así que la
   guarda no tuvo que frenarlo; esa rama está probada con una llamada simulada en
   `prueba_offline.py`.
2. **Las cinco llamadas, verificadas** (sin herramientas, un turno, Opus).
3. **Costo por llamada del juez:** unos 950 tokens de entrada (escritos a
   caché), entre 25 y 140 de salida, unos 4 segundos y unos USD 0,009 a precio de
   API. Para las 400 llamadas de la corrida, unos USD 4; con los 110 gemelos, el
   lado de Claude del experimento queda en unos USD 10 a precio de API, muy poco
   para el plan Max de Nico.

## Lo que no prueba

Cinco casos armados por quien escribe el arnés no validan al juez: la validación
es la de §8.1, con las etiquetas de Nico sobre las respuestas reales. Esto prueba
que el circuito funciona (mensaje, llamada, lectura, guarda) y lo que cuesta.
