# PLAN de Carruseles Lumina · 2026

Documento de evolución y medición del proyecto.

---

## Fase 1: Exploración de Formatos (Semanas 1–2 desde 20/11/2026)

**Objetivo:** Probar los 13 formatos visuales (F01–F13) para medir cuál rinde mejor.

### Rotación

**F01–F11 (exploración normal):**
- Cada día: mínimo 2 formatos nuevos (excepto F01, que es control)
- Nunca: dos carruseles del mismo formato el mismo día
- Cada formato: sale ≥2 veces en las 2 semanas

**F12 & F13 (prueba intensiva desde día 1):**
- 1 carrusel diario alternando F12 y F13 (días 1, 3, 5… F12; días 2, 4, 6… F13)
- Mantener durante 2 semanas (14 carruseles: 7x F12, 7x F13)
- Medir guardados + compartidos vs control (F01)

### Métricas a Registrar (en `formatos/registro-formatos.csv`)
- Vistas a 48h
- Likes
- Guardados (peso: alto)
- Compartidos (peso: alto)
- Comentarios
- Comentarios mencionando "SEÑAL" (específico de Lumina)

### Multiplicador
```
Multiplicador = (Guardados + Compartidos) / promedio general últimos 30 días
```

Ejemplo:
- Formato A: guardados 450, compartidos 320 → 770 interacciones
- Promedio general: 180 interacciones
- Multiplicador de A: 770/180 = 4,3×

---

## Fase 2: Explotación (Desde Semana 3)

**Distribución (60/30/10):**
- **60%:** 2 formatos con mejor multiplicador (top)
- **30%:** Formatos con multiplicador medio (1–2.5×)
- **10%:** Formatos nuevos en prueba o pausados

### Criterios F12 & F13 (después de 2 semanas)
- **Superan 1,5×:** pasan a ser fijos (2 por día alternando)
- **Entre 0,5× y 1,5×:** continúan en rotación normal
- **Menores 0,5×:** se pausan

### Pausa
Formato con multiplicador < 0,5× después de 4+ publicaciones se mueve a `formatos/pausados/`.

---

## Búsqueda Semanal (Cada Domingo)

1. Revisar TikTok: manifestación, espiritualidad, hábitos, signos, números (500K+ vistas mínimo)
2. Buscar formatos NUEVOS no en la biblioteca
3. Escribir receta sin copiar texto
4. Crear `formatos/FXX-nombre.md`
5. Implementar plantilla en `carrusel.py`
6. Probar en `salida/prueba-formatos/`
7. Incluir en cupo 10%
8. Anotar en `guia/aprendizajes-referencia.md`: origen, estructura, qué no copiar

---

## Checklist de Implementación (20/11/2026)

**F01–F11:**
- [x] Especificaciones F01–F11 creadas
- [x] `carrusel.py` extendido para soportar formatos
- [x] `registro-formatos.csv` inicializado
- [x] `formatos/indice.md` documentado
- [x] Agente actualizado para incluir formato en cada slide
- [x] `guia/reglas-carrusel.md` actualizada
- [x] `muestrario.png` generado

**F12–F13:**
- [x] Especificaciones F12 (Storytime) y F13 (Chat) creadas
- [x] `render_F12_storytime()` y `render_F13_chat()` implementadas
- [x] `carrusel.py` integrado con nuevos formatos
- [ ] Próxima ejecución: rotación diaria F12/F13 + F01–F11 exploración
- [ ] Medir multiplicadores después de 2 semanas

---

## Notas

- **Fotos:** Nunca cambiar. Siempre reales del banco de fotos (`fotos/`).
- **Regla de CTA:** Lumina SOLO en última slide. Nunca teléfono, logo o "descárgala".
- **Texto:** Copiar estructura, no palabras ajenas.
- **Dato:** El formato NO debería cambiar la esencia (tema, tono, foto). Solo la **presentación visual**.

---

## Contacto para Cambios

Si un formato claramente no funciona (< 2× multtiplicador):
1. Mover a `formatos/pausados/`
2. Buscar referencia nueva que lo inspire
3. Proponer mejora o remplazo a Juanpa
