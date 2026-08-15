import logging
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from src.models.request.boards import (
    EpicCreateRequest,
    EpicUpdateRequest,
    HabitCheckDayRequest,
    HabitCreateRequest,
    HabitUpdateRequest,
    StickyNoteCreateRequest,
    StickyNotePositionRequest,
    StickyNoteUpdateRequest,
    TaskCreateRequest,
    TaskLocationUpdateRequest,
    TaskStatusUpdateRequest,
    TaskUpdateRequest,
)
from src.models.response.boards import (
    EpicListResponse,
    EpicResponse,
    HabitListResponse,
    HabitResponse,
    KanbanBoardResponse,
    StickyNoteListResponse,
    StickyNoteResponse,
    TaskListResponse,
    TaskResponse,
)
from src.services.board_service import board_service
from src.utils.jwt import get_current_user_payload

logger = logging.getLogger("hermes-api.boards")
router = APIRouter(prefix="/boards", tags=["Boards & Productivity"])


# ═══════════════════════════════════════════════════════════════
#  ÉPICAS ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/epics", response_model=EpicListResponse)
async def get_epics(payload: Dict[str, Any] = Depends(get_current_user_payload)):
    """Obtiene las épicas disponibles del usuario (Escuela, Trabajo, Cursos, personalizadas)."""
    user_id = payload.get("sub")
    epics = await board_service.list_epics(user_id=user_id)
    return EpicListResponse(epics=epics, total=len(epics))


