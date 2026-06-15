"""Definiciones (JSON Schema) de las function tools del agente.

Estas definiciones se registran en el agente de Azure AI Foundry
(`agent/create_agent.py`). La ejecución real vive en el paquete `tools/`
y la realiza el host (CLI local o bot de Teams) cuando el agente emite
un `function_call`.
"""

# Esquema compartido: una historia de usuario con sus seis bloques.
HISTORIA_SCHEMA = {
    "type": "object",
    "properties": {
        "identificador": {
            "type": "string",
            "description": "Identificador de la historia, p. ej. 'HU-011'. '[por confirmar]' si no se conoce.",
        },
        "titulo": {
            "type": "string",
            "description": "Título corto de la historia en mayúsculas, p. ej. 'PRESENTACIÓN GASTOS'.",
        },
        "usuario": {
            "type": "string",
            "description": "Bloque Usuario (¿Quién?): personas o roles de negocio que participan.",
        },
        "funcionalidad": {
            "type": "string",
            "description": "Bloque Funcionalidad (¿Qué?): descripción corta de la historia.",
        },
        "objetivo": {
            "type": "string",
            "description": "Bloque Objetivo (¿Para qué?): valor de negocio, con la forma 'Para que … pueda …'.",
        },
        "descripcion": {
            "type": "object",
            "description": "Bloque Descripción (¿Cómo?), estructurado.",
            "properties": {
                "encuadre": {
                    "type": "string",
                    "description": "Frase de encuadre con el mecanismo general, p. ej. 'A través de un formulario estructurado…'.",
                },
                "precondiciones": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Estado de partida requerido, p. ej. 'El período debe estar en estado «Abierto»'.",
                },
                "pasos": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Flujo numerado: acciones del usuario y respuestas del sistema, en orden.",
                },
                "validaciones": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Validaciones automáticas que realiza el sistema.",
                },
                "almacenamiento": {
                    "type": "string",
                    "description": "Dónde se almacena el resultado y qué trazabilidad/auditoría queda.",
                },
                "casos_error": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Casos de error o excepción; cada uno empieza por 'Si …'.",
                },
            },
            "required": ["encuadre", "pasos"],
        },
        "criterios_aceptacion": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Condiciones observables y verificables; cada una con soporte en el flujo.",
        },
        "aceptacion_usuarios": {
            "type": "object",
            "properties": {
                "quien": {"type": "string", "description": "Responsable de aceptar la historia."},
                "cuando": {"type": "string", "description": "Momento o hito de la aceptación."},
            },
            "required": ["quien", "cuando"],
        },
    },
    "required": [
        "identificador",
        "titulo",
        "usuario",
        "funcionalidad",
        "objetivo",
        "descripcion",
        "criterios_aceptacion",
        "aceptacion_usuarios",
    ],
}

TOOL_DEFINITIONS = [
    {
        "name": "buscar_ejemplos",
        "description": (
            "Recupera la plantilla de historia de usuario y las historias de ejemplo de la base "
            "de conocimiento para fijar formato, estilo y terminología. Llamar al inicio de la sesión."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "consulta": {
                    "type": "string",
                    "description": "Texto libre para filtrar ejemplos (opcional). Vacío devuelve plantilla y lista de ejemplos.",
                }
            },
            "required": [],
        },
    },
    {
        "name": "validar_estructura",
        "description": (
            "Comprueba que los seis bloques de la historia estén completos y sean coherentes "
            "(p. ej. cada criterio de aceptación tiene soporte en el flujo, no quedan marcas "
            "'[por confirmar]'). Llamar SIEMPRE antes de la revisión integral."
        ),
        "parameters": {
            "type": "object",
            "properties": {"historia": HISTORIA_SCHEMA},
            "required": ["historia"],
        },
    },
    {
        "name": "generar_documento",
        "description": (
            "Compone la historia de usuario en el formato de plantilla (Markdown y DOCX) a partir "
            "de los seis bloques aprobados. Devuelve las rutas de los borradores generados. "
            "Llamar solo tras la aprobación final del usuario."
        ),
        "parameters": {
            "type": "object",
            "properties": {"historia": HISTORIA_SCHEMA},
            "required": ["historia"],
        },
    },
    {
        "name": "guardar_documento",
        "description": (
            "Guarda el documento generado en el repositorio configurado y devuelve el enlace. "
            "Registra quién aprueba y cuándo. Llamar solo después de generar_documento."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ruta_documento": {
                    "type": "string",
                    "description": "Ruta del documento devuelta por generar_documento.",
                },
                "aprobado_por": {
                    "type": "string",
                    "description": "Nombre de la persona que da la aprobación final.",
                },
                "fecha_aprobacion": {
                    "type": "string",
                    "description": "Fecha de la aprobación final (ISO 8601, p. ej. 2026-06-12).",
                },
            },
            "required": ["ruta_documento", "aprobado_por", "fecha_aprobacion"],
        },
    },
    {
        "name": "crear_work_item",
        "description": (
            "OPCIONAL: crea la historia como work item en Azure DevOps con los campos mapeados "
            "desde los bloques. Llamar solo si el usuario lo pide explícitamente."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "historia": HISTORIA_SCHEMA,
                "proyecto": {
                    "type": "string",
                    "description": "Nombre del proyecto de Azure DevOps de destino.",
                },
            },
            "required": ["historia", "proyecto"],
        },
    },
]
