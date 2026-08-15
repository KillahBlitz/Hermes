from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────
# ÉPICAS
# ─────────────────────────────────────────────────────────────

class EpicCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=60, description="Nombre de la épica")
    description: Optional[str] = Field(None, max_length=300, description="Descripción opcional")
    color: str = Field("#00E5FF", description="Color neón identificador")
    icon: str = Field("💼", description="Emoji o icono de la épica")


class EpicUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=60)
    description: Optional[str] = Field(None, max_length=300)
    color: Optional[str] = None
    icon: Optional[str] = None


# ─────────────────────────────────────────────────────────────
# TAREAS
# ─────────────────────────────────────────────────────────────

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=140, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=2000, description="Descripción detallada o notas")
    type: str = Field("IMPROVEMENT", pattern="^(IMPROVEMENT|URGENT|PENDING|ANALYSIS)$", description="Tipo de tarea")
    complexity: str = Field("M", pattern="^(XS|S|M|L|XL)$", description="Nivel de complejidad")
    epic_id: Optional[str] = Field(None, description="ID de la épica vinculada")
    status: str = Field("TODO", pattern="^(TODO|IN_PROGRESS|TESTING|DONE)$", description="Columna/estado inicial")
    location: str = Field("BOARD", pattern="^(BOARD|BACKLOG)$", description="Ubicación inicial: Tablero o Backlog")
    due_date: Optional[datetime] = Field(None, description="Fecha límite de entrega opcional")


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=140)
    description: Optional[str] = Field(None, max_length=2000)
    type: Optional[str] = Field(None, pattern="^(IMPROVEMENT|URGENT|PENDING|ANALYSIS)$")
    complexity: Optional[str] = Field(None, pattern="^(XS|S|M|L|XL)$")
    epic_id: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(TODO|IN_PROGRESS|TESTING|DONE)$")
    location: Optional[str] = Field(None, pattern="^(BOARD|BACKLOG)$")
    due_date: Optional[datetime] = None


class TaskStatusUpdateRequest(BaseModel):
    status: str = Field(..., pattern="^(TODO|IN_PROGRESS|TESTING|DONE)$", description="Nuevo estado/columna")


class TaskLocationUpdateRequest(BaseModel):
    location: str = Field(..., pattern="^(BOARD|BACKLOG)$", description="Nueva ubicación: BOARD o BACKLOG")


# ─────────────────────────────────────────────────────────────
# HÁBITOS (21 DÍAS)
# ─────────────────────────────────────────────────────────────

class HabitCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Nombre del hábito a desarrollar")
    description: Optional[str] = Field(None, max_length=400, description="Motivación o notas del hábito")
    icon: str = Field("⚡", description="Emoji identificador del hábito")
    color: str = Field("#00FFC6", description="Color neón del hábito")


class HabitUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=400)
    icon: Optional[str] = None
    color: Optional[str] = None


class HabitCheckDayRequest(BaseModel):
    day_number: int = Field(..., ge=1, le=21, description="Número de día del 1 al 21")
    status: str = Field(..., pattern="^(COMPLETED|FAILED|PENDING)$", description="Estado del día")


# ─────────────────────────────────────────────────────────────
# PIZARRÓN DE IDEAS (STICKY NOTES)
# ─────────────────────────────────────────────────────────────

class StickyNoteCreateRequest(BaseModel):
    title: Optional[str] = Field("", max_length=80, description="Título breve opcional")
    content: str = Field(..., min_length=1, max_length=1000, description="Contenido de la idea")
    color: str = Field("#FFD166", description="Color neón de la nota")
    x: float = Field(120.0, description="Posición horizontal en el canvas")
    y: float = Field(120.0, description="Posición vertical en el canvas")


class StickyNoteUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, max_length=80)
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    color: Optional[str] = None


class StickyNotePositionRequest(BaseModel):
    x: float = Field(..., description="Nueva coordenada X")
    y: float = Field(..., description="Nueva coordenada Y")
    z_index: Optional[int] = Field(1, ge=1, le=9999, description="Capa de profundidad")
