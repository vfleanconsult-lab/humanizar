#!/usr/bin/env python3
"""Marca señales de escritura de IA en un texto en español.

Uso:
    python3 scripts/marcar.py archivo.txt
    pbpaste | python3 scripts/marcar.py

Solo busca las señales que se pueden detectar con palabras y puntuación.
Las de estructura (§2, §5, §26 y otras) necesitan la skill completa.
Una marca no prueba que el texto sea de IA: lo que pesa es la densidad.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Cada patrón: (número en SKILL.md, nombre, expresión regular).
# Las expresiones ignoran mayúsculas salvo donde la mayúscula es la señal.
I = re.IGNORECASE

PATRONES: list[tuple[int, str, re.Pattern[str]]] = [
    (1, "No es X, es Y", re.compile(
        r"\bno (?:es|son|se trata de)(?: solo| solamente| simplemente| únicamente)? [^.;:\n]{1,60}?[,;] (?:es|son|sino)\b"
        r"|\bno solo [^.;\n]{1,60}?,? sino(?: también)?\b"
        r"|\bmás que (?:un|una) [^.;\n]{1,40}?, (?:es|son)\b"
        r"|\blejos de ser\b", I)),
    (3, "Frases que suenan profundas", re.compile(
        r"\b(?:la verdadera pregunta es|en el fondo|en esencia|lo que realmente importa"
        r"|el corazón del asunto|la clave está en|es el ADN de|es el lenguaje de)\b", I)),
    (4, "Preámbulo", re.compile(
        r"\b(?:profundicemos|exploremos|sumerjámonos|vamos a desglosar|te lo explico"
        r"|esto es lo que necesitas saber|sin más preámbulos|seamos honestos|siendo sincer[oa])\b"
        r"|¿la verdad\?", I)),
    (5, "Discutir con nadie", re.compile(
        r"\b(?:no digo que|que quede claro|no me malinterpreten|no me malinterpretes"
        r"|podría pensarse que|sería tentador|uno podría caer en la tentación)\b", I)),
    (8, "Rayas como conector", re.compile(r" [—–] | - |\w—\w|\w – \w")),
    (9, "Calificadores apilados", re.compile(
        r"\b(?:podría eventualmente|quizás podría|en cierta medida|hasta cierto punto|de alguna manera)\b", I)),
    (10, "Conectores de plantilla", re.compile(
        r"(?:^|\n|\. )(?:Además|Asimismo|Por otro lado|Por otra parte|Cabe (?:destacar|señalar|mencionar)"
        r"|Es (?:importante|fundamental|crucial) (?:destacar|señalar|mencionar)|Vale la pena mencionar"
        r"|En este sentido|En este contexto|En definitiva|En resumen|En conclusión|En última instancia"
        r"|Para concluir)\b")),
    (11, "Pasiva perifrástica", re.compile(
        r"\b(?:fue|fueron|ha sido|han sido|será|serán) \w+(?:ado|ada|ados|adas|ido|ida|idos|idas) por\b", I)),
    (12, "Palabras sobreusadas", re.compile(
        r"\b(?:crucial(?:es)?|fundamental(?:es)?|esencial(?:es)?|vital(?:es)?|profundizar|adentrarse|sumergirse"
        r"|panorama|ecosistema|entramado|tapiz|mosaico|intrincad[oa]s?|matices|meticulos[oa]s?|meticulosamente"
        r"|robust[oa]s?|integral(?:es)?|holístic[oa]s?|sinergias?|innovador(?:a|es|as)?|disruptiv[oa]s?"
        r"|transformador(?:a|es|as)?|vibrantes?|fascinantes?|potenciar|optimizar|fomentar|empoderar"
        r"|aprovechar al máximo|desbloquear|navegar|testimonio|en constante evolución|vertiginoso)\b", I)),
    (13, "Importancia inflada", re.compile(
        r"\b(?:marcando un hito|marcó un hito|un antes y un después|sentó las bases|sentando las bases"
        r"|huella imborrable|legado perdurable|papel fundamental|rol fundamental|en un mundo cada vez más"
        r"|en la era digital|en los tiempos que corren|el futuro se ve prometedor|tiempos emocionantes"
        r"|un paso en la dirección correcta)\b", I)),
    (14, "Relación vaga", re.compile(
        r"\b(?:asociad[oa]s? a|vinculad[oa]s? (?:a|con)|ligad[oa]s? a|en el marco de|de la mano de)\b", I)),
    (15, "Gerundio colgado", re.compile(
        r", (?:\w+ndo(?:se|la|lo|las|los)?|convirtiéndose|consolidándose|posicionándose)\b(?! que)", I)),
    (16, "Lenguaje publicitario", re.compile(
        r"\b(?:enclavad[oa]|en el corazón de|rica herencia|rico patrimonio|belleza natural|de ensueño"
        r"|imperdible|joya escondida|experiencia única|compromiso con la excelencia|de clase mundial"
        r"|de vanguardia)\b", I)),
    (17, "Autoridad prestada", re.compile(
        r"\b(?:los expertos (?:coinciden|advierten|señalan|afirman)|los especialistas (?:coinciden|advierten)"
        r"|diversos estudios|numerosas investigaciones|numerosos estudios|según analistas)\b", I)),
    (18, "Evitar ser y tener", re.compile(
        r"\b(?:se erige como|se posiciona como|se consolida como|funge como|cuenta con|ostenta|alberga)\b", I)),
    (20, "Mayúscula en cada palabra del título", re.compile(
        r"(?m)^#{1,6} (?:\S+ )*?[A-ZÁÉÍÓÚÑ]\w+ (?:[A-ZÁÉÍÓÚÑ]\w+ ){2,}")),
    (21, "Ortotipografía a la inglesa", re.compile(
        r"(?<![¿\w])\b[A-ZÁÉÍÓÚÑ][^¿?.!\n]{2,80}\?"
        r"|\b(?:Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo) \d"
        r"|\bde (?:Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre)\b"
        r"|, y \w+[.\n]")),
    (22, "Restos del chatbot", re.compile(
        r"¡(?:Claro|Por supuesto|Excelente pregunta|Qué buena pregunta)!|\b(?:Espero que (?:esto )?te sea útil"
        r"|Espero haberte ayudado|No dudes en|¿Quieres que|¿Te gustaría que|A continuación te presento"
        r"|Aquí tienes)\b", I)),
    (23, "Límite de conocimiento", re.compile(
        r"\b(?:mi última actualización|según la información disponible|no (?:se encuentra|está) ampliamente documentad"
        r"|en las fuentes proporcionadas|mantiene un perfil bajo|se cree que)", I)),
    (27, "Calcos del inglés", re.compile(
        r"\b(?:juega(?:n)? un rol|jugar un rol|tomar lugar|tomó lugar|hace sentido|hacer sentido|en base a"
        r"|a nivel de|en orden a|eventualmente)\b", I)),
]


def marcar(texto: str) -> list[tuple[int, str, list[str]]]:
    resultados = []
    for numero, nombre, patron in PATRONES:
        hallazgos = [m.group(0).strip() for m in patron.finditer(texto)]
        if hallazgos:
            resultados.append((numero, nombre, hallazgos))
    return resultados


def main() -> None:
    if len(sys.argv) > 1:
        texto = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        texto = sys.stdin.read()
    palabras = max(len(texto.split()), 1)
    resultados = marcar(texto)
    total = sum(len(h) for _, _, h in resultados)

    if not resultados:
        print(f"Sin señales detectables en {palabras} palabras.")
        return
    for numero, nombre, hallazgos in resultados:
        ejemplos = "; ".join(dict.fromkeys(hallazgos))[:160]
        print(f"§{numero:<3} {nombre} ({len(hallazgos)}): {ejemplos}")
    densidad = total / palabras * 100
    print(f"\n{total} señales en {palabras} palabras: {densidad:.1f} por cada 100 palabras.")
    print("El umbral no está calibrado: compara con textos tuyos del mismo tipo.")


if __name__ == "__main__":
    main()
