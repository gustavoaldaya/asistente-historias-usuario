# Asistente de Historias de Usuario (Human-in-the-Loop)

Agente conversacional para **Azure AI Foundry** que construye historias de usuario completas
a partir de un título, mediante una entrevista guiada bloque a bloque con aprobación explícita
del usuario en cada paso. Especificación completa en [SPEC.md](SPEC.md).

## Estructura del proyecto

```
├── SPEC.md                     Especificación spec-driven del agente
├── agent/
│   ├── system_prompt.md        Instrucciones del agente (sección 6 de la spec)
│   ├── tools_schema.py         JSON Schema de las function tools (sección 7)
│   └── create_agent.py         Publica el agente en Foundry Agent Service
├── tools/                      Implementación local de las tools
│   ├── buscar_ejemplos.py      Plantilla + ejemplos desde knowledge/
│   ├── validar_estructura.py   Completitud y coherencia de los seis bloques
│   ├── generar_documento.py    Render Markdown + DOCX con el formato de plantilla
│   └── guardar_documento.py    Publica en el repositorio y registra la aprobación
├── app/
│   └── chat_cli.py             Runner local de la entrevista (sin Teams)
├── knowledge/                  Plantilla canónica + 3 historias de ejemplo extraídas
├── teams/
│   ├── manifest.json           Paquete de la app de Teams
│   └── cards/                  Adaptive Cards: Aprobar / Editar / Regenerar
├── docs/DEPLOY_TEAMS.md        Guía de despliegue en Teams (2 rutas)
└── output/ · repositorio/      Borradores generados y documentos publicados (MVP)
```

## Puesta en marcha

1. **Dependencias**
   ```bash
   python -m venv .venv && source .venv/Scripts/activate
   pip install -r requirements.txt
   ```
2. **Configuración** — copia `.env.example` a `.env` y rellena `PROJECT_ENDPOINT` y
   `MODEL_DEPLOYMENT_NAME`. Autenticación con `az login` (DefaultAzureCredential).
3. **Publicar el agente en Foundry**
   ```bash
   python agent/create_agent.py
   ```
4. **Probar la entrevista en local**
   ```bash
   python -m app.chat_cli
   ```
   El runner abre una conversación, el agente pide el título y conduce la entrevista.
   Las tools (`buscar_ejemplos`, `validar_estructura`, `generar_documento`,
   `guardar_documento`) se ejecutan en local. Sal con `/salir`; la sesión se puede
   retomar con `python -m app.chat_cli <conversation_id>`.

## Flujo human-in-the-loop

El agente recorre las fases de la spec: confirmación de alcance → entrevista por bloques
(Usuario → Funcionalidad → Objetivo → Descripción → Criterios → Aceptación) → revisión
integral con `validar_estructura` → aprobación final → `generar_documento` +
`guardar_documento`. Ningún bloque se cierra sin aprobación explícita, y el documento solo
se guarda tras el «aprobado» final, registrando quién y cuándo.

## Despliegue en Teams

Ver [docs/DEPLOY_TEAMS.md](docs/DEPLOY_TEAMS.md):

- **Ruta A (MVP)**: publicar el agente de Foundry directamente vía Azure Bot Service
  (activity protocol endpoint) — sin código de bot, compuertas HITL conversacionales.
- **Ruta B**: host propio con M365 Agents SDK y las Adaptive Cards de `teams/cards/`
  para botones Aprobar / Editar / Regenerar, SSO y mensajes proactivos.

## Estado del MVP

- [x] Plantilla canónica extraída de los DOCX de ejemplo (HU-011, HU-012, Beca)
- [x] System prompt con compuertas HITL
- [x] Function tools: buscar_ejemplos, validar_estructura, generar_documento, guardar_documento
- [x] `crear_work_item` definida (stub; pendiente integración Azure DevOps)
- [x] Runner CLI con pausa/retoma de sesión
- [x] Manifest de Teams + Adaptive Cards
- [ ] Host de Teams con Adaptive Cards (Ruta B)
- [ ] Guardado en SharePoint/Blob con managed identity
- [ ] Índice de AI Search para el grounding (MVP usa ficheros locales)