@router.post("/epics", response_model=EpicResponse, status_code=status.HTTP_201_CREATED)
async def create_epic(
    req: EpicCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Crea una nueva épica de trabajo."""
    user_id = payload.get("sub")
    return await board_service.create_epic(user_id=user_id, req=req)


@router.put("/epics/{epic_id}", response_model=EpicResponse)
async def update_epic(
    epic_id: str,
    req: EpicUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza los datos de una épica."""
    user_id = payload.get("sub")
    updated = await board_service.update_epic(user_id=user_id, epic_id=epic_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Épica no encontrada")
    return updated


@router.delete("/epics/{epic_id}")
async def delete_epic(
    epic_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Elimina una épica y desvincula las tareas asociadas."""
    user_id = payload.get("sub")
    success = await board_service.delete_epic(user_id=user_id, epic_id=epic_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Épica no encontrada")
    return {"message": "Épica eliminada exitosamente"}


# ═══════════════════════════════════════════════════════════════
#  TAREAS & TABLERO KANBAN ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/tasks/kanban", response_model=KanbanBoardResponse)
async def get_kanban_board(
    epic_id: Optional[str] = Query(None, description="Filtrar por ID de épica"),
    type: Optional[str] = Query(None, description="Filtrar por tipo (IMPROVEMENT, URGENT, PENDING, ANALYSIS)"),
    search: Optional[str] = Query(None, description="Buscar en el título"),
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Obtiene el tablero Kanban de 4 columnas (ToDo, In Progress, To Be Tested, Done < 7 días)."""
    user_id = payload.get("sub")
    return await board_service.get_kanban_board(
        user_id=user_id,
        epic_id=epic_id,
        type_filter=type,
        search=search
    )


@router.get("/tasks/backlog", response_model=TaskListResponse)
async def get_backlog_tasks(
    epic_id: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Obtiene las tareas en la cola de Backlog."""
    user_id = payload.get("sub")
    return await board_service.get_backlog_tasks(
        user_id=user_id,
        epic_id=epic_id,
        type_filter=type,
        search=search
    )


@router.get("/tasks/archived", response_model=TaskListResponse)
async def get_archived_tasks(
    epic_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Obtiene las tareas completadas hace más de 7 días."""
    user_id = payload.get("sub")
    return await board_service.get_archived_tasks(
        user_id=user_id,
        epic_id=epic_id,
        search=search
    )


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    req: TaskCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Crea una nueva tarea (en Tablero o Backlog)."""
    user_id = payload.get("sub")
    return await board_service.create_task(user_id=user_id, req=req)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    req: TaskUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza una tarea existente."""
    user_id = payload.get("sub")
    updated = await board_service.update_task(user_id=user_id, task_id=task_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return updated


@router.patch("/tasks/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: str,
    req: TaskStatusUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Mueve la tarea de columna/estado (TODO, IN_PROGRESS, TESTING, DONE)."""
    user_id = payload.get("sub")
    updated = await board_service.update_task_status(user_id=user_id, task_id=task_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return updated


@router.patch("/tasks/{task_id}/location", response_model=TaskResponse)
async def update_task_location(
    task_id: str,
    req: TaskLocationUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Mueve la tarea entre Tablero ('BOARD') y Backlog ('BACKLOG')."""
    user_id = payload.get("sub")
    updated = await board_service.update_task_location(user_id=user_id, task_id=task_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return updated


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Elimina permanentemente una tarea."""
    user_id = payload.get("sub")
    success = await board_service.delete_task(user_id=user_id, task_id=task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada exitosamente"}


# ═══════════════════════════════════════════════════════════════
#  HÁBITOS (21 DÍAS) ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/habits", response_model=HabitListResponse)
async def get_habits(payload: Dict[str, Any] = Depends(get_current_user_payload)):
    """Obtiene los hábitos registrados del usuario con su matriz de 21 días."""
    user_id = payload.get("sub")
    habits = await board_service.list_habits(user_id=user_id)
    return HabitListResponse(habits=habits, total=len(habits))


@router.post("/habits", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
async def create_habit(
    req: HabitCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Crea un nuevo hábito e inicializa sus 21 casillas."""
    user_id = payload.get("sub")
    return await board_service.create_habit(user_id=user_id, req=req)


@router.put("/habits/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: str,
    req: HabitUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza datos del hábito."""
    user_id = payload.get("sub")
    updated = await board_service.update_habit(user_id=user_id, habit_id=habit_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hábito no encontrado")
    return updated


@router.patch("/habits/{habit_id}/check-day", response_model=HabitResponse)
async def check_habit_day(
    habit_id: str,
    req: HabitCheckDayRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Marca el estado de una casilla del 1 al 21 (COMPLETED, FAILED, PENDING)."""
    user_id = payload.get("sub")
    updated = await board_service.check_habit_day(user_id=user_id, habit_id=habit_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hábito no encontrado")
    return updated


@router.delete("/habits/{habit_id}")
async def delete_habit(
    habit_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Elimina un hábito."""
    user_id = payload.get("sub")
    success = await board_service.delete_habit(user_id=user_id, habit_id=habit_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hábito no encontrado")
    return {"message": "Hábito eliminado exitosamente"}


# ═══════════════════════════════════════════════════════════════
#  PIZARRÓN DE IDEAS (STICKY NOTES) ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/notes", response_model=StickyNoteListResponse)
async def get_sticky_notes(payload: Dict[str, Any] = Depends(get_current_user_payload)):
    """Obtiene todas las notas adhesivas del pizarrón con sus posiciones X/Y."""
    user_id = payload.get("sub")
    notes = await board_service.list_sticky_notes(user_id=user_id)
    return StickyNoteListResponse(notes=notes, total=len(notes))


@router.post("/notes", response_model=StickyNoteResponse, status_code=status.HTTP_201_CREATED)
async def create_sticky_note(
    req: StickyNoteCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Crea una nueva nota adhesiva en el pizarrón."""
    user_id = payload.get("sub")
    return await board_service.create_sticky_note(user_id=user_id, req=req)


@router.put("/notes/{note_id}", response_model=StickyNoteResponse)
async def update_sticky_note(
    note_id: str,
    req: StickyNoteUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza el texto, título o color de una nota adhesiva."""
    user_id = payload.get("sub")
    updated = await board_service.update_sticky_note(user_id=user_id, note_id=note_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota no encontrada")
    return updated


@router.patch("/notes/{note_id}/position", response_model=StickyNoteResponse)
async def update_sticky_note_position(
    note_id: str,
    req: StickyNotePositionRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza las coordenadas X, Y y capa z-index de una nota adhesiva tras ser arrastrada."""
    user_id = payload.get("sub")
    updated = await board_service.update_sticky_note_position(user_id=user_id, note_id=note_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota no encontrada")
    return updated


@router.delete("/notes/{note_id}")
async def delete_sticky_note(
    note_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Elimina una nota adhesiva del pizarrón."""
    user_id = payload.get("sub")
    success = await board_service.delete_sticky_note(user_id=user_id, note_id=note_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota no encontrada")
    return {"message": "Nota eliminada exitosamente"}
