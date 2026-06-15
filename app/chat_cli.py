"""Runner local de la entrevista (MVP, sin Teams).

Abre una conversación con el agente de Foundry y ejecuta en local las
function tools cuando el agente las invoca. Permite probar el flujo
completo (Fases 0-4) desde la terminal antes de conectar el bot de Teams.

Uso:
  python -m app.chat_cli            # nueva sesión
  python -m app.chat_cli <conv_id>  # retomar una sesión pausada

Comandos dentro del chat:
  /salir   termina (imprime el id de conversación para poder retomar)
"""

import json
import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools import ejecutar_tool  # noqa: E402


def _crear_clientes():
    project = AIProjectClient(
        endpoint=os.environ["PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    return project, project.get_openai_client()


def _turno(openai, agent_name: str, conversation_id: str, entrada) -> str:
    """Envía `entrada` al agente y resuelve function_calls hasta obtener texto."""
    agente = {"agent_reference": {"name": agent_name, "type": "agent_reference"}}
    response = openai.responses.create(
        conversation=conversation_id, input=entrada, extra_body=agente
    )

    while True:
        salidas_tool = []
        for item in response.output:
            if item.type == "function_call":
                print(f"  [tool] {item.name}({item.arguments[:120]}…)")
                resultado = ejecutar_tool(item.name, item.arguments)
                salidas_tool.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": resultado,
                    }
                )
        if not salidas_tool:
            return response.output_text
        response = openai.responses.create(
            conversation=conversation_id, input=salidas_tool, extra_body=agente
        )


def main() -> None:
    agent_name = os.environ.get("AGENT_NAME", "asistente-historias-usuario")
    _, openai = _crear_clientes()

    if len(sys.argv) > 1:
        conversation_id = sys.argv[1]
        print(f"Retomando sesión {conversation_id}")
    else:
        conversation_id = openai.conversations.create().id
        print(f"Nueva sesión: {conversation_id}")
        print(
            _turno(
                openai,
                agent_name,
                conversation_id,
                "Hola, quiero redactar una historia de usuario. Empieza la sesión: "
                "recupera la plantilla y los ejemplos y pídeme el título.",
            )
        )

    while True:
        try:
            texto = input("\ntú> ").strip()
        except (EOFError, KeyboardInterrupt):
            texto = "/salir"
        if texto == "/salir":
            print(f"\nSesión pausada. Retómala con: python -m app.chat_cli {conversation_id}")
            break
        if not texto:
            continue
        print("\nagente> " + _turno(openai, agent_name, conversation_id, texto))


if __name__ == "__main__":
    main()
