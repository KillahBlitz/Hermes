from typing import List, Optional
from pydantic import BaseModel, Field


# ── Google Drive Requests ──

class CreateFolderRequest(BaseModel):
    """Request para crear una subcarpeta en Google Drive."""
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la nueva carpeta")
    parent_folder_id: str = Field(..., description="ID de la carpeta padre en Google Drive")


# ── Google Calendar Requests ──

class CalendarEventCreateRequest(BaseModel):
    """Request para crear un nuevo evento en Google Calendar."""
    summary: str = Field(..., min_length=1, max_length=255, description="Título del evento")
    description: Optional[str] = Field(None, max_length=2000, description="Descripción o notas del evento")
    location: Optional[str] = Field(None, max_length=500, description="Ubicación física o enlace virtual")
    start_time: str = Field(..., description="Fecha y hora de inicio (ISO 8601 o YYYY-MM-DD)")
    end_time: str = Field(..., description="Fecha y hora de fin (ISO 8601 o YYYY-MM-DD)")
    is_all_day: bool = Field(False, description="Indica si es un evento de todo el día")
    color_id: Optional[str] = Field(None, description="ID de color de Google Calendar (1-11)")
    attendees: Optional[List[str]] = Field(default_factory=list, description="Lista de correos de invitados")


class CalendarEventUpdateRequest(BaseModel):
    """Request para actualizar un evento existente en Google Calendar."""
    summary: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    is_all_day: Optional[bool] = None
    color_id: Optional[str] = None
    attendees: Optional[List[str]] = None


class CalendarQuickAddRequest(BaseModel):
    """Request para creación rápida en lenguaje natural (ej. 'Junta mañana a las 3pm')."""
    text: str = Field(..., min_length=2, max_length=500, description="Texto descriptivo para el quickAdd de Google Calendar")
