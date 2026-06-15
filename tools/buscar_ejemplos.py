"""Tool buscar_ejemplos: devuelve la plantilla y las historias de ejemplo.

MVP: lee los ficheros Markdown de `knowledge/`. En producción puede
sustituirse por un índice de Azure AI Search / File Search sin cambiar
el contrato de la tool.
"""

from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
PLANTILLA = "plantilla_historia_usuario.md"


def buscar_ejemplos(consulta: str = "") -> dict:
    if not KNOWLEDGE_DIR.is_dir():
        return {"error": f"No existe la carpeta de conocimiento: {KNOWLEDGE_DIR}"}

    plantilla = ""
    ejemplos = []
    for fichero in sorted(KNOWLEDGE_DIR.glob("*.md")):
        texto = fichero.read_text(encoding="utf-8")
        if fichero.name == PLANTILLA:
            plantilla = texto
            continue
        if consulta and consulta.lower() not in texto.lower():
            continue
        ejemplos.append({"nombre": fichero.stem, "contenido": texto})

    # Limitar tamaño: la plantilla completa + como mucho dos ejemplos.
    return {
        "plantilla": plantilla,
        "ejemplos": ejemplos[:2],
        "total_ejemplos_disponibles": len(ejemplos),
    }
