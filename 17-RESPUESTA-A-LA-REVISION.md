# Lo que se hizo con la tercera revisión: protocolo v19

**13/10/2026, 20:25 ART.** Con el OK de Nico («arreglá todo y aplicá 1 a 5»),
Claude Code corrigió los once hallazgos de `16` que eran errores y aplicó las cinco
decisiones de Nico sobre los otros. Ninguna llamada a modelos. `prueba_offline.py`:
114 de 114. La tabla que cruza cada hallazgo con lo que se hizo y dónde está en
§15 del protocolo, «De la v18 a la v19»; acá va lo que no entra en una tabla.

## Las cinco decisiones de Nico

1. **Juez ciego** (hallazgo 1). El juez ya no recibe el JSON: recibe sus textos
   libres (cada valor de texto que no es un valor fijo de ninguno de los dos
   esquemas, sin las claves de identificación), sin repetidos, ordenados
   alfabéticamente y con etiquetas opacas (`t1`, `t2`…). La planilla de Nico
   muestra lo mismo. Las etiquetas de Nico se aplican a todo lo que etiquetó, y si
   en algún estrato con al menos 10 etiquetas coincide con el juez menos de 80%,
   C2 no se afirma. Prompt nuevo: `prompts/juez.txt`, 767 caracteres, md5
   `528761ba0ee3c66ffc55ff36dd058de9`.
2. **Casilla C por gemelo** (hallazgo 5): completitud del bloque nuevo, decidida
   siempre a mano. Un «no» saca el par.
3. **Pistas de asincronía, declaradas** (hallazgo 6): limitación 9 de §12, y los
   falsos positivos se informan por separado según el gemelo conserve o no el
   `request_id`.
4. **«Misma generación»** (hallazgo 14): §1 y la limitación 10 de §12 dicen que
   respuesta y JSON salen de un solo pedido, con el esquema a la vista desde el
   principio; el resultado no habla de un reporte pedido después.
5. **La estadística, dicha como es** (hallazgo 8): la prueba es exacta bajo la
   nula de intercambiabilidad de los brazos dentro de cada log; «conservador» se
   sacó y en su lugar va una grilla de correlaciones.

## Lo que hay que saber del juez ciego

- **El brazo ya no se ve en la forma, pero todavía se puede adivinar por el
  contenido**: un texto de A2 que habla de lo que quedó abierto se parece a un
  residuo. Por eso la guarda sigue siendo mecánica y las etiquetas de Nico sólo
  pueden quitar. Va dicho en §8.1.
- **Un JSON sin ningún texto libre cuenta como no registra, sin llamar al juez.**
  El caso `solo-valores-fijos` de `juez-prueba` es justo eso: ahora no llega al
  modelo.
- **La prueba del juez del piloto (`14`) se hizo con el prompt viejo.** Hay que
  repetirla antes de congelar: cuatro llamadas a Claude, con el OK de Nico.
- **Al cerrar esto apareció un error que la revisión no vio:** `juez-prueba`
  reutilizaba cualquier resumen ya terminado, y los del prompt viejo están
  commiteados. Repetirla habría reimpreso el 5 de 5 viejo sin llamar al juez
  nuevo. Ahora cada prompt escribe en su carpeta (`piloto/juez-prueba-528761ba`),
  el resumen guarda el md5 del prompt y un resumen de otro prompt frena la etapa;
  con su prueba.

## La grilla de §6.4

`analisis.py potencia` imprime, además de la tabla, la potencia con dos
correlaciones positivas: entre brazos (con probabilidad ρ, A2 y A2b comparten el
sorteo de una condición) y entre condiciones (con probabilidad ρ, el pendiente y
el limpio de un brazo comparten el suyo), con ρ en 0, 0,3 y 0,6 y 1.000 réplicas
por celda.

- La correlación entre brazos **sube** la potencia: en la primera fila, de 83% a
  92% y 93% con ρ = 0,6.
- La correlación entre condiciones casi no la mueve.
- **Ninguna celda queda debajo de la tabla fuera del ruido** de 1.000 réplicas
  (unos 2,5 puntos): la más baja queda 1,2 puntos debajo. Una primera redacción
  decía «igual o mayor en todas», y no era cierto al pie de la letra; quedó
  corregida antes del commit.
- Con los brazos iguales, el rechazo queda entre 3,2% y 4,5%.

Correlaciones negativas o una heterogeneidad distinta entre logs podrían bajarla:
la tabla sigue siendo una guía.

## Lo que cambió en el código

- `extraccion.py`: un arreglo que parsea se saltea entero (12).
- `juez.py`: textos libres, lista con etiquetas, guarda sobre los textos y lectura
  que exige `evidence_quote` (1 y 12).
- `piloto.py`: `juzgar` sobre los textos, reintentos contados sobre toda la
  historia de cada etiqueta, retoma desde la vuelta siguiente (4); cada intento
  guarda comando, modelo, esfuerzo y binario (16).
- `analisis.py`: etiquetas validadas (booleanos, ids exactos, sin repetidos), C2
  con las etiquetas de Nico sobre todo lo etiquetado y con el signo, umbral de
  80% por estrato, N=0 «no evaluable», sensibilidad sin pares partidos, falsos
  positivos por `request_id`, la grilla (1, 2, 8, 11, 13, 15).
- `corrida.py`: la regla de capacidad sólo al terminar y con las fallas en el
  denominador (3); casilla C y valores exactos (5 y 13); el congelamiento de la
  lista por commit, que `brazos` exige (10); tope de 1.000 en el sorteo (15);
  `--limite` en pares y sesiones registradas (11); estados terminales del juez y
  md5 de todo lo que recibe (4 y 9); la planilla con los textos libres (1).

## Lo que sigue

1. Con el OK de Nico, **`juez-prueba` otra vez** con el prompt nuevo (cuatro
   llamadas a Claude).
2. Si Nico la pide, **una ronda de Codex sobre el diff de la v19**: el cambio
   toca el instrumento de medida (el juez), así que cruza la barra de impacto alto.
3. Congelar (§0, paso 4) y empezar la corrida por `logs`.
