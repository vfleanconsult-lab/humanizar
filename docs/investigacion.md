# Investigación: ¿sirven en español las señales de IA de Wikipedia?

Respuesta corta: sí en la estructura y no en el vocabulario. Los patrones de estructura (contrastes "no es X, es Y", remates, tríadas, importancia inflada, restos del chat) aparecen igual en español porque vienen de cómo genera texto un modelo, no del idioma. Las listas de palabras y las reglas de puntuación sí hay que rehacerlas, y el español tiene señales propias que la guía en inglés no cubre: gerundios colgados, mayúscula en cada palabra de un título, calcos y un español neutro sin país.

## Qué existe y qué no

No hay una versión en español de la guía de Wikipedia. La guía "Signs of AI writing" la mantiene WikiProject AI Cleanup y está disponible solo en inglés; la prensa en español y portugués la cita, pero no encontré una página equivalente en es.wikipedia.org ([Fast Company Brasil](https://fastcompanybrasil.com/ia/como-saber-se-foi-a-ia-que-escreveu-wikipedia-faz-a-curadoria-dos-cliches/), [Olhar Digital](https://olhardigital.com.br/2025/11/21/pro/wikipedia-cria-guia-detalhado-para-identificar-textos-escritos-por-ia/), [Reason Why](https://www.reasonwhy.es/actualidad/wikipedia-documenta-inteligencia-artificial-uniformando-escritura-global)).

Sí hay estudios académicos con corpus en español. Son pocos, exploratorios y con modelos de 2023, así que sirven para confirmar tendencias generales más que para dar listas de palabras.

## Estudios en español

### Alonso Simón et al. (2024), Universidad Complutense de Madrid

"¿Tienen GPT-3.5 y GPT-4 un estilo de escritura diferente del estilo humano? Un estudio exploratorio para el español". *Revista Electrónica de Lingüística Aplicada* (RAEL), vol. 23, n.º 1, pp. 34-54. DOI [10.58859/rael.v23i1.666](https://matrix.aesla.org.es/RAEL/article/view/666). [PDF en el repositorio de la UCM](https://docta.ucm.es/rest/api/core/bitstreams/35114b65-3dbe-4613-b4d7-caa8bc2ba299/content).

- Construye un corpus comparable de textos humanos y de ChatGPT en español y aplica pruebas estadísticas.
- 17 variables lingüísticas muestran diferencias significativas entre humanos y los dos modelos. Las variables son de tres tipos: léxicas, de puntuación y de estructura sintáctica.
- Los textos humanos se diferencian sobre todo en la sintaxis.
- Los trabajos previos que revisa tienen resultados contradictorios sobre densidad y diversidad léxica.

Qué tomamos: la puntuación y la sintaxis son señales válidas en español (§8, §10, §11, §15, §21). Pendiente: el desglose de las 17 variables está en el PDF completo, que no pude descargar desde este entorno; conviene revisarlo para afinar las listas.

### Petrenko, Maslova, Lakhno, Rusachenko y Vydaichuk

"Análisis comparativo de las características lingüísticas y estilísticas de textos mediáticos humanos y generados artificialmente" ([Dialnet](https://dialnet.unirioja.es/servlet/articulo?codigo=10651021)).

- Compara periodismo auténtico con textos de ChatGPT, Gemini y BingAI mediante análisis de corpus, estilométrico, pragmático y discursivo.
- Los textos de IA tienen más corrección gramatical, sintaxis más estandarizada, menos metáforas y menos expresividad emocional.
- Propone cinco parámetros de "humanidad" de un texto: variabilidad gramatical, riqueza semántica, relevancia pragmática, organización retórica y expresión estilística.

Qué tomamos: la uniformidad (§6, §7, §10) y la falta de voz (§28, "Cuándo no actuar"). Por eso la skill pide alternar el largo de las oraciones y conservar las metáforas y opiniones del autor.

### AuTexTification, IberLEF 2023

"Overview of AuTexTification at IberLEF 2023: Detection and Attribution of Machine-Generated Text in Multiple Domains". *Procesamiento del Lenguaje Natural*, 71, pp. 275-288 ([arXiv 2309.11285](https://ar5iv.labs.arxiv.org/html/2309.11285), [CEUR](https://ceur-ws.org/Vol-3496/overview.pdf)).

- Competencia de detección automática con más de 160.000 textos en inglés y español, en cinco dominios: tuits, reseñas, noticias, textos legales y guías prácticas.
- 36 equipos y 175 envíos.

Qué tomamos: es el corpus público más grande de texto de IA en español. Sirve para validar las listas de esta skill con frecuencias reales (ver "Cómo seguir").

### Otros estudios útiles

- **Muñoz-Ortiz, Gómez-Rodríguez y Vilares (2024), Universidade da Coruña.** Noticias en inglés de seis modelos frente a humanas: los textos humanos varían más el largo de las oraciones y el vocabulario ([PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11422446/)). En inglés, pero de un grupo hispano y coherente con los estudios en español.
- **"It's the same but not the same: Do LLMs distinguish Spanish varieties?"** ([arXiv 2504.20049](https://arxiv.org/pdf/2504.20049)). Evalúa si los modelos distinguen variedades del español. Es la base para el §28; falta leer los resultados completos para citar cifras.
- **Estudio de *Caracterización de los textos generados por ChatGPT*** ([Reencuentro, UAM](https://reencuentro.xoc.uam.mx/index.php/reencuentro/article/download/1243/1129/1959)). Análisis temático: los textos simulan respuestas humanas pero les falta contexto y juicio crítico.

## Listas de frases en español

No hay un estudio académico de frecuencia de palabras de IA en español comparable a los de "delve" en inglés. Las listas disponibles vienen de empresas de detección y de la prensa:

- **Pangram Labs** publica frases de IA en español ([frases más comunes](https://www.pangram.com/es/resources/most-common-ai-phrases), [guía de patrones](https://www.pangram.com/es/blog/comprehensive-guide-to-spotting-ai-writing-patterns)): "profundicemos", "en el vertiginoso mundo actual", "es fundamental destacar que", "explorar el mosaico de", "un intrincado entramado", "es una excelente pregunta", "crucial", "matices", "paisaje".
- **El Economista** recoge una lista de palabras repetidas por la IA en español, de "crucial" a "esencial" ([artículo](https://www.eleconomista.es/tecnologia/noticias/12925132/07/24/de-crucial-a-esencial-estas-son-las-palabras-que-revelan-que-un-texto-esta-escrito-con-ia.html)).
- **Prensa sobre estudios en inglés** con equivalentes en español, como "meticuloso" y "encomiable" ([La Nación](https://www.lanacion.com.ar/tecnologia/el-exceso-de-palabras-como-encomiable-y-meticuloso-sugiere-el-uso-de-chatgpt-en-miles-de-estudios-nid27042024/), [Xataka](https://www.xataka.com/robotica-e-ia/chatgpt-esta-escribiendo-estudios-medicos-economicos-sabemos-porque-usa-palabras-rarunas)).

Estas listas no publican su método, así que el §12 las trata como señales que pesan en grupo, nunca solas.

## Calibración con informes reales

En 1.1.0 medí el detector con 9 informes de un curso de negocios. El resultado completo está en [calibracion.md](calibracion.md). Lo que cambia el respaldo de los patrones:

- **§25** suma "el presente informe analiza, documenta, expone...", 8 veces en 7 informes.
- **§15** suma "asegurando", "manteniendo" y "priorizando", que aparecen en 4 a 5 informes.
- **§12 y §14** tienen una excepción para el lenguaje de negocios: "optimizar el uso de la planta", "factores clave de éxito" y "costos asociados a la operación" no son señal.
- **§19** ya estaba en la skill, pero el detector no lo buscaba. Ahora lo hace.

Es un solo curso y un solo semestre, así que sirve para ajustar el detector, no para fijar umbrales.

## Normas del español usadas

Algunas señales no necesitan estudio porque contradicen la norma: la IA calca el inglés y la norma dice otra cosa.

- **Mayúsculas en títulos (§20) y en meses y días (§21).** La RAE pide mayúscula solo en la primera palabra del título y en nombres propios; meses y días van con minúscula.
- **Gerundio de posterioridad (§15).** La RAE considera incorrecto el gerundio que expresa una acción posterior a la del verbo principal ("se fundó en 2010, convirtiéndose en líder").
- **Raya (§8).** En español la raya es correcta para incisos y diálogos, con raya de apertura y de cierre pegadas al inciso. Por eso aquí la raya no se prohíbe por sí misma, como en la skill inglesa; la señal es su uso a la inglesa.
- **Signos de apertura y coma antes de "y" (§21).** El español exige ¿ y ¡, y en general no pone coma antes de la "y" final de una enumeración.
- **Pasiva perifrástica (§11).** Las gramáticas de estilo recomiendan la activa o la pasiva refleja; la pasiva con "ser" y agente es típica de las traducciones.
- **Calcos (§27).** "En base a", "jugar un rol", "hacer sentido", "tomar lugar" y los falsos amigos ("eventualmente", "asumir", "remover") son anglicismos que la FundéuRAE ha tratado en sus recomendaciones.

## Respaldo de cada patrón

| Respaldo | Patrones | Qué significa |
|----------|----------|---------------|
| Wikipedia, estructural | 1-7, 9, 13, 14, 17, 22-26 | Viene de la guía en inglés; la forma se repite en español con otras palabras |
| Estudio en español | 6, 7, 8, 10, 11, 15, 21, 28 | Coincide con diferencias medidas en corpus en español (sintaxis, puntuación, uniformidad, falta de voz) |
| Norma RAE o FundéuRAE | 8, 11, 15, 20, 21, 27 | La forma de IA contradice la norma o el uso recomendado |
| Listas de frases | 4, 10, 12, 16, 18, 22 | Listas de detectores y prensa, sin método publicado |
| Informes reales (1.1.0) | 12, 14, 15, 19, 25 | Frecuencias medidas en 9 informes de un curso; ver [calibracion.md](calibracion.md) |

## Modo presentación (1.2.0)

El modo presentación no agrega patrones; ajusta dónde se aplican. Las viñetas y las frases sin verbo son el formato normal de una lámina, así que ahí no cuentan como señal. La regla de títulos que dicen la conclusión viene de la práctica de consultoría (títulos de acción o "action titles"), no de un estudio sobre IA: un título-tema como "Análisis de clientes" es la elección por defecto que sirve para cualquier lámina. Falta calibrarlo con presentaciones reales, como se hizo con los informes.

## Diferencias con la skill en inglés

| Inglés (humanizer 3.1.0) | Español (humanizar 1.1.0) | Motivo |
|--------------------------|---------------------------|--------|
| §6 Forced triads | §6 Tríadas y pares forzados | En español abundan también los pares de adjetivos sinónimos ("claro y conciso") |
| §8 Prohibición de rayas | §8 Rayas a la inglesa | La raya de inciso es norma en español |
| §10 Hyphenated pairs | Eliminado | No aplica: el español no forma adjetivos compuestos con guion así |
| (no existe) | §10 Conectores de plantilla | "Cabe destacar", "Asimismo", "En conclusión" en cada párrafo |
| §11 Passive voice | §11 Pasiva perifrástica | En español es además un calco |
| §15 Shallow -ing riders | §15 Gerundios colgados | El equivalente español es más grave: suele ser un error normativo |
| §20 Title case | §20 Títulos decorativos | En español la mayúscula en cada palabra es un error, no solo un estilo |
| §21 Curly quotes | §21 Ortotipografía a la inglesa | Las comillas no son señal en español; sí la coma de Oxford y la falta de ¿ |
| (no existe) | §27 Calcos del inglés | Nueva sección G |
| (no existe) | §28 Español neutro sin lugar | Nueva sección G |

## Cómo seguir

1. **Leer el PDF de Alonso Simón et al.** y ajustar §8, §10, §11 y §21 a sus 17 variables.
2. **Medir frecuencias.** Con el corpus de AuTexTification (parte en español), contar cuántas veces aparece cada palabra y frase del §12 por cada mil palabras en textos humanos y de IA. Mantener solo las que aparezcan claramente más en IA. El script `scripts/marcar.py` sirve de base para ese conteo.
3. **Probar con textos propios.** La primera prueba, con informes, está en [calibracion.md](calibracion.md). Falta hacerla con correos y publicaciones de LinkedIn, y revisar a ciegas si el resultado suena mejor.
4. **Actualizar las listas por modelo.** Las palabras de moda cambian con cada versión; las de 2023 ("crucial", "profundizar") pueden no ser las de 2026.
