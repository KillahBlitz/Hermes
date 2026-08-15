from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────
# 1. ÁRBOL DE MAPAS (ROADMAPS)
# ─────────────────────────────────────────────────────────────

class RoadmapNodeRequest(BaseModel):
    id: str = Field(..., description="ID único del nodo en el canvas")
    title: str = Field(..., min_length=1, max_length=120, description="Título del nodo/módulo")
    icon: str = Field("⚡", description="Emoji o icono identificador")
    color: str = Field("#00E5FF", description="Color de acento neón")
    status: str = Field("PENDIENTE", pattern="^(PENDIENTE|EN_CURSO|DOMINADO)$", description="Estado de avance")
    x: float = Field(100.0, description="Coordenada X en el canvas")
    y: float = Field(100.0, description="Coordenada Y en el canvas")
    description: Optional[str] = Field(None, max_length=500, description="Descripción corta")
    note_id: Optional[str] = Field(None, description="ID de la nota Markdown asociada")


class RoadmapEdgeRequest(BaseModel):
    id: str = Field(..., description="ID único de la arista")
    source_node_id: str = Field(..., description="ID del nodo de origen")
    target_node_id: str = Field(..., description="ID del nodo de destino")
    label: Optional[str] = Field(None, max_length=60, description="Etiqueta opcional de la conexión")


class RoadmapCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=120, description="Título del mapa de ruta")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción o meta del roadmap")
    category: str = Field("General", max_length=60, description="Categoría temática")
    color: str = Field("#00FFC6", description="Color representativo")
    nodes: List[RoadmapNodeRequest] = Field(default_factory=list)
    edges: List[RoadmapEdgeRequest] = Field(default_factory=list)


class RoadmapUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, max_length=60)
    color: Optional[str] = None
    nodes: Optional[List[RoadmapNodeRequest]] = None
    edges: Optional[List[RoadmapEdgeRequest]] = None


# ─────────────────────────────────────────────────────────────
# 2. GESTOR DE HITOS (MILESTONES TRACKER)
# ─────────────────────────────────────────────────────────────

class MilestoneTopicRequest(BaseModel):
    id: str = Field(..., description="ID único del tópico dentro del temario")
    title: str = Field(..., min_length=1, max_length=200, description="Título del tema o entregable")
    is_completed: bool = Field(False, description="Estado completado")
    completed_at: Optional[datetime] = None


class MilestoneCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=150, description="Título del hito o proyecto macro")
    category: str = Field("PROYECTO", description="Categoría (TITULACION, CERTIFICACION, EXAMEN, PROYECTO, CARRERA)")
    icon: str = Field("🎯", description="Emoji identificador")
    color: str = Field("#00FFC6", description="Color de acento neón")
    target_date: datetime = Field(..., description="Fecha límite / deadline del hito")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción o alcance")
    topics: List[MilestoneTopicRequest] = Field(default_factory=list)


class MilestoneUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    category: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    target_date: Optional[datetime] = None
    description: Optional[str] = None
    topics: Optional[List[MilestoneTopicRequest]] = None
    status: Optional[str] = Field(None, pattern="^(IN_PROGRESS|COMPLETED|ARCHIVED)$")


class MilestoneTopicToggleRequest(BaseModel):
    is_completed: bool = Field(..., description="Nuevo estado del tema")


# ─────────────────────────────────────────────────────────────
# 3. BÓVEDA ZETTELKASTEN (MARKDOWN NOTES & WIKILINKS)
# ─────────────────────────────────────────────────────────────

class NoteCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=150, description="Título de la nota Zettelkasten")
    content_md: str = Field(..., description="Contenido en Markdown con soporte para [[wikilinks]] y #tags")
    tags: Optional[List[str]] = Field(default_factory=list, description="Etiquetas opcionales")
    roadmap_node_id: Optional[str] = Field(None, description="ID del nodo del roadmap vinculado")


class NoteUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    content_md: Optional[str] = None
    tags: Optional[List[str]] = None
