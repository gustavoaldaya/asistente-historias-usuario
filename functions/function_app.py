"""Azure Functions (HTTP triggers) para las tools del agente de Historias de Usuario.

Cada tool es un endpoint POST que recibe JSON con los argumentos y devuelve
el resultado como JSON. Foundry Agent Service las invoca via OpenAPI spec.
"""

import json
import logging

import azure.functions as func

from tools.buscar_ejemplos import buscar_ejemplos
from tools.validar_estructura import validar_estructura
from tools.generar_documento import generar_documento
from tools.guardar_documento import guardar_documento

app = func.FunctionApp()


def _http_tool(req: func.HttpRequest, nombre_tool: str, fn) -> func.HttpResponse:
    try:
        try:
            body = req.get_json()
        except ValueError:
            body = {}
        logging.info("[%s] Recibido: %s", nombre_tool, json.dumps(body, ensure_ascii=False)[:500])

        resultado = fn(**body)

        return func.HttpResponse(
            json.dumps(resultado, ensure_ascii=False),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as e:
        logging.error("[%s] Error: %s", nombre_tool, e, exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": f"{type(e).__name__}: {e}"}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json",
        )


@app.route(route="buscar-ejemplos", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def buscar_ejemplos_http(req: func.HttpRequest) -> func.HttpResponse:
    return _http_tool(req, "buscar_ejemplos", buscar_ejemplos)


@app.route(route="validar-estructura", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def validar_estructura_http(req: func.HttpRequest) -> func.HttpResponse:
    return _http_tool(req, "validar_estructura", validar_estructura)


@app.route(route="generar-documento", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def generar_documento_http(req: func.HttpRequest) -> func.HttpResponse:
    return _http_tool(req, "generar_documento", generar_documento)


@app.route(route="guardar-documento", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def guardar_documento_http(req: func.HttpRequest) -> func.HttpResponse:
    return _http_tool(req, "guardar_documento", guardar_documento)
