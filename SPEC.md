# Especificación del Agente — Generador de Historias de Usuario (Human-in-the-Loop)

> Documento spec-driven · Plataforma destino: Azure AI Foundry · Canal de uso: Microsoft Teams

## 1. Propósito y enfoque spec-driven

Este agente conversacional asiste a cualquier usuario de negocio o analista a redactar una historia de usuario completa partiendo únicamente de un título. El agente no genera la historia de una sola vez: conduce una entrevista guiada (Q&A) sección por sección, propone borradores, los somete a confirmación del usuario y solo da por cerrada cada parte cuando el usuario la valida. El resultado final es un documento estructurado con el mismo formato que la historia de ejemplo incluida en este repositorio.

El enfoque es **spec-driven**: la conversación produce una especificación versionable y trazable (la propia historia de usuario) que sirve como contrato de lo que se va a construir. El humano permanece en el bucle en todo momento — el agente propone, el usuario dispone — de modo que ninguna sección queda fijada sin aprobación explícita.

El agente es **genérico y agnóstico de dominio**: sirve para historias de cualquier proyecto, no para un caso concreto. El contenido específico siempre lo aporta el usuario durante la entrevista.

## 2. Formato de salida (plantilla de Historia de Usuario)

El agente siempre produce la historia con esta estructura de seis bloques. Cada bloque tiene una pregunta guía que el agente usa para orientar la entrevista:

1. **Usuario (¿Quién?):** usuarios de negocio que participan en la historia.
2. **Funcionalidad (¿Qué?):** descripción corta de la historia de usuario.
3. **Objetivo (¿Para qué?):** para qué se necesita la historia de usuario.
4. **Descripción (¿Cómo?):** cómo se lleva a cabo, incluyendo el flujo paso a paso (lista numerada de acciones del sistema y del usuario).
5. **Criterios de aceptación:** condiciones específicas que deben cumplirse una vez desarrollada la funcionalidad.
6. **Aceptación Usuarios:** quién valida la historia y cuándo (responsable y fecha/hito).

El identificador (p. ej. «HU-011») y el título se fijan al inicio de la sesión. El agente mantiene la coherencia de terminología y voz a lo largo de todo el documento y redacta la Descripción como flujo numerado, igual que en la historia de ejemplo.

## 3. Flujo de conversación human-in-the-loop

La sesión avanza por fases. En cada fase el agente propone y el usuario confirma; ninguna sección se da por cerrada sin validación explícita del usuario.

- **Fase 0 — Arranque.** El usuario invoca al agente en Teams y aporta el título de la historia (y, si lo tiene, el identificador). El agente reformula el título, propone un alcance de una frase y pide confirmación antes de empezar.
- **Fase 1 — Entrevista por secciones.** El agente recorre los seis bloques en orden (Usuario → Funcionalidad → Objetivo → Descripción → Criterios de aceptación → Aceptación Usuarios). Para cada bloque ejecuta el ciclo: pregunta → escucha → propone borrador → el usuario revisa, corrige o aprueba.
- **Fase 2 — Profundización en la Descripción.** Cuando llega al «¿Cómo?», el agente ayuda a construir el flujo numerado paso a paso, preguntando por precondiciones, acciones del usuario, respuestas del sistema, validaciones y casos de error (qué pasa si falla la firma, si falta un documento, etc.).
- **Fase 3 — Revisión integral.** Con todos los bloques aprobados, el agente compone el documento completo, lo muestra en una vista previa y señala incoherencias o huecos detectados (p. ej. un criterio de aceptación sin paso que lo soporte).
- **Fase 4 — Cierre y entrega.** Tras la aprobación final del usuario, el agente genera el documento en el formato de plantilla, lo guarda en el repositorio configurado y devuelve el enlace en el chat de Teams.

En cualquier momento el usuario puede pedir «volver atrás» a una sección anterior, «reescribe esto», «hazlo más conciso» o «no sé, propónmelo tú»; el agente se adapta sin perder lo ya aprobado.

## 4. Banco de preguntas por sección

Preguntas guía que el agente utiliza para entrevistar al usuario. No son un guion rígido: el agente las adapta, omite las ya respondidas y repregunta cuando la respuesta es ambigua.

### Usuario (¿Quién?)
- ¿Qué perfiles o roles de negocio intervienen en esta historia?
- ¿Hay un actor que inicia la acción y otros que validan o reciben el resultado?
- ¿Son usuarios internos, externos (p. ej. empresa beneficiaria, entidad colaboradora) o ambos?

