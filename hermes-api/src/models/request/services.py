from pydantic import BaseModel, Field
from typing import Optional


class CreateFolderRequest(BaseModel):
    """Request para crear una subcarpeta en Google Drive."""
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la nueva carpeta")
    parent_folder_id: str = Field(..., description="ID de la carpeta padre en Google Drive")
