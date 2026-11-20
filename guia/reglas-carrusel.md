# Reglas de los carruseles (aprobadas por Juanpa, 19/11/2026)

## Volumen diario
- **6 carruseles al día:**
  - 3 para Valu y 3 para Sofi.
  - Cada cuenta lleva uno de cada tipo: LISTA IDENTIFICABLE, PHOTO DUMP y MODELO APROBADO.
- **Los 6 llevan temas y textos distintos entre sí.** Nunca el mismo carrusel en las dos cuentas.
- **Formato:** 1080×1080 y 5–7 slides (portada + 4–6).

## Regla de CTA (manda sobre todo)
- **Lumina aparece SOLO en la ÚLTIMA slide.** Va como parte natural de la historia, en primera persona.
  - Ejemplos: "mis 5 min de 528 Hz en Lumina antes de dormir cambiaron mis noches"; "termino con mi frecuencia de 528 Hz en Lumina".
- **Prohibido en cualquier slide:**
  - teléfono o captura de la app
  - logo
  - "descárgala", "link en bio", "descargar ahora"
  - dos CTA
  - cualquier CTA en slides del medio
- **Por qué:** dos CTA en el medio bajaron las vistas de la referencia de ~2.000 a ~500. La meta es la curiosidad, que la gente busque "Lumina Manifestación" por su cuenta.
- **Lumina solo como cierre:** el resto del carrusel tiene que valer por sí solo, sin la app.

## Los 3 tipos
1. **LISTA IDENTIFICABLE (ganador).**
   - **Portada:** la chica + un gancho de identificación ("señales de que estás entrando en tu era de calma", "cosas que solo entiende alguien que está manifestando").
   - **Slides:** una foto bonita + un ítem numerado con el que la gente diga "soy yo", con subtítulo chico gracioso o tierno.
   - **Pie de foto = PREGUNTA**, para que comenten: "¿cuántas eres tú?", "¿cuál te pasa más?".
2. **PHOTO DUMP (ganador).**
   - **Portada:** la chica + "consejos que me hubiera gustado saber cuando empecé a manifestar" (variar el gancho), con "(photo dump)" debajo.
   - **Slides:** `"estilo": "dump"`, una sola frase corta abajo, en minúscula, como escrita por una usuaria.
   - **Pie de foto:** pregunta ("¿cuál me faltó?").
3. **MODELO APROBADO (paso a paso o "cosas que dejé de hacer").**
   - **Portada:** "mi ritual de 5 minutos para…" o "cosas que dejé de hacer cuando…", con "(paso a paso, guárdalo)" o "(guárdalo)".
   - **Slides:** pasos numerados con título + subtítulo.
   - **Pie de foto:** pregunta o invitación a guardar.

## Ejemplos aprobados (no repetir estos temas)
- **Valu, photo dump:** "consejos que me hubiera gustado saber cuando empecé a manifestar". Escríbelo a mano / empieza con algo chiquito / háblate bonito frente al espejo / (último) mis 5 min de 528 Hz en Lumina antes de dormir cambiaron mis noches.
- **Valu, lista:** "señales de que estás entrando en tu era de calma". Ya no contestas al instante / tu cuarto huele a vela / dices que no sin explicar / te alegras por otras / (último) cierras el día con 5 min de 528 Hz en Lumina.
- **Valu, modelo:** "mi ritual de 5 minutos para escribir lo que quiero". Cuaderno solo para esto / fecha arriba / en presente / leerlo una vez / (último) termino con mi frecuencia de 528 Hz en Lumina.
- **Sofi, lista:** "cosas que solo entiende alguien que está manifestando". 11:11 / libreta que nadie lee / gracias al vaso de agua / luna llena y limpieza / (último) frecuencia de Lumina hasta para estudiar.
- **Anteriores:** "5 rituales de 5 minutos antes de dormir", "cosas que dejé de hacer cuando empecé a manifestar en serio", "el ritual del vaso de agua cada mañana", "3 cosas que hago cada mañana para no perder mi energía".

## Texto para subir (título, descripción, hashtags)
Nada de cero. El título y la descripción modelan un post de referencia concreto, encontrado hoy en TikTok o guardado en `investigacion/`. Los hashtags salen de los que usan las referencias con más vistas. El agente anota de dónde salió cada uno.

## Fotos
- **Portada:**
  - Solo sale la chica de esa cuenta y solo en la portada.
  - La ruta va dentro de `fotos/valu/` o `fotos/sofia/`, para que carrusel.py lea `caras.json` y la CENTRE con la cara completa y libre (título debajo del mentón).
  - Mirar la portada renderizada: si el texto tapa la cara o se ve cortada, cambiar de foto.
- **Slides del medio:**
  - Valu usa `fotos/apoyo/`. Sofi usa primero `fotos/apoyo-sofia/` y luego `fotos/apoyo/`.
  - Cada nombre de archivo describe la foto: elegir la que ilustre literalmente el texto.
- **No repetir:**
  - Portada de Valu: no en 7 días (22 fotos).
  - Portada de Sofi: no en 3 días (9 fotos).
  - Foto de apoyo: nunca dos veces el mismo día; entre días, la menos usada según `registro.md`.
- **Prohibido en las fotos:**
  - alcohol
  - logos o marcas visibles (Apple, Netflix, Chanel, Zara, apps)
  - dinero o lujo
  - parejas
  - textos en inglés grandes
- **Fotos nuevas:** si al mirar la hoja de contacto aparece algo de esto, cambiar la foto y anotarla en "fotos vetadas" de `registro.md`.

## Texto
- **Tono:** minúscula, primera persona o "tú" de amiga, frases cortas.
  - Título ≤ 10 palabras; subtítulo ≤ 9.
  - Tildes y ñ siempre bien. Sin emojis dentro de las slides (la fuente no los dibuja); en el pie de foto sí.
- **Nada de promesas:** "funciona siempre", "en 24 horas", "te llega el dinero", "él vuelve". El ángulo es hábito, calma, intuición, ritual, amor propio, gratitud, constancia, dormir, claridad.

## Render
```
python3 herramientas/carrusel.py spec.json salida/AAAA-MM-DD/VALU-1-lista
python3 herramientas/hoja.py salida/AAAA-MM-DD/VALU-1-lista salida/AAAA-MM-DD/VALU-1-lista_hoja.jpg
```
- **spec.json:** una lista con un objeto por slide: `{"foto": "fotos/valu/valu-19.jpg", "portada": true, "texto": "...", "sub": "(guárdalo)"}`. En las slides del medio, `"portada": false` (o se omite) y `"estilo": "dump"` si es photo dump. `"sub"` puede ser null.
- **Lo que hace el script:** la portada centra la cara; las slides normales van con el texto centrado (y≈540); las dump, con el texto abajo (y≈800).
- **Revisión:** abrir (Read) cada hoja de contacto y revisar tildes, legibilidad, cara libre, fotos sin marcas, que Lumina esté solo en la última y que no haya CTA en el medio.

## Plan B (si TikTok no carga o pide sesión)
Usar los ángulos guardados en `investigacion/` de días anteriores y los "ángulos de reserva" de `guia/aprendizajes-referencia.md`, y decir en una línea que hoy no se pudo investigar.
