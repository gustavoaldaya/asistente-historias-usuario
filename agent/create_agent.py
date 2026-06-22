"""Crea o actualiza el agente «Asistente de Historias de Usuario» en Azure AI Foundry.

Requiere (ver .env.example):
  PROJECT_ENDPOINT          https://<recurso>.services.ai.azure.com/api/projects/<proyecto>
  MODEL_DEPLOYMENT_NAME     nombre del despliegue de modelo (p. ej. gpt-4.1)
  AGENT_NAME                nombre del agente (por defecto: asistente-historias-usuario)

Uso:
  python agent/create_agent.py              # con OpenAPI tools (Teams-ready)
  python agent/create_agent.py --local      # con FunctionTool local (para chat_cli)
"""

import os
import sys
from pathlib import Path
from typing import Any, cast

import jsonref
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    FunctionTool,
    OpenApiFunctionDefinition,
    OpenApiAnonymousAuthDetails,
    OpenApiTool,
    PromptAgentDefinition,
)
from azure.identity import DefaultAzureCredential

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tools_schema import TOOL_DEFINITIONS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def _build_openapi_tools() -> list:
    spec_path = ROOT / "functions" / "openapi.json"
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = cast(dict[str, Any], jsonref.loads(f.read()))

    tool = OpenApiTool(
        openapi=OpenApiFunctionDefinition(
            name="user_stories_tools",
            spec=spec,
            description=(
                "Herramientas para generar historias de usuario: buscar ejemplos, "
                "validar estructura, generar y guardar documentos."
            ),
            auth=OpenApiAnonymousAuthDetails(),
        )
    )
    return [tool]


def _build_local_function_tools() -> list:
    return [
        FunctionTool(
            name=t["name"],
            description=t["description"],
            parameters=t["parameters"],
        )
        for t in TOOL_DEFINITIONS
    ]


def main() -> None:
    endpoint = os.environ["PROJECT_ENDPOINT"]
    model = os.environ["MODEL_DEPLOYMENT_NAME"]
    agent_name = os.environ.get("AGENT_NAME", "asistente-historias-usuario")
    local_mode = "--local" in sys.argv

    instructions = (ROOT / "agent" / "system_prompt.md").read_text(encoding="utf-8")

    if local_mode:
        print("Modo local: tools como FunctionTool (client-side execution)")
        tools = _build_local_function_tools()
    else:
        print("Modo OpenAPI: HTTP triggers en Azure Functions")
        tools = _build_openapi_tools()

    project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())

    agent = project.agents.create_version(
        agent_name=agent_name,
        definition=PromptAgentDefinition(
            model=model,
            instructions=instructions,
            tools=tools,
        ),
    )
    print(f"Agente publicado: {agent.name} (id: {agent.id}, versión: {agent.version})")


if __name__ == "__main__":
    main()
