import logging
import io
from typing import Any, Dict, List, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from src.utils.google_credentials import build_google_credentials

logger = logging.getLogger("hermes-api.drive")

HERMES_ROOT_FOLDER = "hermes"
DEFAULT_SUBFOLDERS = ["multimedia", "archivos"]
FOLDER_MIME = "application/vnd.google-apps.folder"


class DriveService:
    """Service layer for Google Drive API v3 interactions."""

    def __init__(self, access_token: str):
        creds = build_google_credentials(access_token)
        self.service = build("drive", "v3", credentials=creds, cache_discovery=False)

    # ── Bucket Provisioning ──

    def ensure_hermes_bucket(self) -> Dict[str, Any]:
        """
        Verify / create the hermes root folder and default subfolders in the user's Drive.
        Returns IDs for root, multimedia, and archivos folders.
        """
        root_id = self._find_or_create_folder(HERMES_ROOT_FOLDER, parent_id="root")
        multimedia_id = self._find_or_create_folder("multimedia", parent_id=root_id)
        archivos_id = self._find_or_create_folder("archivos", parent_id=root_id)

        # List all direct children folders of hermes root
        folders = self._list_items(root_id, folders_only=True)

        return {
            "root_id": root_id,
            "root_name": HERMES_ROOT_FOLDER,
            "multimedia_id": multimedia_id,
            "archivos_id": archivos_id,
            "folders": folders,
        }

    def ensure_whitelist_folder(self) -> str:
        """
        Verify / create the 'whitelist' folder inside hermes root folder for Wishlist item photos.
        Returns the folder ID of 'whitelist'.
        """
        root_id = self._find_or_create_folder(HERMES_ROOT_FOLDER, parent_id="root")
        whitelist_id = self._find_or_create_folder("whitelist", parent_id=root_id)
        return whitelist_id

    # ── List Folder Contents ──

    def list_folder_contents(self, folder_id: str) -> Dict[str, Any]:
        """List all files and subfolders inside a given folder."""
        items = self._list_items(folder_id, folders_only=False)

        # Get folder name
        folder_name = "hermes"
        try:
            meta = self.service.files().get(fileId=folder_id, fields="name").execute()
            folder_name = meta.get("name", folder_id)
        except Exception:
            pass

        return {
            "files": items,
            "current_folder_id": folder_id,
            "current_folder_name": folder_name,
        }

    # ── Create Folder ──

    def create_folder(self, name: str, parent_id: str) -> Dict[str, str]:
        """Create a new subfolder."""
        file_metadata = {
            "name": name,
            "mimeType": FOLDER_MIME,
            "parents": [parent_id],
        }
        try:
            folder = self.service.files().create(
                body=file_metadata, fields="id,name"
            ).execute()
            logger.info(f"Created folder '{name}' (ID: {folder['id']}) in parent {parent_id}")
            return {"id": folder["id"], "name": folder["name"], "parent_id": parent_id}
        except Exception as e:
            logger.error(f"Error creating folder '{name}': {e}")
            raise

    # ── Upload File ──

    def upload_file(self, file_content: bytes, filename: str, mime_type: str, folder_id: str) -> Dict[str, Any]:
        """Upload a file to a specific folder."""
        file_metadata = {
            "name": filename,
            "parents": [folder_id],
        }
        media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype=mime_type, resumable=True)
        try:
            uploaded = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id,name,mimeType,size,webViewLink,thumbnailLink",
            ).execute()
            logger.info(f"Uploaded file '{filename}' (ID: {uploaded['id']}) to folder {folder_id}")
            return {
                "id": uploaded["id"],
                "name": uploaded["name"],
                "mime_type": uploaded.get("mimeType", mime_type),
                "size": uploaded.get("size") or str(len(file_content)),
                "thumbnail_link": uploaded.get("thumbnailLink"),
                "web_view_link": uploaded.get("webViewLink"),
                "folder_id": folder_id,
            }
        except Exception as e:
            logger.error(f"Error uploading file '{filename}': {e}")
            raise

    # ── Trash File ──

    def trash_file(self, file_id: str) -> bool:
        """Move a file to trash."""
        try:
            self.service.files().update(fileId=file_id, body={"trashed": True}).execute()
            logger.info(f"File {file_id} moved to trash")
            return True
        except Exception as e:
            logger.error(f"Error trashing file {file_id}: {e}")
            raise

    # ── Preview URL ──

    def get_preview_info(self, file_id: str) -> Dict[str, Any]:
        """Get preview/download links for a file."""
        try:
            file_meta = self.service.files().get(
                fileId=file_id,
                fields="id,name,mimeType,size,webViewLink,webContentLink,thumbnailLink",
            ).execute()
            return {
                "file_id": file_meta["id"],
                "file_name": file_meta.get("name", ""),
                "mime_type": file_meta.get("mimeType", ""),
                "web_view_link": file_meta.get("webViewLink"),
                "web_content_link": file_meta.get("webContentLink"),
                "thumbnail_link": file_meta.get("thumbnailLink"),
                "size": file_meta.get("size"),
            }
        except Exception as e:
            logger.error(f"Error getting preview for file {file_id}: {e}")
            raise

    # ── Internal Helpers ──

    def _find_or_create_folder(self, name: str, parent_id: str) -> str:
        """Find a folder by name under parent, or create it."""
        query = (
            f"name='{name}' and mimeType='{FOLDER_MIME}' "
            f"and '{parent_id}' in parents and trashed=false"
        )
        try:
            results = self.service.files().list(
                q=query, spaces="drive", fields="files(id,name)", pageSize=1
            ).execute()
            files = results.get("files", [])
            if files:
                return files[0]["id"]
        except Exception as e:
            logger.warning(f"Error searching for folder '{name}': {e}")

        # Create if not found
        return self.create_folder(name, parent_id)["id"]

    def _list_items(self, folder_id: str, folders_only: bool = False) -> List[Dict[str, Any]]:
        """List items in a folder."""
        query = f"'{folder_id}' in parents and trashed=false"
        if folders_only:
            query += f" and mimeType='{FOLDER_MIME}'"

        try:
            results = self.service.files().list(
                q=query,
                spaces="drive",
                fields="files(id,name,mimeType,size,thumbnailLink,webViewLink,createdTime,modifiedTime,iconLink)",
                orderBy="folder,name",
                pageSize=100,
            ).execute()

            items = []
            for f in results.get("files", []):
                items.append({
                    "id": f["id"],
                    "name": f["name"],
                    "mime_type": f.get("mimeType", ""),
                    "size": f.get("size"),
                    "thumbnail_url": f.get("thumbnailLink"),
                    "web_view_link": f.get("webViewLink"),
                    "created_time": f.get("createdTime"),
                    "modified_time": f.get("modifiedTime"),
                    "is_folder": f.get("mimeType") == FOLDER_MIME,
                    "icon_link": f.get("iconLink"),
                })
            return items
        except Exception as e:
            logger.error(f"Error listing folder {folder_id}: {e}")
            raise
