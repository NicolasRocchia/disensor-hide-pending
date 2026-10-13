# Lo que se hizo con la cuarta revisión: protocolo v20

**13/10/2026.** Con la decisión de Nico sobre el juez (lista de campos, no una
llamada por texto) y su pedido de arreglar todo como v20 y correr otra ronda de
Codex antes de congelar. Ninguna llamada a modelos. `prueba_offline.py`: 131 de
131. La tabla que cruza cada hallazgo con lo que se hizo está en §15 del
protocolo, «De la v19 a la v20»; acá va lo que no entra en una tabla.

## Lo que no se aceptó, y por qué

- **El hallazgo 7, seguir la anidación sobre texto que no parsea.** Hoy, un
  arreglo sin cerrar con un objeto completo adentro deja pasar ese objeto. El
  arreglo propuesto lo evitaría, pero haría que un corchete suelto de la prosa
  («Regions [standard, regional») escondiera un JSON válido que viene después:
  reproducido, hoy ese caso sale legible. Lo segundo es más probable que lo
  primero. Queda declarado en §6.1.
- **Que `origin` sea texto libre** (parte del hallazgo 2). El esquema la define
  como «reviewer_id of the reviewer that produced it»: un identificador. Sigue
  afuera.
- **Que la guarda acepte una cita trivial** (parte del hallazgo 2). La guarda es
  mecánica por diseño desde la v14: prueba que la cita existe en lo que vio el
  juez, no que diga algo. Lo semántico lo controla la validación de §8.1.
- **«Es un poco conservadora»** en §6.4 (parte del hallazgo 9). Habla del tamaño
  de la prueba, que rechaza entre 3% y 4% con α = 0,05 por lo discreto de los
  datos, no del supuesto de independencia que se sacó en la v19. Se queda, con
  una aclaración.

## El juez, con la lista de campos

La regla nueva saca las claves de los esquemas que no son prosa (identificadores,
referencias, `link`, `hash`, `date` y los campos de enum) y deja pasar los ocho
campos de prosa y cualquier clave que no esté en ningún esquema, para no perder
un registro escrito en un campo inventado. Una prueba recorre los dos esquemas y
exige que toda clave esté decidida.

Lo que sigue delatando al brazo, el contenido y la cantidad de textos, queda
declarado como limitación 11. La alternativa de Codex, juzgar cada texto por
separado, lo habría ocultado a costa de unas 3.000 llamadas y de perder el
contexto entre título y descripción.

**Los cinco casos de `juez-prueba` reciben los mismos textos con la regla nueva.**
La etapa ahora reutiliza un resumen sólo si los textos coinciden. Se volvió a
correr y reutilizó los cinco sin llamar: la prueba de `18` vale para la v20.

## La grilla de §6.4, rehecha

Con `rho_brazos` corregido (una sola bandera por condición, común a los dos
brazos), la grilla cambia en los números pero no en la conclusión:

- La correlación entre brazos sube la potencia, y más que antes: en la primera
  fila, de 83% sin correlación a 96% y 97% con ρ = 0,6.
- La correlación entre condiciones casi no la mueve.
- Ninguna celda queda debajo de la tabla fuera del ruido: la más baja, 1,4 puntos.
- Con los brazos iguales, el rechazo queda entre 3,9% y 4,7%.

La tabla de §6.4 se reproduce igual que antes: el camino independiente no cambió.

## Un error que no vio ninguna revisión

Un gemelo cortado por cupo queda guardado sin estado, y `incluir` lo descartaba
como «gemelo None» en vez de pedir que se termine: se perdía un par sin razón.
Ahora `incluir` frena y lo pide; descartan sólo los estados terminales. Con su
prueba.

## Lo que sigue

1. La quinta ronda de Codex, sobre el diff de la v20, que Nico ya pidió.
2. Lo que se haga con ella, y congelar (§0, paso 4).
