"""Tool guardar_documento: publica el documento aprobado y registra la aprobación.

MVP: copia el documento (y su DOCX hermano si existe) a un "repositorio"
local configurable con la variable de entorno REPOSITORIO_DIR, y anota la
aprobación en `repositorio/registro_aprobaciones.jsonl`.

En producción, sustituir `_publicar` por la subida a SharePoint (Graph),
Azure DevOps Wiki o Blob Storage con managed identity; el contrato de la
tool no cambia.
"""

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REPO = Path("/tmp/hu-repositorio")


def _publicar(origen: Path, repo: Path) -> Path:
    destino = repo / origen.name
    shutil.copy2(origen, destino)
    return destino


def guardar_documento(ruta_documento: str, aprobado_por: str, fecha_aprobacion: str) -> dict:
    origen = Path(ruta_documento)
    if not origen.is_file():
        return {"error": f"No existe el documento: {ruta_documento}"}

    repo = Path(os.environ.get("REPOSITORIO_DIR", str(DEFAULT_REPO)))
    repo.mkdir(parents=True, exist_ok=True)

    publicados = [str(_publicar(origen, repo))]
    for hermano in (origen.with_suffix(".docx"), origen.with_suffix(".md")):
        if hermano != origen and hermano.is_file():
            publicados.append(str(_publicar(hermano, repo)))

    registro = {
        "documento": origen.name,
        "aprobado_por": aprobado_por,
        "fecha_aprobacion": fecha_aprobacion,
        "guardado_en": datetime.now(timezone.utc).isoformat(),
        "rutas": publicados,
    }
    with (repo / "registro_aprobaciones.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

    return {
        "guardado": True,
        "enlace": publicados[0],
        "todos_los_formatos": publicados,
        "aprobacion_registrada": {"quien": aprobado_por, "cuando": fecha_aprobacion},
    }
