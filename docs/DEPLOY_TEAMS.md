# Despliegue del agente en Microsoft Teams

Dos rutas posibles, de menor a mayor control. Para el MVP se recomienda la **Ruta A**.

## Ruta A — Publicación directa del agente de Foundry (recomendada para MVP)

Foundry Agent Service expone cada agente con un *activity protocol endpoint* que
Azure Bot Service puede usar directamente como messaging endpoint, sin código de bot propio.

1. **Crear el agente** (una vez configurado `.env`):
   ```bash
   python agent/create_agent.py
   ```
2. **Identidad**: el agente necesita un *principal* (app registration / managed identity).
   Anota su `appId` y el `tenantId`.
3. **Azure Bot Service**: crea el recurso bot con endpoint:
   ```
   https://<recurso>.services.ai.azure.com/api/projects/<proyecto>/agents/<agent-name>/endpoint/protocols/activityProtocol?api-version=2025-05-15-preview
   ```
   ```azurecli
   az deployment group create \
     --resource-group <rg> \
     --template-file bot-service.bicep \
     --parameters botName=<bot> displayName="Historias de Usuario" \
                  msaAppId=<agent-principal-id> tenantId=<tenant-id> \
                  endpoint=<activity-protocol-endpoint>
   ```
4. **Canal Teams**: en el recurso Azure Bot → *Channels* → *Microsoft Teams* → aceptar términos y aplicar.
5. **Paquete de Teams**: completa los GUID en [teams/manifest.json](../teams/manifest.json),
   añade `color.png` (192×192) y `outline.png` (32×32), comprime los tres ficheros en un `.zip`
   y súbelo en Teams (*Apps → Manage your apps → Upload an app*) o publícalo vía el
   admin center según la gobernanza de la organización.

> Referencia: [Publish agents to Microsoft 365 Copilot and Teams](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-copilot-virtual-network)

**Limitación de la Ruta A**: las respuestas llegan como texto/markdown; las Adaptive Cards
con botones Aprobar/Editar/Regenerar requieren un host propio (Ruta B). Las compuertas HITL
siguen funcionando de forma conversacional («apruebo», «regenera», «edita: …»).

## Ruta B — Host propio con Adaptive Cards (M365 Agents SDK)

Para materializar las compuertas HITL con botones (tarjetas de [teams/cards/](../teams/cards/)):

1. **Web App** (App Service, Python) que recibe las activities de Teams en `/api/messages`
   usando el **Microsoft 365 Agents SDK** (sucesor del Bot Framework SDK).
2. El handler del bot reutiliza la misma lógica que [app/chat_cli.py](../app/chat_cli.py):
   - mapea `conversation` de Teams ↔ `conversation` de Foundry (persistir la relación en Storage/Cosmos);
   - reenvía el texto del usuario con `responses.create(...)` + `agent_reference`;
   - ejecuta los `function_call` con `tools.ejecutar_tool(...)`;
   - cuando el agente propone un borrador de bloque, lo envuelve en `bloque_card.json`
     (plantilla Adaptive Card con binding `${...}`);
   - los `Action.Submit` llegan como activity con `value.accion` (`aprobar`, `editar`,
     `regenerar`, `volver`, `aprobacion_final`, `pausar`) y se traducen a mensajes para el agente.
3. **Azure Bot** apuntando a `https://<webapp>.azurewebsites.net/api/messages`, canal Teams activado.
4. **SSO**: OAuth connection (Azure AD v2) en el bot para identificar al usuario que aprueba;
   el `preferred_username` del token alimenta `aprobado_por` en `guardar_documento`.
5. **Mensajes proactivos** para recordar sesiones a medio terminar: guardar el
   `conversationReference` de Teams y usar `continue_conversation` desde un timer
   (Azure Functions) que consulte sesiones pausadas.

## Seguridad y observabilidad (ambas rutas)

- **Managed identity** para acceder a SharePoint/Blob/DevOps desde `guardar_documento` y
  `crear_work_item`; sin claves embebidas.
- **Application Insights** en el proyecto de Foundry para trazas; el registro de aprobaciones
  queda además en `repositorio/registro_aprobaciones.jsonl` (MVP) o en la tabla/lista que
  se configure en producción.
- No registrar datos sensibles en trazas (política de protección de datos de la organización).
