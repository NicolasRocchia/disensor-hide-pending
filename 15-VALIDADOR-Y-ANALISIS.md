# El validador de §5.3 y el análisis de C2, escritos antes de que exista un dato

**13/10/2026, 17:20 ART.** Con el OK de Nico, Claude Code escribió
`herramientas/validador.py` y `herramientas/analisis.py` y sus pruebas
(`prueba_offline.py`, 91 de 91). Ninguna llamada a modelos.

## El validador (§5.3)

- **Esquema:** `jsonschema` 4.26.0, `Draft202012Validator` sin verificar formatos,
  el mismo que usa `rules.py` de disensor. Cada JSON contra su fragmento.
- **Reglas de A2:** R1, R2, R2 bis y R8, con `GENERIC_MARKERS`, `RESIDUE_STATES` y
  las clases esperadas copiados textuales de `rules.py` en `de14e5c`. A diferencia
  de `rules.py`, que supone un artefacto ya válido, éstas toleran un JSON mal
  formado.
- **Las pruebas dejaron ver un detalle del esquema que conviene tener presente:**
  los ids tienen forma fija (`h1`, `h2`… para hallazgos; `r1`… para items de
  residuo) y el título tiene un largo mínimo. Un sujeto que use `F1` no cumple el
  esquema, aunque el JSON diga todo lo que tiene que decir. Es sólo descriptivo:
  no cambia C2.
- `jsonschema` no es de la biblioteca estándar; está en el site de usuario como
  dependencia de disensor. Desde ahora las pruebas corren sin `python -I`.

## El análisis (§2.1, §6.3, §6.4, §8.1, §9)

- **La prueba de §2.1:** permutación exacta por cambio de signo, bilateral, con la
  distribución contada con coeficientes binomiales sobre las diferencias de valor
  1 y 2 (sin enumerar 2^n casos). Se rechaza con p ≤ 0,05.
- **Reproduce la tabla de potencia de §6.4**, que había calculado la sesión de
  difusión por su cuenta:

  | A2b registra / falso positivo | A2 registra / falso positivo | Escrita | Reproducida |
  |---|---|---|---|
  | 20% / 0% | 40% / 0% | 84% | 84,4% |
  | 30% / 0% | 50% / 0% | 79% | 79,2% |
  | 40% / 0% | 60% / 0% | 77% | 77,6% |
  | 40% / 0% | 70% / 0% | 99% | 98,9% |
  | 30% / 5% | 50% / 10% | 44% | 44,9% |
  | 40% / 5% | 70% / 10% | 86% | 86,9% |

  Con los brazos iguales rechaza entre 3,1% y 3,7%, el «entre 3% y 4%» de §6.4.
- **Exclusiones:** un log sale de C2 para los dos brazos si alguna de sus cuatro
  llamadas no terminó o si el juez falló en alguno de sus cuatro JSON.
- **§8.1:** la muestra estratificada (15 `true` y 15 `false`) se sortea con
  semilla entre los JSON que el juez leyó, y se le entrega a Nico sin la etiqueta
  del juez. La prueba recalculada usa las etiquetas de Nico sólo en los ítems
  decisivos. **Probado que las etiquetas sólo pueden quitar una afirmación:** un
  juez que da significativa y unas etiquetas que la bajan dan «sensible al juez»;
  un juez que no da, con etiquetas que «la crearían», sigue en «no detectamos».
- **La frase de §9 la elige el script**, no quien lee los datos.

## Dos decisiones que quedan antes de congelar

1. **El intervalo de «s_json aumentó en X [intervalo]».** §9 no decía cuál.
   Propuesto: percentil 2,5 y 97,5 de la media de las diferencias pareadas en
   10.000 remuestreos de logs, semilla 20261013.
2. **Una C2 significativa en contra de A2.** La prueba es bilateral, pero §9 sólo
   escribió la frase a favor. El script dice «C2 da significativa en contra de A2:
   `s_json` disminuyó en X [intervalo]» y avisa que §9 no la escribió; hay que
   escribirla en §9 antes de congelar.

## Lo que falta antes de congelar

La etapa de la corrida real (logs y gemelos hasta 100 pares con la adjudicación
de Nico; después los brazos intercalados, la extracción, el validador y el juez),
que arma el `pares.json` que lee el análisis. Y la tercera revisión independiente.
