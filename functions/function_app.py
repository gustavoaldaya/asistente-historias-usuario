"""Azure Functions (HTTP triggers) para las tools del agente de Historias de Usuario.

Cada tool es un endpoint POST que recibe JSON con los argumentos y devuelve
el resultado como JSON. Foundry Agent Service las invoca via OpenAPI spec.
Incluye un endpoint GET para descargar los documentos generados.
"""

import json
import logging
import os
from pathlib import Path

import azure.functions as func

from tools.buscar_ejemplos import buscar_ejemplos
from tools.validar_estructura import validar_estructura
from tools.generar_documento import generar_documento, OUTPUT_DIR
from tools.guardar_documento import guardar_documento

app = func.FunctionApp()

MENSAJE_ERROR = (
    "El agente está experimentando un problema en este momento, "
    "se comunicará con usted próximamente."
)
FUNCTION_APP_NAME = os.environ.get(
    "FUNCTION_APP_NAME", "func-userstories-agent-001"
)
BASE_URL = f"https://{FUNCTION_APP_NAME}.azurewebsites.net/api"


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
            json.dumps({"error": MENSAJE_ERROR}, ensure_ascii=False),
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
    try:
        try:
            body = req.get_json()
        except ValueError:
            body = {}
        logging.info("[generar_documento] Recibido: %s", json.dumps(body, ensure_ascii=False)[:500])

        resultado = generar_documento(**body)

        if resultado.get("docx"):
            from urllib.parse import quote
            filename = Path(resultado["docx"]).name
            resultado["url_descarga"] = f"{BASE_URL}/descargar?file={quote(filename)}"

        return func.HttpResponse(
            json.dumps(resultado, ensure_ascii=False),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as e:
        logging.error("[generar_documento] Error: %s", e, exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": MENSAJE_ERROR}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json",
        )


@app.route(route="guardar-documento", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def guardar_documento_http(req: func.HttpRequest) -> func.HttpResponse:
    return _http_tool(req, "guardar_documento", guardar_documento)


@app.route(route="descargar", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def descargar_http(req: func.HttpRequest) -> func.HttpResponse:
    try:
        filename = req.params.get("file", "")
        if not filename or ".." in filename or "/" in filename or "\\" in filename:
            return func.HttpResponse("Archivo no válido", status_code=400)

        filepath = OUTPUT_DIR / filename
        if not filepath.is_file():
            return func.HttpResponse(
                "El documento ya no está disponible. Solicite al agente que lo genere de nuevo.",
                status_code=404,
            )

        with open(filepath, "rb") as f:
            content = f.read()

        if filename.endswith(".docx"):
            mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            mimetype = "application/octet-stream"

        return func.HttpResponse(
            content,
            status_code=200,
            mimetype=mimetype,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        logging.error("[descargar] Error: %s", e, exc_info=True)
        return func.HttpResponse("Error al descargar el documento.", status_code=500)
