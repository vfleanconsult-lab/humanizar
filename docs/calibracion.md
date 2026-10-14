# Calibración con informes reales

Respuesta corta: el detector estaba bien orientado, pero marcaba mucho que es normal en un informe de negocios. Con 9 informes de un curso con simulador de negocios, los ajustes bajaron los falsos positivos de §8, §12, §14, §20 y §21, y mostraron dos huecos: las negritas con dos puntos (§19) y las frases que hablan del propio informe (§25). Las señales que más aparecen son los gerundios colgados (§15) y las listas con etiqueta en negrita (§19).

Estas cifras no prueban que un texto sea de IA. Miden señales de estilo, y algunas son comunes en cualquier informe formal.

## Muestra

- 9 informes en Word, con 48.229 palabras de prosa. Se quitaron las tablas, las imágenes y los índices automáticos.
- Quedaron fuera 2 PDF escaneados (sin texto que leer), 3 presentaciones y una planilla de pauta.
- Los informes son de un solo curso y de un solo semestre. Los de un mismo curso comparten encargo, pauta y vocabulario.

Este repositorio es público. Aquí hay solo cifras agregadas y frases cortas de ejemplo.

## Método

1. Convertir cada Word y PDF a texto con `markitdown`.
2. Quitar tablas, imágenes e índices.
3. Pasar el texto por `scripts/marcar.py` de la versión 1.0.0 y de la 1.1.0.
4. Contar patrones, informes donde aparecen y marcas por cada 100 palabras.
5. Buscar frases repetidas: secuencias de 3 y 4 palabras en 5 informes o más, palabras de 5 letras o más con 8 usos o más en 5 informes o más, y los dos primeros términos de cada oración.

## Qué marca el detector

| § | Patrón | Informes (de 9) | Marcas con 1.0.0 | Marcas con 1.1.0 | Por 100 palabras (1.1.0) |
|---|--------|-----------------|------------------|------------------|--------------------------|
| 1 | No es X, es Y | 3 | 3 | 3 | 0,01 |
| 8 | Rayas como conector | 1 | 41 | 3 | 0,01 |
| 10 | Conectores de plantilla | 7 | 28 | 28 | 0,06 |
| 11 | Pasiva perifrástica | 1 | 1 | 1 | menos de 0,01 |
| 12 | Palabras sobreusadas | 0 (antes 9) | 32 | 0 | 0 |
| 13 | Importancia inflada | 1 | 1 | 1 | menos de 0,01 |
| 14 | Relación vaga | 3 | 18 | 7 | 0,01 |
| 15 | Gerundios colgados | 9 | 168 | 161 | 0,33 |
| 16 | Lenguaje publicitario | 1 | 1 | 1 | menos de 0,01 |
| 18 | Evitar ser y tener | 4 | 5 | 5 | 0,01 |
| 19 | Negritas decorativas | 6 | no existía | 177 | 0,37 |
| 20 | Mayúscula en cada palabra del título | 3 | 35 | 26 | 0,05 |
| 21 | Ortotipografía a la inglesa | 0 (antes 1) | 1 | 0 | 0 |
| 25 | Escribir sobre el documento | 7 | no existía | 8 | 0,02 |

El total sube de 0,69 a 0,87 marcas por cada 100 palabras porque la versión 1.1.0 detecta §19 y §25. Sin §19 baja a 0,51.

Densidad por informe, de todas las señales: de 0,23 a 1,96, con mediana de 0,92. El texto de ejemplo del README, escrito para tener señales, da 14,5. Ningún informe de la muestra pasa de 2.

## Frases nuevas

Casi todo lo que se repite es vocabulario del encargo: "costo medio total", "barreras de entrada y salida", "descripción del sector industrial". La pauta lo pide, así que no es señal.

Se agregaron tres cosas que se repiten en varios informes y que la skill no tenía:

- **§25:** "el presente informe analiza, documenta, expone...", 8 veces en 7 informes. La skill solo traía "este informe se organiza en tres secciones".
- **§15:** los gerundios "asegurando" (6 usos en 4 informes), "manteniendo" (7 en 5) y "priorizando" (5 en 4).
- **§19 en el detector:** la skill ya describía las etiquetas en negrita con dos puntos, pero `marcar.py` no las buscaba. Hay 177 en 6 informes.

Se descartaron, con el motivo:

| Candidata | Datos | Motivo |
|-----------|-------|--------|
| "Sin embargo" al inicio de oración | 21 veces, 8 informes | Conector normal; la señal es uno en cada párrafo |
| "mediante", "permitió" | 53 veces cada una, 9 y 8 informes | Formales, pero normales en un informe |
| "estratégico", "alineamiento", "gestión" | 71, 18 y 82 veces | Vocabulario del curso |
| "Esto nos permitió comprender que..." | 8 veces, 1 informe | No se repite en varios informes |

