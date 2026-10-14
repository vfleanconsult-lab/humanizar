#!/usr/bin/env python3
"""Marca señales de escritura de IA en un texto en español.

Uso:
    python3 scripts/marcar.py archivo.txt
    python3 scripts/marcar.py presentacion.pptx
    pbpaste | python3 scripts/marcar.py

Solo busca las señales que se pueden detectar con palabras y puntuación.
Las de estructura (§2, §6, §26 y otras) necesitan la skill completa.
Una marca no prueba que el texto sea de IA: lo que pesa es la densidad.
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree

# Cada patrón: (número en SKILL.md, nombre, expresión regular[, descartar]).
# "descartar(texto, marca)" devuelve True cuando la marca es un falso positivo conocido.
# Las expresiones ignoran mayúsculas salvo donde la mayúscula es la señal.
I = re.IGNORECASE

# Sustantivos de negocio donde "asociado a" nombra una relación clara.
NEGOCIO = re.compile(
    r"(?:costos?|gastos?|riesgos?|cargos?|recargos?|pagos?|multas?|fletes?|trámites?"
    r"|permisos?|ingresos?|impuestos?|operaci\w+)\W+(?:\w+\W+){0,5}$", I)


def tras_negocio(texto: str, marca: re.Match[str]) -> bool:
    return bool(NEGOCIO.search(texto[max(0, marca.start() - 40):marca.start()]))


def en_titulo(texto: str, marca: re.Match[str]) -> bool:
    """Los títulos y las líneas en negrita usan la raya como separador, no como conector."""
    inicio = texto.rfind("\n", 0, marca.start()) + 1
    fin = texto.find("\n", marca.end())
    linea = texto[inicio:fin if fin != -1 else len(texto)].strip()
    return linea.startswith(("#", "**", "[")) or linea.isupper()


def pregunta_con_apertura(texto: str, marca: re.Match[str]) -> bool:
    if not marca.group(0).endswith("?"):
        return False
    inicio = texto.rfind("\n", 0, marca.start()) + 1
    return "¿" in texto[inicio:marca.start()]

# Palabras que una persona usa sin problema; son señal solo si se juntan.
# {nombre del patrón: marcas mínimas en un mismo párrafo}
MINIMO_POR_PARRAFO = {
    "Rayas como conector (guion o semiraya)": 2,
    "Calificadores apilados": 2,
    "Palabras sobreusadas": 3,
}

# Gerundios de uso corriente en textos formales; no cuentan como colgados.
GERUNDIO_CORRIENTE = re.compile(
    r"^, (?:incluyendo|dependiendo|hablando|siendo|teniendo|habiendo|considerando|suponiendo"
    r"|estando|tratando|entendiendo|pensando)\b", I)


def gerundio_corriente(texto: str, marca: re.Match[str]) -> bool:
    return bool(GERUNDIO_CORRIENTE.match(marca.group(0)))

# Líneas de índice automático de Word: "[1. Introducción 3](#_Toc123)".
INDICE = re.compile(r"^.*\]\(#[^)]*\).*$", re.M)

PATRONES: list[tuple] = [
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
    (8, "Rayas como conector", re.compile(r" — |\w—\w"), en_titulo),
    (8, "Rayas como conector (guion o semiraya)", re.compile(
        r"(?<=[a-záéíóúñ,;)]) [–-] (?=[a-záéíóúñ¿¡(])"
        r"| [–-][a-záéíóúñ][^-–\n]{2,60}[a-záéíóúñ][–-] "), en_titulo),
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
        r"\b(?:asociad[oa]s? a|vinculad[oa]s? (?:a|con)|ligad[oa]s? a|de la mano de"
        r"|en el marco (?:de|del)(?! (?:la |el )?(?:asignatura|evaluaci|ramo|taller|curso|simula"
        r"|actividad|módulo|unidad|programa)))\b", I), tras_negocio),
    (15, "Gerundio colgado", re.compile(
        r", (?!cuando\b)(?:\w+(?:ando|iendo|yendo)(?:se|la|lo|las|los)?|convirtiéndose|consolidándose|posicionándose)\b(?! que)", I), gerundio_corriente),
    (16, "Lenguaje publicitario", re.compile(
        r"\b(?:enclavad[oa]|en el corazón de|rica herencia|rico patrimonio|belleza natural|de ensueño"
        r"|joya escondida|experiencia única|compromiso con la excelencia|de clase mundial"
        r"|de vanguardia)\b", I)),
    (17, "Autoridad prestada", re.compile(
        r"\b(?:los expertos (?:coinciden|advierten|señalan|afirman)|los especialistas (?:coinciden|advierten)"
        r"|diversos estudios|numerosas investigaciones|numerosos estudios|según analistas)\b", I)),
    (18, "Evitar ser y tener", re.compile(
        r"\b(?:se erige como|se posiciona como|se consolida como|funge como|ostenta|alberga)\b", I)),
    (19, "Negritas decorativas", re.compile(
        r"(?m)^[ \t]*(?:[-*•][ \t]+)?\*\*[^*\n]{2,70}:\*\*[ \t]+(?:\S+[ \t]+){5,}\S+")),
    (20, "Mayúscula en cada palabra del título", re.compile(
        r"(?m)^#{1,6} (?:[^\w\s#]+ )?(?:\d+(?:\.\d+)*\.? )?[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+"
        r"(?: (?:(?:de|del|la|las|el|los|y|e|en|para|por|con|a|al|o|u) )*[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){2,}")),
    (21, "Ortotipografía a la inglesa", re.compile(
        r"(?<![¿\w])\b[A-ZÁÉÍÓÚÑ][^¿?.!\n]{2,80}\?"
        r"|\b\w+, \w+(?: \w+){0,2}, y (?:\w+ )?\w+"), pregunta_con_apertura),
    (22, "Restos del chatbot", re.compile(
        r"¡(?:Claro|Por supuesto|Excelente pregunta|Qué buena pregunta)!|\b(?:Espero que (?:esto )?te sea útil"
        r"|Espero haberte ayudado|No dudes en|¿Quieres que|¿Te gustaría que|A continuación te presento"
        r"|Aquí tienes)\b", I)),
    (23, "Límite de conocimiento", re.compile(
        r"\b(?:mi última actualización|según la información disponible|no (?:se encuentra|está) ampliamente documentad"
        r"|en las fuentes proporcionadas|mantiene un perfil bajo|se cree que)", I)),
    (25, "Escribir sobre el documento", re.compile(
        r"\b(?:el presente|este) (?:informe|documento|trabajo) (?:se (?:elabora|organiza|estructura|presenta|divide|enmarca)"
        r"|tiene (?:como )?(?:por )?(?:objetivo|el propósito)|busca|presenta|expone|analiza|documenta|evalúa|detalla|describe|aborda|da cuenta)\b"
        r"|\bla siguiente tabla\b|\bse organiza en \w+ (?:secciones|capítulos|partes)\b", I)),
    (27, "Calcos del inglés", re.compile(
        r"\b(?:juega(?:n)? un rol|jugar un rol|tomar lugar|tomó lugar|hace sentido|hacer sentido|en base a"
        r"|a nivel de|en orden a)\b|(?:^|[.!?] )Eventualmente,", I)),
]


# Presentaciones (.pptx). Un .pptx es un ZIP con un XML por lámina.
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
TITULOS = {"title", "ctrTitle"}


def _destinos(pptx: zipfile.ZipFile, parte: str) -> dict[str, str]:
    """Lee las relaciones de una parte del paquete: {id: ruta dentro del ZIP}."""
    ruta = PurePosixPath(parte)
    rels = ruta.parent / "_rels" / f"{ruta.name}.rels"
    if str(rels) not in pptx.namelist():
        return {}
    destinos = {}
    for rel in ElementTree.fromstring(pptx.read(str(rels))).findall("rel:Relationship", NS):
        destino = PurePosixPath(ruta.parent, rel.get("Target", ""))
        partes: list[str] = []
        for trozo in destino.parts:
            if trozo == "..":
                partes.pop()
            else:
                partes.append(trozo)
        destinos[rel.get("Id", "")] = "/".join(partes)
    return destinos


def _texto_de_formas(xml: bytes, solo_cuerpo: bool = False) -> str:
    """Une el texto de cada cuadro. Los títulos llevan "# " para que §20 los revise."""
    bloques = []
    for forma in ElementTree.fromstring(xml).iter(f"{{{NS['p']}}}sp"):
        marcador = forma.find(".//p:nvPr/p:ph", NS)
        tipo = marcador.get("type", "body") if marcador is not None else None
        if solo_cuerpo and tipo != "body":
            continue
        lineas = ["".join(t.text or "" for t in parrafo.iter(f"{{{NS['a']}}}t")).strip()
                  for parrafo in forma.iter(f"{{{NS['a']}}}p")]
        lineas = [linea for linea in lineas if linea]
        if not lineas:
            continue
        if tipo in TITULOS:
            lineas = ["# " + " ".join(lineas)]
        bloques.append("\n".join(lineas))
    return "\n\n".join(bloques)


def leer_pptx(ruta: Path) -> list[tuple[int, str]]:
    """Devuelve [(número de lámina, texto de la lámina y sus notas)] en el orden de la presentación."""
    with zipfile.ZipFile(ruta) as pptx:
        principal = "ppt/presentation.xml"
        destinos = _destinos(pptx, principal)
        orden = ElementTree.fromstring(pptx.read(principal)).findall("p:sldIdLst/p:sldId", NS)
        laminas = []
        for numero, lamina in enumerate(orden, start=1):
            parte = destinos[lamina.get(f"{{{NS['r']}}}id")]
            texto = _texto_de_formas(pptx.read(parte))
            notas = [d for d in _destinos(pptx, parte).values() if "notesSlide" in d]
            if notas:
                texto_notas = _texto_de_formas(pptx.read(notas[0]), solo_cuerpo=True)
                if texto_notas:
                    texto += "\n\n" + texto_notas
            laminas.append((numero, texto))
        return laminas


def normalizar(texto: str, unir_lineas: bool = True) -> str:
    """Quita índices de Word y arregla lo que deja un PDF: espacios dobles y saltos de línea dentro del párrafo.

    En una presentación cada viñeta es una línea; ahí no se unen (unir_lineas=False).
    """
    texto = INDICE.sub("", texto)
    texto = re.sub(r"[ \t]{2,}", " ", texto)
    if not unir_lineas:
        return texto
    texto = re.sub(r"(?<=[a-záéíóúñ])-\n(?=[a-záéíóúñ])", "", texto)
    return re.sub(r"(?<=\S)\n(?=[a-záéíóúñ(¿¡])", " ", texto)


def marcar(texto: str, unir_lineas: bool = True) -> list[tuple[int, str, list[str]]]:
    texto = normalizar(texto, unir_lineas)
    resultados = []
    for numero, nombre, patron, *descartar in PATRONES:
        hallazgos = []
        for m in patron.finditer(texto):
            if descartar and descartar[0](texto, m):
                continue
            hallazgos.append(m.group(0).strip())
        minimo = MINIMO_POR_PARRAFO.get(nombre)
        if minimo:
            hallazgos = [h for parrafo in re.split(r"\n\s*\n", texto)
                         if len(grupo := [m.group(0).strip() for m in patron.finditer(parrafo)]) >= minimo
                         for h in grupo]
        if hallazgos:
            resultados.append((numero, nombre, hallazgos))
    return resultados


def informar(resultados: list[tuple[int, str, list[str]]], sangria: str = "") -> None:
    for numero, nombre, hallazgos in resultados:
        ejemplos = "; ".join(dict.fromkeys(hallazgos))[:160]
        print(f"{sangria}§{numero:<3} {nombre} ({len(hallazgos)}): {ejemplos}")


def main() -> None:
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if ruta and ruta.suffix.lower() == ".pptx":
        laminas = leer_pptx(ruta)
        texto = "\n\n".join(t for _, t in laminas)
        resultados = marcar(texto, unir_lineas=False)
        for numero, texto_lamina in laminas:
            if lamina := marcar(texto_lamina, unir_lineas=False):
                print(f"Lámina {numero}")
                informar(lamina, "  ")
        if resultados:
            print("\nTotal de la presentación")
    else:
        texto = ruta.read_text(encoding="utf-8") if ruta else sys.stdin.read()
        resultados = marcar(texto)

    palabras = max(len(texto.split()), 1)
    total = sum(len(h) for _, _, h in resultados)
    if not resultados:
        print(f"Sin señales detectables en {palabras} palabras.")
        return
    informar(resultados)
    densidad = total / palabras * 100
    print(f"\n{total} señales en {palabras} palabras: {densidad:.1f} por cada 100 palabras.")
    print("Referencia de densidad en docs/calibracion.md; compara con textos tuyos del mismo tipo.")


if __name__ == "__main__":
    main()
