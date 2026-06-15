"""Tool validar_estructura: completitud y coherencia de los seis bloques.

Devuelve un informe con `valida` (bool), `errores` (bloqueantes) y
`avisos` (mejorables). El agente presenta este informe al usuario en la
revisión integral (Fase 3) para que decida.
"""

import re
import unicodedata

POR_CONFIRMAR = "[por confirmar]"

_STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "al",
    "a", "en", "y", "o", "u", "que", "se", "su", "sus", "con", "por", "para",
    "como", "debe", "deben", "ser", "es", "son", "está", "están", "cada", "si",
    "no", "lo", "le", "les", "este", "esta", "estos", "estas",
}


def _normalizar(texto: str) -> set[str]:
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    palabras = re.findall(r"[a-zñ0-9]{3,}", texto)
    return {p for p in palabras if p not in _STOPWORDS}


def validar_estructura(historia: dict) -> dict:
    errores: list[str] = []
    avisos: list[str] = []

    # 1. Completitud de los seis bloques
    obligatorios = {
        "identificador": "Identificador",
        "titulo": "Título",
        "usuario": "Usuario (¿Quién?)",
        "funcionalidad": "Funcionalidad (¿Qué?)",
        "objetivo": "Objetivo (¿Para qué?)",
    }
    for clave, etiqueta in obligatorios.items():
        if not str(historia.get(clave, "")).strip():
            errores.append(f"El bloque «{etiqueta}» está vacío.")

    descripcion = historia.get("descripcion") or {}
    pasos = [p for p in descripcion.get("pasos", []) if str(p).strip()]
    if not str(descripcion.get("encuadre", "")).strip():
        avisos.append("La Descripción no tiene frase de encuadre (mecanismo general).")
    if not pasos:
        errores.append("La Descripción no tiene flujo numerado de pasos.")
    elif len(pasos) < 3:
        avisos.append("El flujo tiene menos de 3 pasos; suele ser señal de detalle insuficiente.")
    if not descripcion.get("precondiciones"):
        avisos.append("No se han indicado precondiciones (estado de partida).")
    if not descripcion.get("casos_error"):
        avisos.append("No se han indicado casos de error o excepción.")
    if not str(descripcion.get("almacenamiento", "")).strip():
        avisos.append("No se indica dónde se almacena el resultado ni qué trazabilidad queda.")

    criterios = [c for c in historia.get("criterios_aceptacion", []) if str(c).strip()]
    if not criterios:
        errores.append("No hay criterios de aceptación.")

    aceptacion = historia.get("aceptacion_usuarios") or {}
    if not str(aceptacion.get("quien", "")).strip():
        errores.append("Falta el responsable de la aceptación (Quién).")
    if not str(aceptacion.get("cuando", "")).strip():
        errores.append("Falta el momento o hito de la aceptación (Cuándo).")

    # 2. Marcas pendientes de confirmar
    texto_completo = repr(historia)
    if POR_CONFIRMAR.lower() in texto_completo.lower():
        avisos.append(
            "Quedan datos marcados como «[por confirmar]»; deben resolverse o "
            "asumirse explícitamente antes del cierre."
        )

    # 3. Coherencia: cada criterio debe tener soporte en el flujo
    texto_flujo = " ".join(
        pasos
        + list(descripcion.get("validaciones", []))
        + list(descripcion.get("casos_error", []))
        + [str(descripcion.get("almacenamiento", ""))]
    )
    vocabulario_flujo = _normalizar(texto_flujo)
    for criterio in criterios:
        palabras = _normalizar(criterio)
        if palabras and not (palabras & vocabulario_flujo):
            avisos.append(
                f"El criterio «{criterio[:80]}» no parece tener soporte en ningún "
                "paso del flujo de la Descripción."
            )

    return {
        "valida": not errores,
        "errores": errores,
        "avisos": avisos,
        "resumen": (
            f"{len(errores)} errores bloqueantes, {len(avisos)} avisos. "
            + ("Lista para revisión integral." if not errores else "Corregir antes de continuar.")
        ),
    }