## Falsos positivos corregidos

| § | Qué marcaba | Por qué es normal | Ajuste |
|---|-------------|-------------------|--------|
| 8 | Guiones en índices, títulos, rótulos ("Período 1 – grupo"), rangos ("P1 - P3") y listas ("Visión - Misión") | No son conectores en prosa | Ignora índices y líneas de título o negrita. El guion y la semiraya cuentan solo entre palabras en minúscula. Suma el inciso con guion pegado (-así-), que la skill ya describía |
| 12 | "integral" (11), "optimizar" (6), "fundamental" (5) y similares | En un informe de negocios nombran objetivos y términos del ramo | Cuenta solo con 3 marcas o más en un párrafo, como pide el propio §12. "clave" nunca estuvo en la expresión |
| 14 | "costos asociados a la operación", "en el marco de la asignatura" | Nombran la relación | Ignora esos casos |
| 15 | ", cuando" | No es gerundio | Exige terminación -ando, -iendo o -yendo y excluye "cuando" |
| 20 | Títulos en mayúsculas sostenidas | Es la plantilla del curso, no un calco del inglés | Cuenta solo la mayúscula inicial en cada palabra, aunque haya conectores en medio |
| 21 | "S.I. o Mercado?" dentro de una pregunta con ¿ | La abreviatura cortaba la búsqueda del ¿ | Mira el inicio de la línea |
| 19 | Un campo de portada como "**Empresa:** nombre" | Es un campo, no una explicación | Pide 6 palabras o más después de la etiqueta |

Sobre §15: revisé a mano 22 de las 168 marcas y unas 8 eran gerundios colgados de verdad ("..., generando una severa pérdida"). El resto decía cómo se hizo algo ("..., redactando la misión"). Por eso `SKILL.md` ahora distingue los dos usos. Es una lectura mía, no una revisión ciega.

El ajuste de §12 tiene un costo: en los ejemplos "Antes" de `SKILL.md` las marcas de §12 bajan de 9 a 6, porque algunos ejemplos tienen solo dos palabras juntas.

## Prueba de humanización

Humanicé la prosa de 2 informes con `SKILL.md` y comparé antes y después.

| | Informe A | Informe B |
|---|-----------|-----------|
| Palabras | 3.987 → 3.822 | 3.012 → 2.855 |
| Marcas por 100 palabras | 1,96 → 0,24 | 1,56 → 0 |
| Cifras (contadas) | 383 → 383 | 214 → 214 |
| Siglas y términos del simulador | 95 → 95 | 63 → 63 |

Las 9 marcas que quedan en A son la bibliografía, la cita de la visión y la misión (que la skill manda no tocar), un "Además" que escribí yo y un gerundio de una lista de objetivos. Las cifras y los términos se contaron con una expresión regular; que el conteo coincida no prueba que cada cifra siga en su oración.

Fallas encontradas y qué se corrigió:

1. **Una oración sobre el propio informe.** Al reescribir una introducción escribí "este informe expone...". El detector la marcó. `SKILL.md` ahora trae ese ejemplo en §25 y dice que, si la pauta exige un objetivo, se deja como objetivo ("El objetivo es evaluar X").
2. **Dos cambios de sentido que el conteo no ve.** "esenciales para la dieta" pasó a "parte de la dieta", y "firmas emergentes que buscamos" pasó a "todas buscamos". Los encontré al releer. El paso 3 de `SKILL.md` ahora pide revisar grados y cuantificadores.
3. **Datos del informe.** No hubo cifras ni siglas cambiadas. El modo archivo ahora lista cifras, fórmulas, tablas, índices, bibliografía, siglas y términos del ramo entre lo que no se toca.

## Límites

- La prueba de humanización la hizo el mismo modelo que corrigió las instrucciones, y nadie la revisó a ciegas.
- Dos informes no alcanzan para sacar conclusiones sobre otros cursos.
- No se probaron tablas, imágenes ni PDF escaneados.
- Todos los informes comparten pauta. Una frase repetida puede venir de la pauta y no de una IA.
- Una densidad baja no descarta IA y una alta no la confirma. Compara siempre con textos del mismo curso.

## Cómo repetirlo

```bash
markitdown informe.docx > informe.txt
python3 scripts/marcar.py informe.txt
```

Quita tablas e índices antes de medir, o las cifras se inflan. Para repetir la búsqueda de frases hay que contar secuencias de palabras en varios informes; el detector no lo hace.
