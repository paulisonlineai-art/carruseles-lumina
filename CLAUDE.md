# Lumina · Carruseles diarios (Claude Code)

Proyecto de Juanpa (Juan Pablo). Responde SIEMPRE en español.

Lumina es una app de manifestación con frecuencias Solfeggio (528 Hz), diario, tablero de visión, "Pide una señal" y fases de la luna. Esta carpeta produce **6 carruseles al día** para TikTok:

- **3 para Valu** (@valu.manifiesta): la chica rubia, fotos en `fotos/valu/`.
- **3 para Sofi** (@manifiesta.con.sofia): la chica morena de pelo ondulado, fotos en `fotos/sofia/`.

## Cómo se corre
- **Comando:** `/carruseles` hace el día completo con el agente `carruseles-lumina`. Abre Claude Code con Chrome conectado (`claude --chrome`) para que pueda investigar TikTok.
- **Antes de empezar:** lee, en este orden, `guia/reglas-carrusel.md`, `guia/aprendizajes-referencia.md`, `guia/marca.md` y `registro.md`.

## Mapa de la carpeta
- `guia/`: reglas, aprendizajes de la referencia y reglas de marca. **Mandan sobre cualquier idea nueva.**
- `fotos/`: fotos REALES que subió Juanpa, la única fuente de imágenes.
  - `valu/` y `sofia/`: portadas, con `caras.json` para centrar la cara.
  - `apoyo/` y `apoyo-sofia/`: slides del medio.
  - Nunca generar imágenes con IA ni bajar fotos de internet para los slides.
- `herramientas/carrusel.py`: renderiza un carrusel desde un spec.json. `herramientas/hoja.py` arma la hoja de contacto.
- `investigacion/AAAA-MM-DD.md`: lo que se encontró en TikTok ese día.
- `salida/AAAA-MM-DD/`: los carruseles del día. Al final se copian también a `~/Downloads/Lumina-carruseles/AAAA-MM-DD/`.
- `registro.md`: historial de temas, tipos y fotos usadas por cuenta. **Leerlo antes de elegir y actualizarlo al terminar.**

## Límites
- **TikTok es SOLO LECTURA:** nunca dar like, seguir, comentar, guardar, compartir, enviar mensajes ni publicar.
- **No iniciar sesión:** si TikTok pide iniciar sesión, seguir con lo que se vea sin sesión; si no se ve nada, usar el plan B de `guia/reglas-carrusel.md`.
- **Nada se publica:** Juanpa publica a mano.
- **Contenido ajeno:** no copiar textos literales de otros creadores. Se modela el ÁNGULO y la ESTRUCTURA, con palabras propias.
- **Comandos:** no correr comandos fuera de esta carpeta, salvo copiar la salida a `~/Downloads` y `pip install pillow` si falta.
