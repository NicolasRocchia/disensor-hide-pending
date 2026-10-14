# Corrida: `brazos` (§7.7)

**14/10/2026, 09:26 a 10:50 ART.** `python experimento\herramientas\corrida.py
brazos`, con el OK de Nico, sobre la lista congelada (`238c1df`, registro en
«Enmiendas» en `7d02634`), después del push de `main` y del tag
`protocolo-congelado` al repo público
`github.com/NicolasRocchia/disensor-hide-pending`.

**Este informe sólo dice cómo anduvo el arnés.** Claude Code no abrió ninguna
respuesta ni ningún JSON de los brazos (§0): lo de abajo sale de los registros de
cada intento.

## El congelamiento, antes de la primera llamada

El plan de los brazos quedó guardado con el commit de la lista (`238c1df`), el
árbol (`10c81bb6341d62e909a4256d8299cdb4`, el mismo del tag) y el HEAD anclado
(`7d02634`), que el arnés verificó en `origin/main` con un `fetch` antes de llamar
(§4.4).

## Lo que dio

- **400 llamadas, las 400 terminadas en el primer intento.** Ningún reintento,
  ningún corte por cupo, ninguna parada.
- **Red de seguridad (§7.1):** ningún comando ejecutado, ningún archivo cambiado,
  ningún rechazo del sandbox en el stderr.
- **Una sola sesión:** no hay pares partidos (§7.7).
- **Gasto:** 5.678.856 tokens de entrada de GPT (4.047.232 de caché) y 134.724 de
  salida, en 82 minutos de llamadas.

## El cupo de GPT, recalibrado

El medidor de Nico pasó de 97% a 88% restante entre la cuarta revisión y el final
de los brazos: 9 puntos para unos 21,7 millones de tokens de entrada (las rondas 4
a 7, `logs` y `brazos`), más de 70% de caché. Es alrededor de un punto cada 2,4
millones de entrada, no cada 1,25 como estimó el piloto (`11`), que tenía menos
caché.

## Lo que sigue

`juez` (§6.2), con el OK de Nico: el juez ciego sobre los 400 JSON, en un orden
sorteado que mezcla brazos y condiciones. Los JSON sin textos libres o ilegibles no
llaman al modelo. Después, `validacion`, la planilla de Nico.
