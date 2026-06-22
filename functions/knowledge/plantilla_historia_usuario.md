# Plantilla de Historia de Usuario

> Formato canónico extraído de las historias de ejemplo (HU-011, HU-012, Carga de destinos Beca).
> El documento final es una serie de seis tablas de dos filas: la primera fila contiene la
> etiqueta del bloque y su pregunta guía; la segunda, el contenido.

**Identificador y título** (cabecera del documento): `HU-XXX - TÍTULO EN MAYÚSCULAS`
Subtítulo fijo: `Historia de Usuario`

---

| Usuario ¿Quién? | Usuarios de negocio que participan en la historia |
|---|---|
| | _Personas o roles de negocio: quién inicia, quién valida, quién recibe el resultado._ |

| Funcionalidad ¿Qué? | Descripción corta de la historia de usuario. |
|---|---|
| | _Una a tres frases: qué debe permitir hacer el sistema, qué datos o documentos se manejan._ |

| Objetivo ¿Para qué? | Para qué se necesita la historia de usuario. |
|---|---|
| | _Frase con la forma «Para que … pueda …»: problema de negocio que resuelve, valor que aporta, normativa o proceso al que responde._ |

| Descripción ¿Cómo? | Descripción de cómo se debe llevar a cabo la historia de usuario |
|---|---|
| | _Estructura obligatoria:_<br>1. Frase de encuadre (mecanismo general: «A través de un formulario…», «Mediante una interfaz de revisión…»).<br>2. Precondiciones (estado de partida: «El período debe estar en estado “Abierto”»).<br>3. Flujo numerado paso a paso, alternando acciones del usuario y respuestas del sistema.<br>4. Validaciones automáticas del sistema.<br>5. Almacenamiento del resultado y trazabilidad/auditoría.<br>6. Casos de error o excepción («Si no se adjuntan todos los documentos, el sistema no permite avanzar», «Si la firma falla, …»). |

| Criterios de aceptación | Condiciones específicas que deben cumplirse una vez desarrollada |
|---|---|
| | _Lista de condiciones observables y verificables. Cada criterio debe tener soporte en algún paso del flujo de la Descripción. Incluir estados finales esperados y reglas de bloqueo._ |

| Aceptación Usuarios | Especificar Quién y Cuándo |
|---|---|
| | Quién: _responsable de aceptar la historia_<br>Cuándo: _momento o hito de la aceptación_ |

---

## Reglas de estilo observadas en los ejemplos

- Redacción en español de España, voz activa, presente («La empresa beneficiaria accede…», «El sistema valida…»).
- Los actores se nombran de forma consistente en todo el documento (p. ej. «empresa beneficiaria», «auditor», «gestor»).
- Los estados del sistema van entre comillas españolas: «Abierto», «Presentada», «Con Incidencia».
- Los casos de error empiezan por «Si …» y cierran la Descripción.
- Los criterios de aceptación son frases cortas que empiezan por el sujeto (sistema/usuario) o por el resultado esperado.
- Lo no confirmado por el usuario se marca con «[por confirmar]».
