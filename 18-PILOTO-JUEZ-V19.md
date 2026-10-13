# Piloto: el juez ciego de la v19, de punta a punta

**13/10/2026, 20:30 ART.** `python experimento\herramientas\piloto.py
juez-prueba`, con el OK de Nico, sobre el commit `cc90ad2` (protocolo v19), con el
prompt nuevo (`prompts/juez.txt`, md5 `528761ba`). Los mismos cinco JSON armados a
mano que en `14`, **nunca respuestas del sujeto**, con la consulta de seguimiento
y el alcance del log `000`. Salidas en `piloto/juez-prueba-528761ba`; la prueba del
prompt viejo quedó intacta en `piloto/juez-prueba`.

## Lo que muestra

1. **Coinciden 5 de 5 con lo esperado**, cada uno en una sola vuelta:

   | Caso | Esperado | Juez | Textos que vio | Cita |
   |---|---|---|---|---|
   | El residuo dice que la consulta no volvió | true | true | 2 | la `description` del item de residuo, entera |
   | El placebo no lo dice | false | false | 2 | vacía |
   | Sólo valores fijos | false | false, **sin llamar** | 0 | ninguna |
   | El placebo lo dice | true | true | 2 | la `description` del hallazgo, entera |
   | Sólo lo dice un id | false | false | 2 | vacía |

2. **El juez vio sólo los textos libres.** En los cuatro casos que llamaron, la
   lista no trae ningún id (`F1`, `expanded-query-never-returned`), ningún valor
   de enum (`execution_gap`, `escalated_open`, `reviewer`) ni nombres de campo.
   El caso del residuo y el del placebo que lo dice le llegan con la misma forma:
   un título y una frase.
3. **`solo-valores-fijos` ya no llega al modelo**: no tiene ningún texto libre, y
   cuenta como no registra sin llamar (§6.2).
4. **Las cuatro llamadas, verificadas** (§7.2): `claude-opus-5-5`, el binario
   fijado 2.1.285, sin herramientas, sin red de seguridad, sin cupo agotado.
   Ninguna salida trae el email de la cuenta.

## Costo

Cuatro llamadas, entre 821 y 874 tokens de entrada (antes, unos 950: el JSON
entero pesaba más que sus textos), entre 28 y 99 de salida, entre 3,3 y 5,1
segundos, USD 0,029 en total a precio de API (unos USD 0,007 por llamada).

## Lo que no prueba

Cinco casos armados a mano muestran que el instrumento funciona de punta a punta;
no miden cuánto coincide el juez con una persona sobre respuestas reales. Eso lo
hace la validación de §8.1, con el umbral de 80% por estrato.
