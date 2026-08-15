from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ── Gmail Models ──

class EmailAttachment(BaseModel):
    filename: str
    mime_type: str
    size: int = 0
    attachment_id: str


class EmailSummaryResponse(BaseModel):
    id: str
    thread_id: str
    sender: str
    sender_email: str
    subject: str
    snippet: str
    is_starred: bool = False
    is_important: bool = False
    date: str


class EmailListResponse(BaseModel):
    emails: List[EmailSummaryResponse]
    next_page_token: Optional[str] = None
    result_size_estimate: int = 0


class EmailDetailResponse(BaseModel):
    id: str
    thread_id: str
    sender: str
    sender_email: str
    recipients: str
    subject: str
    date: str
    body_html: Optional[str] = None
    body_text: Optional[str] = None
    labels: List[str] = []
    attachments: List[EmailAttachment] = []


# ── Google Drive Models ──

class DriveFileResponse(BaseModel):
    id: str
    name: str
    mime_type: str
    size: Optional[str] = None
    thumbnail_url: Optional[str] = None
    web_view_link: Optional[str] = None
    created_time: Optional[str] = None
    modified_time: Optional[str] = None
    is_folder: bool = False
    icon_link: Optional[str] = None


class DriveFileListResponse(BaseModel):
    files: List[DriveFileResponse]
    current_folder_id: str
    current_folder_name: str = "hermes"


class DriveBucketResponse(BaseModel):
    root_id: str
    root_name: str = "hermes"
    multimedia_id: str
    archivos_id: str
    folders: List[DriveFileResponse] = []


class DrivePreviewResponse(BaseModel):
    file_id: str
    file_name: str
    mime_type: str
    web_view_link: Optional[str] = None
    web_content_link: Optional[str] = None
    thumbnail_link: Optional[str] = None
    size: Optional[str] = None


class FolderCreatedResponse(BaseModel):
    id: str
    name: str
    parent_id: str


class FileUploadResponse(BaseModel):
    id: str
    name: str
    mime_type: str
    size: Optional[str] = None
    folder_id: str


# ── Google Calendar Models ──

class CalendarEventResponse(BaseModel):
    id: str
    summary: str
    description: Optional[str] = None
    location: Optional[str] = None
    start: str
    end: str
    is_all_day: bool = False
    html_link: Optional[str] = None
    status: str = "confirmed"
    color_id: Optional[str] = None
    attendees: List[str] = []
    created: Optional[str] = None
    updated: Optional[str] = None


class CalendarEventListResponse(BaseModel):
    events: List[CalendarEventResponse]
    total: int = 0
    time_min: Optional[str] = None
    time_max: Optional[str] = None


# ── Audit Models ──

class AuditLogResponse(BaseModel):
    id: str
    service: str
    action: str
    resource_id: str
    resource_title: str
    timestamp: datetime
    status: str
    details: Optional[dict] = None


class AuditLogListResponse(BaseModel):
    logs: List[AuditLogResponse]
    total: int = 0


# ── Generic ──

class ServiceActionResponse(BaseModel):
    success: bool
    message: str
