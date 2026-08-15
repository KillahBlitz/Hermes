from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────
# ÉPICAS
# ─────────────────────────────────────────────────────────────

class EpicResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    color: str
    icon: str
    is_default: bool = False
    created_at: Optional[datetime] = None
    task_count: int = 0


class EpicListResponse(BaseModel):
    epics: List[EpicResponse]
    total: int


# ─────────────────────────────────────────────────────────────
# TAREAS
# ─────────────────────────────────────────────────────────────

class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    type: str
    complexity: str
    epic_id: Optional[str] = None
    epic: Optional[EpicResponse] = None
    status: str
    location: str
    order: int = 0
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    days_since_completion: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int


class KanbanBoardResponse(BaseModel):
    todo: List[TaskResponse]
    in_progress: List[TaskResponse]
    testing: List[TaskResponse]
    done: List[TaskResponse]
    total_active: int
    archived_count: int


# ─────────────────────────────────────────────────────────────
# HÁBITOS (21 DÍAS)
# ─────────────────────────────────────────────────────────────

class HabitDayInfo(BaseModel):
    day_number: int
    status: str
    date: Optional[str] = None


class HabitResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    icon: str
    color: str
    start_date: Optional[datetime] = None
    days: List[HabitDayInfo]
    current_streak: int = 0
    total_completed: int = 0
    completion_percentage: float = 0.0
    is_consolidated: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class HabitListResponse(BaseModel):
    habits: List[HabitResponse]
    total: int


# ─────────────────────────────────────────────────────────────
# PIZARRÓN DE IDEAS (STICKY NOTES)
# ─────────────────────────────────────────────────────────────

class StickyNoteResponse(BaseModel):
    id: str
    user_id: str
    title: Optional[str] = ""
    content: str
    color: str
    x: float
    y: float
    z_index: int = 1
    rotation: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StickyNoteListResponse(BaseModel):
    notes: List[StickyNoteResponse]
    total: int
