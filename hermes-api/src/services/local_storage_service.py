import base64
import logging
import mimetypes
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.config.settings import get_settings

logger = logging.getLogger("hermes-api.local_storage")

HERMES_ROOT_FOLDER = "hermes"
DEFAULT_SUBFOLDERS = ["multimedia", "archivos", "whitelist"]
FOLDER_MIME = "inode/directory"
TRASH_FOLDER = ".trash"

_INVALID_NAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


class LocalStorageError(Exception):
    """Error de almacenamiento local con código HTTP sugerido."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class LocalStorageService:
    """
    Service layer para el bucket alojado en el servidor que hostea Hermes.
    Replica la interfaz pública de DriveService para que el módulo Multimedia
    pueda alternar entre Google Drive y el disco del servidor de forma transparente.

    Cada usuario tiene su propio bucket aislado en
    `<LOCAL_STORAGE_PATH>/<user_id>/` con las subcarpetas por defecto.
    Los IDs expuestos al frontend son la ruta relativa codificada en base64 urlsafe,
    de modo que resulten opacos y compatibles con los IDs de Google Drive.
    """

    def __init__(self, user_id: str):
        settings = get_settings()
        if not user_id:
            raise LocalStorageError("Usuario no válido para el almacenamiento local.", 401)

        base_path = Path(settings.LOCAL_STORAGE_PATH)
        if not base_path.is_absolute():
            api_root = Path(__file__).resolve().parents[2]
            base_path = api_root / base_path

        self.max_upload_bytes = settings.LOCAL_STORAGE_MAX_UPLOAD_MB * 1024 * 1024
        self.root = (base_path / self._sanitize_segment(user_id)).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    # ── Bucket Provisioning ──

    def ensure_hermes_bucket(self) -> Dict[str, Any]:
        """
        Verifica / crea el bucket del usuario en el servidor con sus subcarpetas por defecto.
        Devuelve los IDs de root, multimedia, archivos y whitelist.
        """
        for folder in DEFAULT_SUBFOLDERS:
            (self.root / folder).mkdir(parents=True, exist_ok=True)

        return {
            "root_id": self._encode_id(""),
            "root_name": HERMES_ROOT_FOLDER,
            "multimedia_id": self._encode_id("multimedia"),
            "archivos_id": self._encode_id("archivos"),
            "whitelist_id": self._encode_id("whitelist"),
            "folders": self._list_items(self.root, folders_only=True),
        }

    def ensure_whitelist_folder(self) -> str:
        """Verifica / crea la carpeta 'whitelist' para las fotos de la Lista de Deseos."""
        whitelist = self.root / "whitelist"
        whitelist.mkdir(parents=True, exist_ok=True)
        return self._encode_id("whitelist")

    # ── List Folder Contents ──

    def list_folder_contents(self, folder_id: str) -> Dict[str, Any]:
        """Lista archivos y subcarpetas dentro de una carpeta del servidor."""
        path = self._resolve_id(folder_id)
        if not path.is_dir():
            raise LocalStorageError("La carpeta solicitada no existe en el servidor.", 404)

        return {
            "files": self._list_items(path, folders_only=False),
            "current_folder_id": self._encode_id(self._relative(path)),
            "current_folder_name": HERMES_ROOT_FOLDER if path == self.root else path.name,
        }

    # ── Create Folder ──

    def create_folder(self, name: str, parent_id: str) -> Dict[str, str]:
        """Crea una nueva subcarpeta en el servidor."""
        parent = self._resolve_id(parent_id)
        if not parent.is_dir():
            raise LocalStorageError("La carpeta padre no existe en el servidor.", 404)

        target = parent / self._sanitize_segment(name)
        if target.exists():
            raise LocalStorageError(f"Ya existe un elemento llamado '{target.name}' en esta carpeta.", 409)

        target.mkdir()
        logger.info(f"Created local folder '{target.name}' in {self._relative(parent) or '/'}")
        return {
            "id": self._encode_id(self._relative(target)),
            "name": target.name,
            "parent_id": self._encode_id(self._relative(parent)),
        }

    # ── Upload File ──

    def upload_file(self, file_content: bytes, filename: str, mime_type: str, folder_id: str) -> Dict[str, Any]:
        """Guarda un archivo en una carpeta del servidor."""
        if len(file_content) > self.max_upload_bytes:
            raise LocalStorageError(
                f"El archivo excede el límite de {self.max_upload_bytes // (1024 * 1024)} MB "
                "permitido en el almacenamiento del servidor.",
                413,
            )

        folder = self._resolve_id(folder_id)
        if not folder.is_dir():
            raise LocalStorageError("La carpeta destino no existe en el servidor.", 404)

        target = self._unique_path(folder, self._sanitize_segment(filename))
        target.write_bytes(file_content)
        logger.info(f"Stored local file '{target.name}' ({len(file_content)} bytes) in {self._relative(folder) or '/'}")

        return {
            "id": self._encode_id(self._relative(target)),
            "name": target.name,
            "mime_type": mime_type or self._guess_mime(target),
            "size": str(len(file_content)),
            "thumbnail_link": None,
            "web_view_link": None,
            "folder_id": self._encode_id(self._relative(folder)),
        }

    # ── Download File Content ──

    def get_file_content(self, file_id: str) -> tuple[bytes, str, str]:
        """Lee el contenido binario de un archivo del servidor. Devuelve (bytes, mime_type, filename)."""
        path = self._resolve_id(file_id)
        if not path.is_file():
            raise LocalStorageError("El archivo no existe en el servidor.", 404)
        return path.read_bytes(), self._guess_mime(path), path.name

    # ── Trash File ──

    def trash_file(self, file_id: str) -> bool:
        """Mueve un archivo o carpeta a la papelera interna del bucket (`.trash`)."""
        path = self._resolve_id(file_id)
        if path == self.root:
            raise LocalStorageError("No se puede eliminar la carpeta raíz del bucket.", 400)
        if not path.exists():
            raise LocalStorageError("El archivo no existe en el servidor.", 404)

        trash = self.root / TRASH_FOLDER
        trash.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        shutil.move(str(path), str(self._unique_path(trash, f"{stamp}_{path.name}")))
        logger.info(f"Moved local item '{path.name}' to {TRASH_FOLDER}")
        return True

    # ── Preview Info ──

    def get_preview_info(self, file_id: str) -> Dict[str, Any]:
        """
        Metadatos de previsualización de un archivo del servidor.
        No hay enlaces externos: el frontend construye la URL del endpoint de contenido.
        """
        path = self._resolve_id(file_id)
        if not path.exists():
            raise LocalStorageError("El archivo no existe en el servidor.", 404)

        stat = path.stat()
        return {
            "file_id": self._encode_id(self._relative(path)),
            "file_name": path.name,
            "mime_type": FOLDER_MIME if path.is_dir() else self._guess_mime(path),
            "web_view_link": None,
            "web_content_link": None,
            "thumbnail_link": None,
            "size": None if path.is_dir() else str(stat.st_size),
        }

    # ── Internal Helpers ──

    def _list_items(self, path: Path, folders_only: bool = False) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        try:
            entries = sorted(
                (e for e in path.iterdir() if not e.name.startswith(".")),
                key=lambda e: (not e.is_dir(), e.name.lower()),
            )
        except OSError as e:
            logger.error(f"Error listing local folder {path}: {e}")
            raise LocalStorageError("No se pudo leer la carpeta en el servidor.", 500)

        for entry in entries:
            is_folder = entry.is_dir()
            if folders_only and not is_folder:
                continue
            stat = entry.stat()
            items.append({
                "id": self._encode_id(self._relative(entry)),
                "name": entry.name,
                "mime_type": FOLDER_MIME if is_folder else self._guess_mime(entry),
                "size": None if is_folder else str(stat.st_size),
                "thumbnail_url": None,
                "web_view_link": None,
                "created_time": self._iso(stat.st_ctime),
                "modified_time": self._iso(stat.st_mtime),
                "is_folder": is_folder,
                "icon_link": None,
            })
        return items

    def _relative(self, path: Path) -> str:
        rel = path.resolve().relative_to(self.root).as_posix()
        return "" if rel == "." else rel

    def _resolve_id(self, file_id: str) -> Path:
        """Decodifica un ID y garantiza que la ruta resultante viva dentro del bucket del usuario."""
        rel = self._decode_id(file_id)
        candidate = (self.root / rel).resolve() if rel else self.root
        if candidate != self.root and self.root not in candidate.parents:
            logger.warning(f"Blocked path traversal attempt for id '{file_id}'")
            raise LocalStorageError("Ruta no permitida en el almacenamiento del servidor.", 403)
        if candidate.name == TRASH_FOLDER or TRASH_FOLDER in candidate.relative_to(self.root).parts:
            raise LocalStorageError("La papelera del servidor no es accesible.", 403)
        return candidate

    @staticmethod
    def _encode_id(rel_path: str) -> str:
        raw = (rel_path or ".").strip("/") or "."
        return base64.urlsafe_b64encode(raw.encode("utf-8")).decode("ascii").rstrip("=")

    @staticmethod
    def _decode_id(file_id: str) -> str:
        if not file_id:
            raise LocalStorageError("Identificador de archivo vacío.", 400)
        padded = file_id + "=" * (-len(file_id) % 4)
        try:
            raw = base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8")
        except Exception:
            raise LocalStorageError("Identificador de archivo inválido para el servidor.", 400)
        return "" if raw == "." else raw

    @staticmethod
    def _sanitize_segment(name: str) -> str:
        cleaned = _INVALID_NAME_CHARS.sub("_", (name or "").strip()).lstrip(".").strip()
        cleaned = cleaned[:200]
        if not cleaned or cleaned in {".", ".."}:
            raise LocalStorageError("Nombre de archivo o carpeta no válido.", 400)
        return cleaned

    @staticmethod
    def _unique_path(folder: Path, name: str) -> Path:
        target = folder / name
        if not target.exists():
            return target
        stem, suffix = target.stem, target.suffix
        for i in range(1, 1000):
            candidate = folder / f"{stem} ({i}){suffix}"
            if not candidate.exists():
                return candidate
        raise LocalStorageError("No se pudo generar un nombre único para el archivo.", 409)

    @staticmethod
    def _guess_mime(path: Path) -> str:
        mime, _ = mimetypes.guess_type(path.name)
        return mime or "application/octet-stream"

    @staticmethod
    def _iso(timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
