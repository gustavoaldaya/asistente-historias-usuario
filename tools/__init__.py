"""Implementación local de las function tools del agente.

El host (CLI o bot de Teams) usa `ejecutar_tool(nombre, argumentos)` para
despachar los `function_call` que emite el agente de Foundry.
"""

import json
from typing import Any

from .buscar_ejemplos import buscar_ejemplos
from .generar_documento import generar_documento
from .guardar_documento import guardar_documento
from .validar_estructura import validar_estructura


def crear_work_item(historia: dict, proyecto: str) -> dict:
    # Stub del MVP: la integración real con Azure DevOps se hará vía
    # azure-devops SDK o la API REST con managed identity.
    return {
        "creado": False,
        "mensaje": (
            "crear_work_item no está habilitado en el MVP. La historia queda "
            f"lista para crearse en el proyecto '{proyecto}' cuando se configure Azure DevOps."
        ),
    }


_REGISTRO = {
    "buscar_ejemplos": buscar_ejemplos,
    "validar_estructura": validar_estructura,
    "generar_documento": generar_documento,
    "guardar_documento": guardar_documento,
    "crear_work_item": crear_work_item,
}


def ejecutar_tool(nombre: str, argumentos: str | dict[str, Any]) -> str:
    """Ejecuta la tool `nombre` y devuelve el resultado serializado en JSON."""
    if isinstance(argumentos, str):
        argumentos = json.loads(argumentos) if argumentos.strip() else {}
    funcion = _REGISTRO.get(nombre)
    if funcion is None:
        return json.dumps({"error": f"Tool desconocida: {nombre}"}, ensure_ascii=False)
    try:
        resultado = funcion(**argumentos)
    except Exception as exc:  # el agente debe recibir el error, no romper el host
        return json.dumps({"error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False)
    return json.dumps(resultado, ensure_ascii=False)
