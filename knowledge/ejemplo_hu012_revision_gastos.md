HU-012- REVISIÓN DE GASTOS E INFORME PROVISIONALHU-012- REVISIÓN DE GASTOS E INFORME PROVISIONALHistoria de UsuarioHistoria de Usuario

| Usuario ¿Quién? | Usuarios de negocio que participan en la historia |
|  | Rocio Viñas, Eduardo Sanchez, Adela Gimenez, Esther Espinosa |

| Funcionalidad<br>¿Qué? | Descripción corta de la historia de usuario. |
|  | El auditor revisa el expediente de gastos presentado por una empresa, analizando los documentos cargados, verificando que cumplan con los requisitos establecidos, comprobando su validez y generando un informe provisional. |

| Objetivo<br>¿Para qué? | Para qué se necesita la historia de usuario. |
|  | Para detectar inconsistencias y permitir la corrección antes del cierre del proceso, garantizando que solo se aprueban gastos válidos conforme a la normativa y bases reguladoras. |

| Descripción<br>¿Cómo? | Descripción de cómo se debe llevar a cabo la historia de usuario |
|  | Mediante una interfaz de revisión con herramientas para validar documentos y generar observaciones.<br>Los gastos deben coincidir con las partidas presupuestarias aprobadas.<br>Se deben rechazar gastos que no cumplan con las condiciones establecidas.<br>El auditor accede al site Auditor.<br>Abre el expediente de la empresa asignada, este debe estar en estado “presentado”.<br>Se muestran los gastos y el auditor revisa cada gasto y su documentación.<br>Clasifica: Elegible, No Elegible, Con Incidencia.<br>Añade comentarios por línea y marca como completado.<br>En el caso de que la revisión se esté realizando “in situ”, permitir añadir nueva documentación que complete la justificación de un gasto, en los casos que sean necesarios.<br>Para la facilidad de revisión de estos documentos, se debe de implentar una validación automática de gastos subvencionables mediante IA y OCR:<br>Document Classification: Clasifique y encamine automáticamente los documentos importantes, reduciendo la carga de trabajo<br>Document Extraction: Extraiga automáticamente datos estructurados de documentos/facturas y formularios.<br>Chat con los documentos (IA-Copilot)<br>Automatización de la generación de informes de justificación para facilitar el control financiero y la trasparencia.<br>Control de plazos y alertas para evitar retrasos en la presentación y eficientando el proceso.<br>El sistema genera el informe provisional en PDF, el cual debe incluir:<br>Resumen general<br>Total de gastos elegibles/no elegibles<br>Detalle por línea<br>Se notifica a la empresa y al gestor correspondiente.<br>Se abre el plazo de presentación de alegaciones una vez recibida las notificaciones (10 días)<br>Si falta documentación, se marca automáticamente como “Con Incidencia”.<br>Si el PDF no se puede generar, se guarda en estado “Revisión finalizada sin informe” |

| Criterios de aceptación | Condiciones específicas que deben cumplirse una vez desarrollada |
|  | El auditor debe poder visualizar todos los gastos presentados de las empresas beneficiarias.<br>Se debe permitir marcar gastos como Elegible, No Elegible, Con Incidencia”.<br>El beneficiario debe recibir una notificación con el estado de sus gastos.<br>Cada anotación genera automáticamente una incidencia y justificación.<br>Se genera un documento resumen (informe provisional) para el gestor, con copia para la empresa.<br>El informe debe estar firmado electrónicamente.<br>Auditoría interna de Appian: quién revisó, cuándo, y qué campos modificó. |

|  | Especificar Quién y Cuándo |
| Aceptación Usuarios | Quién:<br>Cuándo: |
