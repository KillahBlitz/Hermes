import logging
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from src.models.request.progress import (
    MilestoneCreateRequest,
    MilestoneTopicToggleRequest,
    MilestoneUpdateRequest,
    NoteCreateRequest,
    NoteUpdateRequest,
    RoadmapCreateRequest,
    RoadmapUpdateRequest,
)
from src.models.response.progress import (
    KnowledgeGraphResponse,
    MilestoneListResponse,
    MilestoneResponse,
    NoteListResponse,
    NoteResponse,
    RoadmapListResponse,
    RoadmapResponse,
)
from src.services.progress_service import progress_service
from src.utils.jwt import get_current_user_payload

logger = logging.getLogger("hermes-api.progress")
router = APIRouter(prefix="/progress", tags=["Progreso & Conocimiento"])


# ═══════════════════════════════════════════════════════════════
#  1. ÁRBOL DE MAPAS (ROADMAPS)
# ═══════════════════════════════════════════════════════════════

@router.get("/roadmaps", response_model=RoadmapListResponse)
async def get_roadmaps(payload: Dict[str, Any] = Depends(get_current_user_payload)):
    """Obtiene la lista de mapas de ruta del usuario."""
    user_id = payload.get("sub")
    return await progress_service.list_roadmaps(user_id=user_id)


@router.post("/roadmaps", response_model=RoadmapResponse, status_code=status.HTTP_201_CREATED)
async def create_roadmap(
    req: RoadmapCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Crea un nuevo árbol de mapas."""
    user_id = payload.get("sub")
    return await progress_service.create_roadmap(user_id=user_id, req=req)


@router.get("/roadmaps/{roadmap_id}", response_model=RoadmapResponse)
async def get_roadmap(
    roadmap_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Obtiene el detalle completo de un roadmap con sus nodos y conexiones."""
    user_id = payload.get("sub")
    roadmap = await progress_service.get_roadmap(user_id=user_id, roadmap_id=roadmap_id)
    if not roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap no encontrado")
    return roadmap


@router.put("/roadmaps/{roadmap_id}", response_model=RoadmapResponse)
async def update_roadmap(
    roadmap_id: str,
    req: RoadmapUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza la estructura, nodos o conexiones de un roadmap."""
    user_id = payload.get("sub")
    updated = await progress_service.update_roadmap(user_id=user_id, roadmap_id=roadmap_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap no encontrado")
    return updated


@router.delete("/roadmaps/{roadmap_id}")
async def delete_roadmap(
    roadmap_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Elimina permanentemente un roadmap."""
    user_id = payload.get("sub")
    success = await progress_service.delete_roadmap(user_id=user_id, roadmap_id=roadmap_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap no encontrado")
    return {"message": "Roadmap eliminado exitosamente"}


# ═══════════════════════════════════════════════════════════════
#  2. GESTOR DE HITOS (MILESTONES TRACKER)
# ═══════════════════════════════════════════════════════════════

@router.get("/milestones", response_model=MilestoneListResponse)
async def get_milestones(
    category: Optional[str] = Query(None, description="Filtrar por categoría (TITULACION, CERTIFICACION, EXAMEN, PROYECTO, CARRERA)"),
    status: Optional[str] = Query(None, description="Filtrar por estado (IN_PROGRESS, COMPLETED, ARCHIVED)"),
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Obtiene los hitos de gran escala con cálculos de cuenta regresiva y porcentaje."""
    user_id = payload.get("sub")
    return await progress_service.list_milestones(user_id=user_id, category=category, status=status)


@router.post("/milestones", response_model=MilestoneResponse, status_code=status.HTTP_201_CREATED)
async def create_milestone(
    req: MilestoneCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Registra un nuevo proyecto macro o hito con fecha meta y temario."""
    user_id = payload.get("sub")
    return await progress_service.create_milestone(user_id=user_id, req=req)


@router.put("/milestones/{milestone_id}", response_model=MilestoneResponse)
async def update_milestone(
    milestone_id: str,
    req: MilestoneUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza datos, fecha meta o temario de un hito."""
    user_id = payload.get("sub")
    updated = await progress_service.update_milestone(user_id=user_id, milestone_id=milestone_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hito no encontrado")
    return updated


@router.patch("/milestones/{milestone_id}/topics/{topic_id}/toggle", response_model=MilestoneResponse)
async def toggle_milestone_topic(
    milestone_id: str,
    topic_id: str,
    req: MilestoneTopicToggleRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Conmuta el estado de completado de un tema dentro del temario del hito."""
    user_id = payload.get("sub")
    updated = await progress_service.toggle_milestone_topic(
        user_id=user_id,
        milestone_id=milestone_id,
        topic_id=topic_id,
        req=req
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hito o tema no encontrado")
    return updated


@router.delete("/milestones/{milestone_id}")
async def delete_milestone(
    milestone_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Elimina permanentemente un hito."""
    user_id = payload.get("sub")
    success = await progress_service.delete_milestone(user_id=user_id, milestone_id=milestone_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hito no encontrado")
    return {"message": "Hito eliminado exitosamente"}


# ═══════════════════════════════════════════════════════════════
#  3. BÓVEDA ZETTELKASTEN & GRAFO DE CONOCIMIENTO
# ═══════════════════════════════════════════════════════════════

@router.get("/notes", response_model=NoteListResponse)
async def get_notes(
    search: Optional[str] = Query(None, description="Búsqueda por título o contenido"),
    tag: Optional[str] = Query(None, description="Filtrar por etiqueta #tag"),
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Obtiene la lista de notas de la bóveda Zettelkasten con backlinks."""
    user_id = payload.get("sub")
    return await progress_service.list_notes(user_id=user_id, search=search, tag=tag)


@router.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    req: NoteCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Crea una nota Markdown e indexa automáticamente wikilinks y hashtags."""
    user_id = payload.get("sub")
    return await progress_service.create_note(user_id=user_id, req=req)


@router.get("/notes/{note_id_or_title}", response_model=NoteResponse)
async def get_note(
    note_id_or_title: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Obtiene una nota por ID, título o slug con sus backlinks activos."""
    user_id = payload.get("sub")
    note = await progress_service.get_note(user_id=user_id, note_id_or_title=note_id_or_title)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota no encontrada")
    return note


@router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    req: NoteUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza el contenido Markdown y reindexa wikilinks y etiquetas."""
    user_id = payload.get("sub")
    updated = await progress_service.update_note(user_id=user_id, note_id=note_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota no encontrada")
    return updated


@router.delete("/notes/{note_id}")
async def delete_note(
    note_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Elimina permanentemente una nota de la bóveda."""
    user_id = payload.get("sub")
    success = await progress_service.delete_note(user_id=user_id, note_id=note_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota no encontrada")
    return {"message": "Nota eliminada exitosamente"}


@router.get("/graph", response_model=KnowledgeGraphResponse)
async def get_knowledge_graph(payload: Dict[str, Any] = Depends(get_current_user_payload)):
    """Genera la estructura de nodos y aristas de la red Zettelkasten para visualización 2D."""
    user_id = payload.get("sub")
    return await progress_service.get_knowledge_graph(user_id=user_id)
