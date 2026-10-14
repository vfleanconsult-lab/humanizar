# Guía para agentes

Cómo cambiar Humanizar sin romper el paquete ni el prompt.

## Qué contiene el repositorio

Humanizar es una skill escrita en Markdown. `SKILL.md` es el prompt que leen los agentes. No hay paso de compilación.

## Archivos clave

- `SKILL.md`: la fuente de verdad y el único archivo de skill. Tiene metadatos YAML y los patrones numerados en siete secciones, del más fuerte al más débil.
- `README.md`: instalación, uso y tablas de patrones.
- `CHANGELOG.md`: notas de versión, la más nueva primero.
- `docs/investigacion.md`: estudios y respaldo de cada patrón.
- `scripts/marcar.py`: detector de señales por palabras y puntuación.
- `scripts/validate-package.py`: revisa archivos y valores compartidos.
- `.claude-plugin/`, `.cursor-plugin/` y `agents/openai.yaml`: manifiestos para cada agente.

## Reglas para cambios

- **Patrones:** numerados desde 1 sin saltos. Si agregas, quitas o renumeras uno, actualiza las tablas del README, el título "Los N patrones", cada referencia § en `SKILL.md`, el número en `scripts/marcar.py` y la tabla de respaldo en `docs/investigacion.md`.
- **Respaldo:** un patrón nuevo debe indicar de dónde viene (Wikipedia, estudio en español, norma RAE o FundéuRAE, o lista de frases) en `docs/investigacion.md`.
- **Ejemplos:** el "Después" nunca agrega datos que no estén en el "Antes".
- **Versión:** la misma en `SKILL.md` (`metadata.version`), el primer título de `CHANGELOG.md` y los dos `plugin.json`.
- **Descripción:** los manifiestos usan la primera oración de la descripción de `SKILL.md`.
- **Largo:** `SKILL.md` se lee completo en cada uso; el validador lo limita a 5.500 palabras.
- **Revisión:** antes de publicar, corre `python3 scripts/validate-package.py`.

## Estilo

Escribe en español claro: la idea principal primero, palabras comunes, voz activa, oraciones cortas. La documentación de este repositorio debe pasar su propia skill.
