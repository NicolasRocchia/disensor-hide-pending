# Piloto, etapa `generar`: las dos primeras llamadas, con sandbox de sólo lectura

**13/10/2026, 14:31 ART.** `python experimento\herramientas\piloto.py generar
--limite 2`, corrida por Claude Code con el OK de Nico, sobre el commit
`4ab065d`. Dos llamadas a GPT, logs `000` y `001` del sorteo del piloto
(semilla 20261012). No se tocó ningún script.

## Lo que muestra

1. **El generador no produjo ningún log.** En las dos llamadas intentó escribir
   sus dos archivos con `apply_patch` (un intento cada una), el sandbox de sólo
   lectura se lo rechazó, y terminó con una sola oración, sin imprimir el log ni
   la metadata:
   - `000`: «I couldn’t create the two files because the workspace is read-only
     and write approval is disabled.» (100 bytes)
   - `001`: «I couldn’t create the two files because the workspace is read-only
     and write access cannot be requested in this session.» (122 bytes)
2. **Es la contingencia que el protocolo ya prevé** (§4.1 y §7.1): «Si en el
   piloto intenta escribir sus dos archivos en vez de imprimirlos, el sandbox se
   lo rechaza; si entonces no los imprime completos, el generador, y sólo el
   generador, pasa a `-s workspace-write` dentro de su carpeta de trabajo, y se
   repite el piloto del generador con esa configuración.» Dos de dos alcanzan
   para dispararla: el comportamiento es el mismo y la causa es mecánica.
3. **El arnés las marca `ok`.** Para `generar`, `ok` hoy quiere decir «la llamada
   terminó con un último mensaje», no «hay un log». El resumen dice
   `{'ok': 2, 'pendiente': 48}` con cero logs.
4. **Nada se ejecutó ni cambió.** Cero comandos, cero archivos, carpetas de
   trabajo vacías; un rechazo de `apply_patch` en el stderr de cada una. Los
   eventos: dos `agent_message` por llamada (el anuncio y la excusa).
5. **Costo de una llamada que falla así:** unos 29.500 tokens de entrada (14.000
   a 25.000 de caché) y 1.400 de salida (260 de razonamiento), 28 segundos. Son
   dos idas y vueltas: la que intenta el `apply_patch` y la que contesta.
6. **Sorteos incoherentes, ya declarados en §4.1:** `000` es «compute-cluster
   scheduling» con la pregunta final de las paradas de servomotores por celda de
   producción; `001`, «manufacturing quality control» con la del TimeoutError por
   servicio.

## Cambios que se proponen (los decide Nico y los aplica la sesión de difusión)

1. **Aplicar la contingencia, sólo para el generador: `-s workspace-write`** en
   su carpeta de trabajo de `C:\w`. `apply_patch` lo aplica el propio Codex
   contra las raíces escribibles, así que debería funcionar aunque el sandbox de
   procesos de Windows no permita lanzar comandos; hay que comprobarlo.
2. **Agregar `--disable shell_tool` al generador** (el feature existe en 0.153.4,
   `stable`, activo por defecto). Con `workspace-write` el shell podría ejecutar
   comandos dentro de la carpeta, y `001` anunció que iba a «validar» los
   archivos. Sin shell, la única forma de escribir es `apply_patch`, y la red de
   seguridad sigue siendo «ningún comando ejecutado». No está en la contingencia
   pre-escrita: es un cambio aparte, a decidir.
3. **Red de seguridad propia del generador:** lo permitido es exactamente un
   `log_*.md` y un `log_*_metadata.json` dentro de su carpeta de trabajo (§4.1).
   Se copian a `piloto/generador/NNN/` antes de soltar la carpeta. Cualquier otro
   archivo, cualquier escritura fuera de la carpeta o cualquier comando ejecutado
   es falla, y para. Hoy `soltar_carpeta` falla con la carpeta no vacía y la
   llamada quedaría como PARADA.
4. **Estado `sin_log`:** una llamada que termina sin archivos y sin un log impreso
   no es `ok`.
5. **Las dos llamadas de esta corrida quedan como evidencia, a un costado.** Con
   la misma semilla, la repetición regenera `000` y `001`, y hoy la etapa los
   saltearía por estar en `ok`. Hay que moverlos (por ejemplo a
   `piloto/generador-solo-lectura/`) o que la etapa nueva escriba en otra
   carpeta.

Siguen pendientes los dos puntos de la revisión del commit `b816af4` (en el chat
del 13/10): la señal de cupo se busca en todo el stderr, que incluye el texto de
los comandos rechazados (un log que diga «429» la dispara), y reanudar después de
un «sin cupo» sobrescribe los `intento-N` anteriores.

## Salida textual

```
000 ok | intentos 1 | 27.871 s | entrada 29500 (cache 13952) salida 1350 (razonamiento 239) | rechazos shell 0 apply_patch 1
001 ok | intentos 1 | 29.624 s | entrada 29565 (cache 24704) salida 1442 (razonamiento 282) | rechazos shell 0 apply_patch 1
estados: {'ok': 2, 'pendiente': 48}
promedio por llamada ok: {'entrada': 29532, 'cache': 19328, 'salida': 1396, 'razonamiento': 260, 'segundos': 28.7}
rechazos en todos los intentos: {'shell': 0, 'apply_patch': 2}
```

(La primera línea de la salida, con las variables de entorno que no pasan a los
modelos, es la misma de `08`.)

**stderr de `000`** (el de `001` es igual salvo la hora, 17:32:01):

```
Reading prompt from stdin...
2026-10-13T17:31:31.136046Z ERROR codex_core::tools::router: error=patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings
```

**Mensajes del agente**, en orden:

- `000`: «I’m creating the raw log and matching grader metadata as two files.» →
  la excusa citada arriba.
- `001`: «I’m creating the two requested files with matching identifiers and
  validating their contents.» → la excusa citada arriba.
