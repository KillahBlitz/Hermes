from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────
# LISTA DE DESEOS (WISHLIST)
# ─────────────────────────────────────────────────────────────

class WishlistImageResponse(BaseModel):
    drive_file_id: str
    name: str
    mime_type: str
    size: int = 0
    thumbnail_link: Optional[str] = None
    web_view_link: Optional[str] = None


class WishlistItemResponse(BaseModel):
    id: str
    user_id: str
    name: str
    price: float
    currency: str = "MXN"
    category: str = "General"
    priority: str = "MEDIA"
    description: Optional[str] = None
    url: Optional[str] = None
    images: List[WishlistImageResponse] = []
    status: str = "PENDING"
    purchased_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WishlistStatsResponse(BaseModel):
    total_items: int = 0
    pending_items: int = 0
    purchased_items: int = 0
    total_pending_value: float = 0.0
    total_purchased_value: float = 0.0
    currency: str = "MXN"


class WishlistListResponse(BaseModel):
    items: List[WishlistItemResponse]
    stats: WishlistStatsResponse
    total: int


# ─────────────────────────────────────────────────────────────
# LISTA DE TAREAS (MICROSOFT TO-DO STYLE)
# ─────────────────────────────────────────────────────────────

class TodoSectionResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    name: str
    icon: str
    color: str
    is_default: bool = False
    order: int = 0
    pending_count: int = 0
    completed_count: int = 0
    created_at: Optional[datetime] = None


class TodoSectionListResponse(BaseModel):
    sections: List[TodoSectionResponse]
    total: int


class TodoTaskResponse(BaseModel):
    id: str
    user_id: str
    section_id: Optional[str] = None
    section: Optional[TodoSectionResponse] = None
    title: str
    difficulty_points: int = 1
    repeat: str = "NONE"
    due_date: Optional[datetime] = None
    notes: Optional[str] = None
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TodoTaskListResponse(BaseModel):
    tasks: List[TodoTaskResponse]
    total: int
    pending_count: int = 0
    completed_count: int = 0
