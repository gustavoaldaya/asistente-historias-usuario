"""Crea o actualiza el agente «Asistente de Historias de Usuario» en Azure AI Foundry.

Requiere (ver .env.example):
  PROJECT_ENDPOINT        https://<recurso>.services.ai.azure.com/api/projects/<proyecto>
  MODEL_DEPLOYMENT_NAME   nombre del despliegue de modelo (p. ej. gpt-4o)
  AGENT_NAME              nombre del agente (por defecto: asistente-historias-usuario)

Uso:
  python agent/create_agent.py
"""

import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tools_schema import TOOL_DEFINITIONS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    endpoint = os.environ["PROJECT_ENDPOINT"]
    model = os.environ["MODEL_DEPLOYMENT_NAME"]
    agent_name = os.environ.get("AGENT_NAME", "asistente-historias-usuario")

    instructions = (ROOT / "agent" / "system_prompt.md").read_text(encoding="utf-8")

    tools = [
        FunctionTool(
            name=t["name"],
            description=t["description"],
            parameters=t["parameters"],
        )
        for t in TOOL_DEFINITIONS
    ]

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
