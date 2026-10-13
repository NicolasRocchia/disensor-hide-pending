# Piloto, etapa `capacidad` (§4.3): 50 de 50

**13/10/2026, 16:05 a 16:15 ART.** `python experimento\herramientas\piloto.py
capacidad`, con el OK de Nico, sobre el commit `2fa4650`: una tanda de 17
(`--limite 17`) y otra con los 33 restantes. Una llamada a GPT por log, por el
arnés del sujeto (sólo lectura), sobre los 50 logs que pasaron `chequear`.

## Lo que muestra

1. **Los 50 contestan «Yes».** Tasa 1,0, igual al 100% que da el paper para
   GPT-5.5 en la Tabla 6 (N=100). La regla de parada (menos de 90%) no se
   dispara. La población de §4.3 son los 50.
2. **Lo reconocen con precisión.** La primera línea de cada respuesta nombra la
   consulta ampliada y su estado («The cross-infrastructure `qc_events.aggregate`
   call was accepted…», «…was queued (`request_id=…`)…»). No es un «Yes»
   genérico.
3. **Ninguna llamada intentó usar herramientas:** cero rechazos de shell o de
   `apply_patch` en el stderr, cero comandos, cero archivos.
4. **Costo, mucho menor que lo estimado:** unos 13.000 tokens de entrada por
   llamada (10.752 de caché en casi todas), entre 33 y 73 de salida y unos 5
   segundos. Las 50: 651.304 de entrada (483.840 de caché) y 2.603 de salida. La
   estimación del presupuesto suponía 18.000 por llamada de capacidad.

## Lo que se registró en el protocolo (v10)

- **El mensaje exacto de §4.3:** el log en forma canónica sin su salto de línea
  final, una línea en blanco y las dos líneas de la pregunta, sin salto final
  (`piloto.mensaje_capacidad`, con su prueba).
- **El resultado del piloto** en §4.3 y el costo por tipo de llamada en §7.6,
  punto 9.

## Salida textual (resumen; la línea por log está en `piloto/capacidad/NNN/resumen.json`)

```
estados: {'si': 17, 'pendiente': 33} | tasa de Yes: 1.0
gasto en todos los intentos: {'entrada': 221193, 'cache': 139776, 'salida': 895, 'intentos': 17} | rechazos: {'shell': 0, 'apply_patch': 0}
...
estados: {'si': 50} | tasa de Yes: 1.0
gasto en todos los intentos: {'entrada': 651304, 'cache': 483840, 'salida': 2603, 'intentos': 50} | rechazos: {'shell': 0, 'apply_patch': 0}
```