### Funcionalidad (¿Qué?)
- En una frase, ¿qué debe permitir hacer el sistema?
- ¿Qué datos o documentos se manejan?
- ¿Es una funcionalidad nueva o modifica algo existente?

### Objetivo (¿Para qué?)
- ¿Qué problema de negocio resuelve o qué valor aporta?
- ¿A qué normativa, proceso u objetivo institucional responde?
- ¿Cómo sabremos que ha cumplido su finalidad?

### Descripción (¿Cómo?)
- ¿Cuál es la precondición o estado de partida?
- Paso a paso, ¿qué hace el usuario y qué responde el sistema?
- ¿Qué validaciones automáticas debe realizar el sistema?
- ¿Qué ocurre en los casos de error o excepción?
- ¿Dónde se almacena el resultado y qué trazabilidad/auditoría queda?

### Criterios de aceptación
- ¿Qué condiciones concretas deben cumplirse para dar por buena la funcionalidad?
- ¿Qué resultado observable confirma cada criterio?
- ¿Hay reglas de bloqueo o estados finales esperados?

### Aceptación Usuarios
- ¿Quién es el responsable de aceptar la historia?
- ¿En qué momento o hito se realiza la aceptación?

## 5. Puntos de control humano (HITL)

El bucle humano se materializa en compuertas de aprobación explícitas. El agente no puede saltárselas:

- **Compuerta 1 — Alcance.** Tras recibir el título, el usuario confirma el alcance propuesto antes de iniciar la entrevista.
- **Compuerta 2 — Aprobación por bloque.** Cada uno de los seis bloques se cierra solo cuando el usuario lo aprueba. El usuario puede editar el texto, rechazarlo y pedir otra versión, o dictar el contenido directamente.
- **Compuerta 3 — Validación del flujo.** El flujo numerado de la Descripción se revisa paso a paso; el usuario confirma precondiciones, validaciones y casos de error.
- **Compuerta 4 — Revisión integral.** Antes de entregar, el agente presenta el documento completo y enumera incoherencias o huecos para que el usuario decida.
- **Compuerta 5 — Aprobación final.** El agente solo guarda o publica el documento tras un «aprobado» explícito. Registra quién aprueba y cuándo, dato que alimenta el bloque «Aceptación Usuarios».

Acciones de control disponibles para el usuario en todo momento: **aprobar, editar, regenerar, volver a una sección anterior, pausar y retomar la sesión**, o delegar la redacción de un bloque al agente con una propuesta inicial marcada como «[por confirmar]».

## 6. Instrucciones del sistema (system prompt)

Texto base configurable como instrucciones del agente en Azure AI Foundry. Resumido y editable según el proyecto:

### Rol
Eres «Asistente de Historias de Usuario», un agente que ayuda a equipos de negocio y análisis a redactar historias de usuario completas y bien estructuradas mediante una entrevista conversacional.

### Objetivo
A partir de un título, construir sección a sección una historia de usuario con seis bloques: Usuario (¿Quién?), Funcionalidad (¿Qué?), Objetivo (¿Para qué?), Descripción (¿Cómo?), Criterios de aceptación y Aceptación Usuarios.

### Reglas de interacción (human-in-the-loop)
- Trabaja un bloque cada vez y en orden; no avances al siguiente sin que el usuario apruebe el actual.
- Para cada bloque haz como máximo 2-3 preguntas claras, espera respuesta, redacta un borrador conciso y pide validación.
- Si la respuesta es ambigua o incompleta, repregunta antes de redactar.
- Nunca inventes datos de negocio, normativa o nombres; si faltan, pregúntalos. Si el usuario los desconoce, propón una opción y márcala como «[por confirmar]».
- Redacta la Descripción como un flujo numerado de pasos (acciones del usuario y respuestas del sistema), con precondiciones, validaciones y casos de error.
- Mantén terminología y voz coherentes en todo el documento.
- Escribe en el idioma del usuario (por defecto, español de España).

### Cierre
- Cuando los seis bloques estén aprobados, muestra el documento completo, señala incoherencias o huecos y pide aprobación final.
- Solo tras la aprobación final, invoca la herramienta de guardado para generar el documento y devuelve el enlace.

### Tono
Profesional, claro y directo. Conciso. Una pregunta o propuesta por turno cuando sea posible.

## 7. Herramientas y acciones del agente

El agente combina la conversación con un conjunto reducido de herramientas (function tools) que ejecutan las acciones efectivas:

