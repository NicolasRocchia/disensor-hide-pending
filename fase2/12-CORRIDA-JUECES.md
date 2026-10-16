# La corrida de la fase 2: `jueces` y `validacion`

**16/10/2026, 13:24 a 15:22 ART** (16:24 a 18:22 UTC), sobre el congelamiento de
`09cc6c3`, con el OK de Nico. Claude Code no abrió ningún veredicto, ninguna planilla,
`clave.json` ni `pares.json`: este informe sale sólo de los datos del arnés (estados,
intentos, costo).

## `jueces`

- **1.200 de 1.200 juzgados, todos en el primer intento:** 400 de Q.2.8 sobre los
  pendientes, 400 del juez de falsos positivos sobre los gemelos y 400 del juez
  «registra» sobre los JSON de A2b y A2. Ningún «juez falló», ninguna llamada sin
  terminar, ningún veredicto por regla (no hubo prosas vacías).
- **Ningún canario, ninguna caída, ninguna sesión vencida, ninguna `PARADA`.**
- **USD 26,93 a precio de API**, dentro de lo que estimó §16 con el piloto (USD 25 a
  30). Dos horas.
- Antes de empezar, `verificar` repitió el congelamiento de las dos fases, el plan,
  la descendencia y el ancla en el remoto.

## `validacion`

**71 ítems para Nico, en dos planillas** (`fase2/corrida/validacion/PARA-NICO-*.md`),
con ids opacos mezclados, la rúbrica textual de cada juez y, en los pendientes, la
metadata que recibe Q.2.8. Como en la fase 1, el arnés imprime sólo el total.

## Lo que sigue

Nico etiqueta las dos planillas sin ayuda de ningún modelo (§8), y sin abrir
`clave.json`, `pares.json`, `jueces/` ni `informe.json` hasta terminar. Las etiquetas
se commitean antes de analizar. Después, `analizar`.
