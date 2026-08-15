from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────
# 1. ÁRBOL DE MAPAS (ROADMAPS)
# ─────────────────────────────────────────────────────────────

class RoadmapNodeResponse(BaseModel):
    id: str
    title: str
    icon: str = "⚡"
    color: str = "#00E5FF"
    status: str = "PENDIENTE"
    x: float = 100.0
    y: float = 100.0
    description: Optional[str] = None
    note_id: Optional[str] = None
    note_title: Optional[str] = None


class RoadmapEdgeResponse(BaseModel):
    id: str
    source_node_id: str
    target_node_id: str
    label: Optional[str] = None


class RoadmapResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    category: str = "General"
    color: str = "#00FFC6"
    nodes: List[RoadmapNodeResponse] = []
    edges: List[RoadmapEdgeResponse] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RoadmapListResponse(BaseModel):
    roadmaps: List[RoadmapResponse]
    total: int


# ─────────────────────────────────────────────────────────────
# 2. GESTOR DE HITOS (MILESTONES TRACKER)
# ─────────────────────────────────────────────────────────────

class MilestoneTopicResponse(BaseModel):
    id: str
    title: str
    is_completed: bool = False
    completed_at: Optional[datetime] = None


class MilestoneResponse(BaseModel):
    id: str
    user_id: str
    title: str
    category: str
    icon: str = "🎯"
    color: str = "#00FFC6"
    target_date: datetime
    description: Optional[str] = None
    topics: List[MilestoneTopicResponse] = []
    total_topics: int = 0
    completed_topics: int = 0
    progress_percentage: float = 0.0
    days_remaining: int = 0
    is_overdue: bool = False
    status: str = "IN_PROGRESS"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MilestoneListResponse(BaseModel):
    milestones: List[MilestoneResponse]
    total: int
    active_count: int = 0
    completed_count: int = 0


# ─────────────────────────────────────────────────────────────
# 3. BÓVEDA ZETTELKASTEN (MARKDOWN NOTES & WIKILINKS & GRAPH)
# ─────────────────────────────────────────────────────────────

class BacklinkItemResponse(BaseModel):
    id: str
    title: str
    slug: str


class NoteResponse(BaseModel):
    id: str
    user_id: str
    title: str
    slug: str
    content_md: str
    tags: List[str] = []
    outgoing_links: List[str] = []
    backlinks: List[BacklinkItemResponse] = []
    roadmap_node_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class NoteListResponse(BaseModel):
    notes: List[NoteResponse]
    total: int


class GraphNodeResponse(BaseModel):
    id: str
    title: str
    tags: List[str] = []
    connections_count: int = 0
    group: str = "Nota"


class GraphEdgeResponse(BaseModel):
    source: str
    target: str


class KnowledgeGraphResponse(BaseModel):
    nodes: List[GraphNodeResponse]
    edges: List[GraphEdgeResponse]
    all_tags: List[str] = []
    total_notes: int = 0
    total_connections: int = 0