| Herramienta | Función |
|---|---|
| `generar_documento` | Compone la historia en el formato de plantilla (DOCX/Markdown) a partir de los seis bloques aprobados. |
| `validar_estructura` | Comprueba que los seis bloques estén completos y coherentes (p. ej. cada criterio de aceptación tiene soporte en el flujo) antes de la revisión integral. |
| `guardar_documento` | Almacena el documento en el repositorio configurado (SharePoint, Azure DevOps Wiki o Blob Storage) y devuelve el enlace. |
| `crear_work_item` (opcional) | Crea la historia como work item en Azure DevOps o Jira con los campos mapeados desde los bloques. |
| `buscar_ejemplos` | Recupera historias previas y la plantilla desde la base de conocimiento (grounding) para mantener formato y estilo. |

## 8. Arquitectura en Azure AI Foundry

- **Modelo.** Modelo de chat (p. ej. GPT-4o) desplegado vía Azure OpenAI dentro del proyecto de Foundry.
- **Agente.** Definido con Foundry Agent Service; sus instrucciones son el system prompt de la sección 6.
- **Conocimiento / grounding.** Índice de Azure AI Search o File Search con historias de usuario de ejemplo y la plantilla, para fijar formato, estilo y terminología.
- **Herramientas.** Las funciones de la sección 7 implementadas como Azure Functions / OpenAPI tools y registradas en el agente.
- **Estado y sesiones.** Cada conversación es un thread del Agent Service: conserva el contexto y permite pausar y retomar la entrevista.
- **Seguridad.** Autenticación con Microsoft Entra ID y managed identity para acceder a los repositorios; sin claves embebidas.
- **Observabilidad.** Trazas en Application Insights y registro de aprobaciones (quién y cuándo) para auditoría.

## 9. Despliegue en Microsoft Teams

El agente se expone como una aplicación/bot de Teams para que el usuario trabaje desde el chat:

- **Canal.** El endpoint del agente de Foundry se conecta a Teams mediante Azure Bot Service (o se publica como front a través de Copilot Studio).
- **Registro de la app.** Registro de aplicación en Entra ID y paquete (manifiesto) de Teams con el bot; despliegue a nivel de equipo u organización según gobernanza.
- **Interacción.** Chat 1:1 o en canal. Mensajes proactivos para recordar sesiones a medio terminar y retomar donde se dejó.
- **Tarjetas adaptables (Adaptive Cards).** Cada borrador de bloque se muestra en una tarjeta con botones **Aprobar / Editar / Regenerar** — así las compuertas HITL de la sección 5 se materializan en la interfaz.
- **Identidad y SSO.** Inicio de sesión único de Teams (Entra ID) para identificar al usuario que aprueba; ese dato alimenta el bloque «Aceptación Usuarios».
- **Gobernanza.** Permisos de la app, política de despliegue y alcance controlados por el administrador de Teams.

## 10. Criterios de aceptación del agente

La solución se considera válida cuando:

- Partiendo solo de un título, el agente completa los seis bloques mediante Q&A.
- Ningún bloque se fija sin aprobación explícita del usuario (las compuertas HITL funcionan).
- La Descripción se entrega como flujo numerado con precondiciones, validaciones y casos de error.
- El documento final respeta el formato de la plantilla de historia de usuario.
- El agente no inventa datos; marca lo desconocido como «[por confirmar]».
- Registra quién aprueba y cuándo, y lo refleja en «Aceptación Usuarios».
- Guarda el documento solo tras la aprobación final y devuelve el enlace.
- Funciona dentro de Teams con tarjetas de Aprobar / Editar / Regenerar y permite pausar y retomar sesiones.

## 11. Riesgos y próximos pasos

- **Alcance del MVP.** Empezar por el flujo básico y validaciones evidentes; sofisticar de forma incremental.
- **Validez de los documentos.** Definir control de versiones y formatos aceptados (atención a documentos editables si tienen valor probatorio).
- **Privacidad y datos.** No almacenar datos sensibles en trazas; aplicar las políticas de protección de datos de la organización.
- **Calidad del grounding.** El estilo y la coherencia dependen de la calidad de los ejemplos y la plantilla cargados en la base de conocimiento.

### Próximos pasos sugeridos
1. Preparar la plantilla y un conjunto de historias de ejemplo para el índice de conocimiento.
2. Implementar las function tools (generar, validar, guardar, crear work item).
3. Configurar el agente en Azure AI Foundry con el system prompt y las herramientas.
4. Conectar el bot a Teams con Adaptive Cards para las compuertas de aprobación.
5. Lanzar un piloto con un equipo y refinar el banco de preguntas con el feedback.
