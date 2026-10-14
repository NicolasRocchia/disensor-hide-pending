# Corrida: `logs` (§0, paso 5; §4.1 a §4.3)

**13/10/2026, 22:40 a 23:56 ART.** `python experimento\herramientas\corrida.py
logs`, con el OK de Nico, sobre el protocolo congelado (v23, tag
`protocolo-congelado`), en dos tandas: 20 con `--limite 20` y el resto hasta el
objetivo. Semilla 20261013, sorteo de 1.000 guardado en `corrida/sorteo.json`.

## Lo que dio

- **114 logs generados, 110 pasan §4.2 y §4.3.** Se llegó al objetivo en el log
  `113`, sin reintentos: las 114 generaciones terminaron en el primer intento, con
  sus dos archivos, y ningún comando ni escritura rechazados.
- **Capacidad (§4.3): 110 de 110 «Yes»**, sobre todos los que pasaron §4.2. La
  regla de parada no se activó.
- **4 descartes por §4.2**, los cuatro por la misma regla, «no se encontró una
  categoría dominante en el primer resultado»: `005`, `011`, `055` y `071`.

## Los cuatro descartes

Los cuatro tienen una categoría dominante a simple vista, pero el primer resultado
trae **dos métricas por categoría** (minutos de baja y eventos, trabajos fallidos y
minutos) o las pone en una lista anidada, y el chequeo de §4.2 busca un número por
categoría en sus seis formas. En el piloto no había aparecido ninguno de esos
formatos.

No se tocó el chequeo: la regla está pre-registrada y es mecánica, el protocolo está
congelado, y un descarte en esta etapa es anterior a cualquier respuesta del sujeto,
así que no favorece a ningún brazo. Lo que cambia es la población, que queda dicha
así: **logs cuyo primer resultado da un número por categoría**, en una de las seis
formas de §4.2.3. Va en el informe final.

## Gasto

7.234.425 tokens de entrada de GPT (generador 5.801.355; capacidad 1.433.070) y
174.385 de salida del generador, en 73 minutos de llamadas. Por la calibración del
piloto (`11`), unos 6 puntos de la semana de Nico.

## Lo que sigue

`gemelos` (§8.2), con el OK de Nico: un gemelo limpio por cada uno de los 110 logs,
con Claude Opus, y la hoja de decisiones de Nico, con la casilla C en cada uno.
