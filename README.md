# Humanizar

Humanizar reescribe textos en español generados por IA para que suenen a la persona que los firma, sin cambiar lo que dicen. Es una adaptación al español de [humanizer](https://github.com/blader/humanizer), que se basa en la guía ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) de Wikipedia. Funciona en Claude Code, Claude.ai, Codex y cualquier agente que use skills.

**Antes:**
> ¡Excelente pregunta! En el vertiginoso mundo actual, la gestión financiera no es solo una tarea administrativa, es un motor estratégico. Cabe destacar que la empresa se fundó en 2010, convirtiéndose en líder del sector y reflejando el compromiso de sus socios. Asimismo, el área de finanzas juega un rol crucial en base a los datos. En conclusión, el futuro se ve prometedor.

**Después:**
> La empresa se fundó en 2010 y hoy lidera su sector. Finanzas toma sus decisiones con los datos.

Humanizar edita para lectores humanos. Engañar a los detectores de IA no es el objetivo.

## ¿Sirven en español las señales de Wikipedia?

En la estructura sí; en el vocabulario y la puntuación, no. Los contrastes "no es X, es Y", los remates, las tríadas o la importancia inflada salen de cómo genera texto un modelo, así que aparecen igual en español. Pero las palabras típicas son otras, la raya es correcta en español y hay señales propias que la guía inglesa no cubre: gerundios colgados, mayúscula en cada palabra de los títulos, calcos del inglés y un español neutro que no es de ningún país.

No existe una versión en español de la guía de Wikipedia. Esta skill combina la guía inglesa con estudios de corpus en español (Alonso Simón et al., 2024, UCM; Petrenko et al.; AuTexTification, IberLEF 2023), listas de frases de IA en español y las normas de la RAE y la FundéuRAE. El detalle, con fuentes y el respaldo de cada patrón, está en [docs/investigacion.md](docs/investigacion.md).

## Las cinco señales más fuertes

1. **No es X, es Y:** "No es solo una herramienta, es una revolución."
2. **Remates de una línea:** "Y eso lo cambia todo."
3. **Frases que suenan profundas:** "En el fondo, lo que realmente importa es..."
4. **Preámbulos:** "Profundicemos." "¿La verdad?"
5. **Discutir con nadie:** "Que quede claro: no digo que X, pero..."

Y dos muy propias del español: **gerundios colgados** ("se fundó en 2010, convirtiéndose en líder") y **conectores de plantilla** ("Cabe destacar", "Asimismo", "En conclusión" en cada párrafo).

## Instalación

### Claude Code

```text
/plugin marketplace add vfleanconsult-lab/humanizar
/plugin install humanizar@humanizar
```

O con la herramienta de skills:

```bash
npx skills add vfleanconsult-lab/humanizar --global --agent claude-code
```

### Claude.ai y Claude Desktop

Descarga este repositorio como ZIP (**Code → Download ZIP**) y súbelo como skill en Configuración → Capacidades.

### Codex y otros agentes

```bash
npx skills add vfleanconsult-lab/humanizar --global --agent '*'
```

Sin `--global` se instala solo en el proyecto actual. Para un agente que la herramienta no conozca, copia `SKILL.md` a su carpeta de skills.

## Uso

```
/humanizar

[pega tu texto aquí]
```

O en lenguaje normal:

```
Humaniza este texto: [tu texto]
```

Para un archivo:

```
Humaniza la prosa de docs/propuesta.md
```

### Que suene a ti

Incluye una muestra de tu escritura:

```
/humanizar

Esta es una muestra de cómo escribo:
[2 o 3 párrafos tuyos]

Ahora humaniza este texto:
[texto de IA]
```

Humanizar imita el ritmo, el vocabulario, la puntuación y la variedad del español de la muestra (chilena, mexicana, rioplatense, peninsular u otra), incluidas las rayas si las usas.

## Detector rápido

`scripts/marcar.py` marca las señales que se pueden encontrar con palabras y puntuación. No reemplaza la skill: las señales de estructura necesitan leer el texto completo.

```bash
python3 scripts/marcar.py mi-texto.txt
```

```
§1   No es X, es Y (1): no es solo una tarea administrativa, es
§10  Conectores de plantilla (3): Cabe destacar; . Asimismo; En conclusión
§12  Palabras sobreusadas (5): vertiginoso; crucial; integral; holístico; fundamental
§15  Gerundio colgado (1): , convirtiéndose
...
23 señales en 105 palabras: 21.9 por cada 100 palabras.
```

## Cómo funciona

Un modelo de lenguaje escribe lo más probable a continuación, así que elige lo que sirve para la mayor cantidad de lectores y temas. Una persona escribe para un lector y un tema. Cada señal es una forma de esa elección por defecto: una oración que anuncia importancia en vez de dar un dato, ritmo o formato aplicado por regla, un hecho común presentado como hito, restos del chat, o un español calcado del inglés.

Humanizar marca cada señal, de la más fuerte a la más débil, escribe un borrador sin tratar la estructura original como fija, lo revisa contra los patrones y contra los datos originales, y entrega la versión final. No inventa: un nombre, cifra, fecha, cita o fuente tiene que venir del texto o del autor. Si falta un dato, pregunta.

## Los 28 patrones

Los patrones van del más fuerte y frecuente al más débil. Del 1 al 5 basta una aparición para editar. Los marcados *débil sola* cuentan solo cuando hay otras señales en el mismo pasaje.

### A. Escenificar en vez de afirmar

| # | Patrón | Antes | Después |
|---|--------|-------|---------|
| 1 | **No es X, es Y** | "No es solo una herramienta, es una revolución"; "no se trata de X, sino de Y" | Decir la idea directamente |
| 2 | **Remates de una línea y fragmentos dramáticos** | "Y eso lo cambia todo."; "Sin excusas. Sin atajos." | Cortar el remate; unir los fragmentos en una afirmación concreta |
| 3 | **Frases que suenan profundas** | "En el fondo, lo que realmente importa es..." | Reemplazar el dicho por la afirmación concreta |
| 4 | **Preámbulo antes de la idea** | "Profundicemos", "¿La verdad? Depende" | Quitar el preámbulo y decir la idea |
| 5 | **Discutir con nadie** | "Que quede claro: no digo que...", "Sería tentador..." | Quitar la objeción inventada |

### B. Ritmo por regla

| # | Patrón | Antes | Después |
|---|--------|-------|---------|
| 6 | **Tríadas y pares forzados** | "aprendizaje, inspiración y crecimiento"; "claro y conciso" | Usar los elementos que el sentido necesita |
| 7 | **Inicios repetidos** | "La empresa... La empresa... La empresa..." | Unir oraciones u omitir el sujeto |
| 8 | **Rayas como conector universal** (*débil sola*) | "La política — anunciada sin aviso — afecta..." | Comas, puntos o paréntesis; raya solo según norma o muestra |
| 9 | **Calificadores apilados** (*débil sola*) | "podría eventualmente, en cierta medida..." | Dejar solo los que respalda la fuente |
| 10 | **Conectores de plantilla** | "Cabe destacar... Asimismo... En conclusión..." | Quitar o usar el conector que dice la relación real |
| 11 | **Pasiva perifrástica y sujetos ausentes** (*débil sola*) | "fue aprobado por el directorio" | "el directorio aprobó" |

### C. Inflar y pedir autoridad prestada

| # | Patrón | Antes | Después |
|---|--------|-------|---------|
| 12 | **Palabras sobreusadas por la IA** | "crucial... panorama... potenciar... sinergia" | Palabras simples |
| 13 | **Importancia inflada** | "marcando un hito", "en el vertiginoso mundo actual", "el futuro se ve prometedor" | Conservar el hecho; terminar en el último dato |
| 14 | **Relación vaga** | "vinculado a", "en el marco de" | Decir la relación que da la fuente |
| 15 | **Gerundios colgados** | "se fundó en 2010, convirtiéndose en líder" | Oración con verbo conjugado |
| 16 | **Lenguaje publicitario** | "enclavada en el corazón de", "joya escondida" | Decir qué es |
| 17 | **Autoridad prestada** | "Los expertos coinciden", "diversos estudios demuestran" | Nombrar la fuente o quitar la afirmación |
| 18 | **Evitar ser, estar y tener** | "se erige como... cuenta con... alberga" | "es... tiene" |

### D. Formato por regla

| # | Patrón | Antes | Después |
|---|--------|-------|---------|
| 19 | **Negritas decorativas** | "**Rentabilidad:** La rentabilidad mejoró" | Quitar la negrita; pasar la lista a prosa |
| 20 | **Títulos decorativos** | "🚀 Estrategias Clave Para El Crecimiento" | Mayúscula solo inicial; sin emojis |
| 21 | **Ortotipografía a la inglesa** (*débil sola*) | "Qué opinas?", "el Lunes 3 de Marzo", "ventas, costos, y gastos" | "¿Qué opinas?", "el lunes 3 de marzo", "ventas, costos y gastos" |

### E. Restos del chat y del borrador

| # | Patrón | Antes | Después |
|---|--------|-------|---------|
| 22 | **Restos del chatbot** | "¡Excelente pregunta! ... Espero que te sea útil." | Quitar el envoltorio |
| 23 | **Avisos de límite de conocimiento y suposiciones** | "Si bien no hay información documentada, probablemente..." | Decir lo que la fuente muestra o quitar |
| 24 | **Título repetido en la primera oración** | "## Flujo de caja" + "El flujo de caja es importante." | Dejar que el título haga su trabajo |
| 25 | **Escribir sobre el documento en vez del tema** | "Este informe se organiza en tres secciones" | Hablar del tema |

### F. Escribir para el lector equivocado

| # | Patrón | Antes | Después |
|---|--------|-------|---------|
| 26 | **Volver a explicar lo que el lector sabe** | Una respuesta que repite el diagnóstico antes de decir qué hacer | Empezar por la decisión |

### G. Español de traducción

| # | Patrón | Antes | Después |
|---|--------|-------|---------|
| 27 | **Calcos del inglés** | "juega un rol", "en base a", "hace sentido", "eventualmente" (por "al final") | La forma propia del español |
| 28 | **Español neutro sin lugar** (*débil sola*) | "vosotros" y "ordenador" en un texto para Chile; tú y usted mezclados | La variedad del escritor, consistente |

## Fuentes

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) y [humanizer](https://github.com/blader/humanizer) de Siqi Chen, base de las secciones A a F.
- Alonso Simón, Fernández-Pampillón, Fernández Trinidad y Márquez Cruz (2024). [¿Tienen GPT-3.5 y GPT-4 un estilo de escritura diferente del estilo humano? Un estudio exploratorio para el español](https://matrix.aesla.org.es/RAEL/article/view/666). RAEL 23(1).
- Petrenko et al. [Análisis comparativo de las características lingüísticas y estilísticas de textos mediáticos humanos y generados artificialmente](https://dialnet.unirioja.es/servlet/articulo?codigo=10651021).
- [Overview of AuTexTification at IberLEF 2023](https://ar5iv.labs.arxiv.org/html/2309.11285). Procesamiento del Lenguaje Natural 71.
- [Pangram Labs: frases más comunes de la IA en español](https://www.pangram.com/es/resources/most-common-ai-phrases).

La lista completa y el respaldo de cada patrón están en [docs/investigacion.md](docs/investigacion.md).

## Historial

Ver [CHANGELOG.md](CHANGELOG.md).

## Licencia

MIT. Basado en humanizer, © 2025 Siqi Chen, también MIT.
