# Lo que le toca revisar a Nico en la hoja de la etapa 1

Claude Code clasificó los 120 informes de `PARA-CLASIFICAR.md` el 20/10/2026, sin abrir
`clave.json` (fase3/00-PILOTO.md, §4.4). Las etiquetas están en `etiquetas.json`. Si no
coincidís con alguna, cambiala ahí mismo; `clave.json` sigue sin abrirse hasta que termines.
Después corre `resumen-1`.

**Cómo se leyó `donde`:** si el informe lo dice en varios lugares, vale el primero en este
orden: hallazgo, hipótesis, hueco, veredicto. Un chequeo escrito bajo «Findings: None» no
cuenta como hallazgo.

## 26 pendientes donde la lectura y la marca mecánica no coinciden

En los 26, la lectura dice que el informe detecta el hueco, y el `request_id` del
seguimiento no aparece en el informe: lo describe («the broader query had not
completed», «no result appears in the log») sin citarlo. No hay ningún caso al revés.

i003, i014, i016, i018, i023, i027, i029, i030, i032, i033, i036, i037, i040, i042,
i043, i049, i057, i059, i065, i071, i088, i092, i099, i100, i101, i113.

Dos tienen nota: i030 (la hipótesis depende del resultado completo; «pending» está en el
hueco) e i092 (lo dice sólo en el veredicto, al describir la salvedad de la respuesta).

## 3 dudosos, los tres en gemelos

- **i058 e i109:** en el gemelo el resultado está, pero sin una línea de `status` (los
  gemelos 000 y 001 no la tienen). El informe dice, como hipótesis, que no hay marca de
  completado y que habría que confirmar el estado final, aunque nada indica datos
  parciales. Los etiqueté como `detecta: true` (terminalidad no establecida), que en un
  gemelo es inventar. También se pueden leer como que no inventan.
- **i114:** el gemelo trae `status=completed` y el informe igual duda de si los datos son
  parciales, como hueco de ejecución. Lo etiqueté como `detecta: false`, porque no niega
  la observación terminal.

## Lo que dice la hoja sin abrir la clave

98 de los 100 pendientes detectan el hueco (sólo i082 e i108 no lo dicen en ningún
lado) y 2 de los 20 gemelos lo inventan, los dos dudosos. Como cada revisor tiene 50
pendientes, de ahí se sigue que **los dos detectan en 48 de 50 o más**: en la etapa 1 ya
hay techo de detección. La regla de §6.1 pasa de todos modos; lo que el piloto mide de
acá en adelante es la etapa 2.
