from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────
# LISTA DE DESEOS (WISHLIST)
# ─────────────────────────────────────────────────────────────

class WishlistItemCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, description="Nombre del artículo deseado")
    price: float = Field(..., ge=0.0, description="Precio estimado del artículo")
    currency: str = Field("MXN", max_length=10, description="Moneda (ej. MXN, USD)")
    category: Optional[str] = Field("General", max_length=50, description="Categoría del artículo")
    priority: str = Field("MEDIA", pattern="^(ALTA|MEDIA|BAJA)$", description="Prioridad del deseo")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción o notas del producto")
    url: Optional[str] = Field(None, max_length=500, description="Enlace de compra externo (tienda online)")
    status: str = Field("PENDING", pattern="^(PENDING|PURCHASED|ARCHIVED)$", description="Estado del deseo")


class WishlistItemUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    price: Optional[float] = Field(None, ge=0.0)
    currency: Optional[str] = Field(None, max_length=10)
    category: Optional[str] = Field(None, max_length=50)
    priority: Optional[str] = Field(None, pattern="^(ALTA|MEDIA|BAJA)$")
    description: Optional[str] = Field(None, max_length=1000)
    url: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, pattern="^(PENDING|PURCHASED|ARCHIVED)$")


class WishlistItemStatusRequest(BaseModel):
    status: str = Field(..., pattern="^(PENDING|PURCHASED|ARCHIVED)$", description="Nuevo estado del artículo")


# ─────────────────────────────────────────────────────────────
# LISTA DE TAREAS (MICROSOFT TO-DO STYLE)
# ─────────────────────────────────────────────────────────────

class TodoSectionCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=60, description="Nombre de la sección/categoría")
    icon: str = Field("📋", description="Emoji o icono de la sección")
    color: str = Field("#00E5FF", description="Color identificador neón")


class TodoSectionUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=60)
    icon: Optional[str] = None
    color: Optional[str] = None


class TodoTaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=160, description="Título o descripción rápida de la tarea")
    section_id: Optional[str] = Field(None, description="ID de la sección asignada")
    difficulty_points: int = Field(1, description="Puntos de dificultad: 1, 2, 3 o 5")
    repeat: str = Field("NONE", pattern="^(NONE|DAILY|WEEKDAYS|WEEKLY|MONTHLY)$", description="Frecuencia de repetición")
    due_date: Optional[datetime] = Field(None, description="Fecha de vencimiento")
    notes: Optional[str] = Field(None, max_length=1000, description="Notas o sub-pasos adicionales")


class TodoTaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=160)
    section_id: Optional[str] = None
    difficulty_points: Optional[int] = None
    repeat: Optional[str] = Field(None, pattern="^(NONE|DAILY|WEEKDAYS|WEEKLY|MONTHLY)$")
    due_date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=1000)
    is_completed: Optional[bool] = None


class TodoTaskToggleRequest(BaseModel):
    is_completed: bool = Field(..., description="Estado completado (true/false)")
