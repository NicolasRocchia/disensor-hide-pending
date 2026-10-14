# Resultado de la fase 1: C2

**14/10/2026, 12:20 ART.** `python experimento\herramientas\corrida.py analizar`,
con el OK de Nico, después de que Nico etiquetara la planilla ciega (`abae52d`).
Protocolo congelado en la v23 (tag `protocolo-congelado`), lista congelada en
`238c1df`. Todo el análisis es el de `herramientas/analisis.py`, escrito y probado
antes de que existiera un dato; la salida entera está en `corrida/informe.json`.

## La frase de §9

> Con gpt-5.6-sol corriendo por Codex, el esquema de residuo, tal como sale, hizo
> que el registro consignara el hueco, sin consignarlo cuando no había hueco, más
> seguido que un listado de hallazgos sin residuo: `s_json` aumentó en 0,24
> [0,16, 0,33].

## C2, la prueba confirmatoria (§2.1)

- **N = 100 pares**, ninguno excluido: las 400 llamadas terminaron, el juez dio
  veredicto en los 400 JSON, y no hubo pares partidos.
- **24 pares con diferencia +1 y ninguno con diferencia en contra.** Permutación
  exacta por cambio de signo, bilateral: p = 1,2 × 10⁻⁷.
- **Efecto medio: 0,24**, intervalo bootstrap de percentiles al 95% [0,16, 0,33]
  (10.000 remuestreos, semilla 20261013).

## La validación de Nico (§8.1)

- **Coincidencia con el juez en la muestra estratificada:** 15 de 15 en los `true`
  del juez y 14 de 15 en los `false`, los dos estratos suficientes y por encima del
  umbral de 80%. El juez es confiable.
- **Precisión de los positivos del juez en los ítems decisivos:** 23 de 24 (0,96
  [0,80, 0,99]).
- **La prueba recalculada con las etiquetas de Nico** da lo mismo en las dos
  versiones (todo lo etiquetado y sólo los decisivos): suma 24, p = 2,4 × 10⁻⁷, el
  mismo signo. C2 no es «sensible al juez».

## De qué está hecho el efecto (§2.2, descriptivas)

| | A2b (placebo) | A2 (residuo) |
|---|---|---|
| Consigna el hueco en el pendiente | 5 de 100 (0,05 [0,02, 0,11]) | 29 de 100 (0,29 [0,21, 0,39]) |
| Lo consigna en el gemelo limpio (falso positivo) | 0 de 100 ([0, 0,04]) | 0 de 100 ([0, 0,04]) |
| Falso positivo, gemelos con `request_id` (67) | 0 de 67 | 0 de 67 |
| Falso positivo, gemelos sin `request_id` (33) | 0 de 33 | 0 de 33 |
| JSON ilegible | 0 de 200 | 0 de 200 |
| Cumple el esquema | 200 de 200 | 200 de 200 |
| Cumple las reglas de disensor | no aplica | 96 de 100 pendientes, 93 de 100 limpios |

- **Todo el efecto viene de consignar el hueco**, no de evitar falsos positivos:
  ningún brazo registró un hueco en un gemelo limpio, tampoco cuando el gemelo
  conservaba el `request_id` (limitación 9 de §12).
- **El residuo no alcanza para que el registro sea fiel.** En 71 de los 100 logs
  pendientes, el JSON de A2 declaró expresamente que no quedaba residuo
  (`declared_absence`) con la consulta todavía sin volver: el **falso cierre** es
  0,71 [0,61, 0,79]. En los limpios, el cierre correcto es 99 de 100. El esquema
  sube la tasa de registro de 5% a 29%, pero en la mayoría de los casos el modelo
  usa la casilla de ausencia para cerrar un hueco que existe.
- Ningún brazo ejecutó comandos ni escribió más de un mensaje.

## Lo que este resultado dice y lo que no

- Dice que, con este sujeto, este arnés y este escenario, pedir el JSON con el
  esquema de residuo hace que el JSON consigne más seguido que la consulta no
  volvió, sin consignarlo cuando sí volvió, que pedir un listado de hallazgos.
- No dice que la respuesta en prosa cambie: eso es la fase 2 (§13).
- No dice que el residuo vuelva fiel al registro: el falso cierre de 71% es el
  dato que más pesa para disensor, y va al frente del informe junto con C2.
- Vale para la población que dejó el protocolo: logs cuyo primer resultado da un
  número por categoría (`24`), gemelos que pasaron los chequeos y la casilla C, y
  respuesta y JSON en una sola generación (§1, §12).

## Gasto de la corrida

GPT: unos 12,9 millones de tokens de entrada (`logs` 7,2 M, `brazos` 5,7 M).
Claude: USD 10,72 a precio de API (`gemelos` 7,47, `juez` 3,25).
