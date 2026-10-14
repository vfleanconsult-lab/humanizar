# Historial de cambios

## 1.4.0

- `scripts/marcar.py`: §1 detecta el contraste partido en dos oraciones ("no es X. Es Y", "no significa X. Significa Y") y "no como X, sino". §27 suma "en post de", "ejemplo estelar", "un gran ejemplo de", "mejoras tremendas", "se embarcó en una misión" y "demuestra consistentemente". No se recalibró con los textos humanos de 2010.
- `SKILL.md`: §27 lista los mismos calcos.
- `README.md` y `scripts/marcar.py`: aclaran que el script es una guía de edición y no un detector de autoría. Con 4 artículos generados con IA, la densidad cayó dentro del rango de los informes humanos. Detalle en `docs/investigacion.md`.

## 1.3.0

- `README.md`: la instalación en Claude Desktop explica cómo armar un ZIP sin los manifiestos de plugin, que Desktop rechaza.
- Calibración con 6 textos humanos de 2010 (10.909 palabras), usados como control: toda marca es un falso positivo. Resultados agregados en `docs/calibracion.md`.
- `scripts/marcar.py` junta los saltos de línea de los PDF, quita espacios dobles y pega palabras cortadas por guion antes de buscar. En un .pptx no junta líneas, porque cada viñeta es una línea.
- `scripts/marcar.py`: el guion y la semiraya en §8 cuentan con 2 marcas por párrafo; "de alguna manera" en §9 también; sale "imperdible" de §16, "cuenta con" de §18 y los meses con mayúscula de §21; "eventualmente" en §27 solo al abrir una oración; la coma antes de "y" en §21 solo en series; "incluyendo", "dependiendo", "hablando", "siendo" y similares no cuentan como gerundio colgado en §15.
- `SKILL.md`: §9, §15, §21 y §27 aclaran qué es habitual en textos humanos; §15 dice que es el patrón con más falsos positivos. Salen "imperdible" de §16 y "cuenta con" y "dispone de" de §18.
- `docs/investigacion.md` suma el respaldo de la muestra de 2010.

## 1.2.0

- Modo presentación en `SKILL.md`: revisa lámina por lámina, trata como prosa los párrafos y las notas del orador, no aplica §2, §11, §19 ni §25 a viñetas cortas ni a la lámina de agenda, pide títulos que digan la conclusión, no alarga el texto y entrega una tabla por lámina.
- `scripts/marcar.py` lee archivos .pptx sin dependencias externas: respeta el orden de las láminas, incluye las notas del orador, revisa los títulos con §20 e informa las señales por lámina.

## 1.1.0

- Calibración con 9 informes de un curso de negocios. Resultados agregados en `docs/calibracion.md`.
- `scripts/marcar.py` ignora índices de Word y líneas de título en §8, exige 3 marcas por párrafo en §12, deja pasar "costos asociados a" y "en el marco de la asignatura" en §14, ya no marca "cuando" en §15 ni títulos en mayúsculas sostenidas en §20, y no cuenta como falta de ¿ la pregunta que la lleva antes de una abreviatura (§21).
- `scripts/marcar.py` detecta ahora §19 (negritas con dos puntos) y §25 (frases sobre el propio informe).
- `SKILL.md`: §25 suma "el presente informe analiza..." y conserva el objetivo que exige una pauta; §15 suma "asegurando", "manteniendo" y "priorizando" y distingue el gerundio de modo; §12 y §14 aclaran el lenguaje de negocios.
- `SKILL.md`: el paso 3 pide revisar que no cambie un grado ni un cuantificador, y el modo archivo no toca cifras, fórmulas, tablas, índices, bibliografía, siglas ni términos del ramo.
- `docs/investigacion.md` suma el respaldo de los informes reales.

## 1.0.0

- Primera versión en español, adaptada de humanizer 3.1.0.
- 28 patrones en siete secciones. Las secciones A a F adaptan la guía de Wikipedia; la sección G (calcos del inglés y español neutro sin lugar) es nueva.
- Patrones nuevos o rehechos para el español: §6 tríadas y pares forzados, §8 rayas a la inglesa (la raya de inciso es norma en español), §10 conectores de plantilla, §11 pasiva perifrástica, §15 gerundios colgados, §20 mayúscula en cada palabra del título, §21 ortotipografía a la inglesa, §27 calcos del inglés y §28 español neutro sin lugar.
- Se quitó el patrón de guiones en adjetivos compuestos (hyphenated pairs), que no aplica al español.
- La skill respeta la variedad del español del escritor (tratamiento, vocabulario, formatos de número y fecha).
- `scripts/marcar.py` marca las señales detectables con palabras y puntuación.
- `docs/investigacion.md` reúne los estudios en español y el respaldo de cada patrón.
