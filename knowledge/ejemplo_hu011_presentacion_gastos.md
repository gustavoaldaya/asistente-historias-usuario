HU-011- PRESENTACIÓN GASTOSHU-011- PRESENTACIÓN GASTOSHistoria de UsuarioHistoria de Usuario

| Usuario ¿Quién? | Usuarios de negocio que participan en la historia |
|  | Rocio Viñas, Eduardo Sanchez, Adela Gimenez, Esther Espinosa |

| Funcionalidad<br>¿Qué? | Descripción corta de la historia de usuario. |
|  | La empresa beneficiaria presenta un expediente de justificación de Gastos.La empresa beneficiaria sube justificantes de gasto, justificantes de pago y otra documentación al sistema. Carga de datos y documentos justificativos, validación y firma. |

| Objetivo<br>¿Para qué? | Para qué se necesita la historia de usuario. |
|  | Para que la empresa pueda justificar correctamente el uso de la ayuda recibida y que ICEX pueda evaluar y reembolsar los importes subvencionables y garantizar el cumplimiento normativo. |

| Descripción<br>¿Cómo? | Descripción de cómo se debe llevar a cabo la historia de usuario |
|  | A través de un formulario estructurado que permite adjuntar archivos y detallar conceptos.<br>El período de justificación debe estar en estado “Abierto”.<br>La empresa beneficiaria accede al site Empresa.<br>Inicia nuevo expediente desde el panel “Mis Justificaciones”.<br>Completa el formulario con información del proyecto (datos generales, económicos, etc), y lista gastos.<br>Adjunta facturas, justificantes y otros documentos por gasto.<br>Cada gasto debe adjuntar: Factura, Justificante bancario y Documentos adicionales (si aplica).<br>El sistema valida automáticamente que los gastos sean elegibles (formatos y obligatoriedad).<br>Se genera un resumen con el total de gastos presentados.<br>Guarda el expediente como borrador o genera PDF para firma.<br>Firma electrónicamente.<br>El sistema cambia el estado a “Presentada” y se bloquea su edición excepto si se requiere subsanación.<br>Documentación almacenada en Alfresco con metadatos.<br>Se genera entrada de auditoría<br>Si no se adjuntan todos los documentos, el sistema no permite avanzar.<br>Si la firma falla, se mantiene el estado “pendiente” hasta reintento. |

| Criterios de aceptación | Condiciones específicas que deben cumplirse una vez desarrollada |
|  | El sistema permite cargar facturas y comprobantes.<br>Valida que los datos ingresados coincidan con la resolución.<br>Acuse de recibo firmado para la empresa.<br>Expediente registrado como “Presentado”.<br>Documentación almacenada en Alfresco con metadatos.<br>Bloqueo del expediente excepto si se requiere subsanación. |

|  | Especificar Quién y Cuándo |
| Aceptación Usuarios | Quién:<br>Cuándo: |
