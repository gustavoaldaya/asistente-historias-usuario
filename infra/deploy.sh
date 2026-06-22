#!/usr/bin/env bash
# Despliegue de la infraestructura para el agente de Historias de Usuario.
#
# Crea: Storage Account, Function App (Consumption) y publica
# las Azure Functions (HTTP triggers) que implementan las tools del agente.
#
# Uso:
#   bash infra/deploy.sh
#
# Variables requeridas (se leen de .env o se piden):
#   RESOURCE_GROUP          (por defecto: Agentic)
#   LOCATION                (por defecto: swedencentral)
#   FUNCTION_APP_NAME       nombre único de la Function App
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

# Cargar .env si existe
if [[ -f "$ROOT/.env" ]]; then
  set -a; source "$ROOT/.env"; set +a
fi

RG="${RESOURCE_GROUP:-Agentic}"
LOC="${LOCATION:-swedencentral}"
FA="${FUNCTION_APP_NAME:?Falta FUNCTION_APP_NAME en .env}"

echo "=== 1. Function App: $FA ==="
az functionapp create \
  --name "$FA" \
  --resource-group "$RG" \
  --consumption-plan-location "$LOC" \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --os-type Linux \
  --output none

echo "=== 2. Publicar las Functions (HTTP triggers) ==="
cd "$ROOT/functions"
func azure functionapp publish "$FA" --python
cd "$ROOT"

echo ""
echo "=== Hecho ==="
echo "Function App URL: https://${FA}.azurewebsites.net/api"
echo ""
echo "Endpoints desplegados:"
echo "  POST /api/buscar-ejemplos"
echo "  POST /api/validar-estructura"
echo "  POST /api/generar-documento"
echo "  POST /api/guardar-documento"
echo ""
echo "Ahora recrea el agente con las OpenAPI tools:"
echo "  python agent/create_agent.py"
echo ""
echo "Y publica a Teams desde el portal de Foundry:"
echo "  ai.azure.com → \$AGENT_NAME → Publish → Publish to Teams"
