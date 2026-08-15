import json
import logging
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from googleapiclient.errors import HttpError
from src.database.mongo import get_credentials_collection
from src.models.request.lists import (
    TodoSectionCreateRequest,
    TodoSectionUpdateRequest,
    TodoTaskCreateRequest,
    TodoTaskToggleRequest,
    TodoTaskUpdateRequest,
    WishlistItemCreateRequest,
    WishlistItemStatusRequest,
    WishlistItemUpdateRequest,
)
from src.models.response.lists import (
    TodoSectionListResponse,
    TodoSectionResponse,
    TodoTaskListResponse,
    TodoTaskResponse,
    WishlistItemResponse,
    WishlistListResponse,
)
from src.services.lists_service import lists_service
from src.utils.crypto import decrypt_token
from src.utils.jwt import get_current_user_payload

logger = logging.getLogger("hermes-api.lists")
router = APIRouter(prefix="/lists", tags=["Lists & Wishlist"])


def _handle_google_error(e: Exception, service_name: str = "Google"):
    logger.error(f"Error en {service_name}: {e}")
    if isinstance(e, HttpError):
        status_code = e.resp.status
        try:
            error_details = json.loads(e.content.decode("utf-8"))
            error_msg = error_details.get("error", {}).get("message", str(e))
        except Exception:
            error_msg = str(e)

        if status_code == 403:
            if "has not been used in project" in error_msg or "disabled" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        f"La API de {service_name} no está habilitada en la consola de Google Cloud de tu proyecto de Firebase. "
                        f"Por favor ve a Google Cloud Console (https://console.cloud.google.com/apis/library) "
                        f"y habilita '{service_name} API'. Detalle técnico: {error_msg}"
                    ),
                )
            elif "insufficientPermissions" in error_msg or "Insufficient Permission" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        f"Permisos insuficientes para {service_name}. "
                        "Cierra sesión en la plataforma e inicia sesión nuevamente con Google para conceder los permisos solicitados."
                    ),
                )
        elif status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tu token de acceso de Google ha expirado. Por favor cierra sesión y vuelve a iniciar sesión con Google.",
            )
        raise HTTPException(
            status_code=status_code,
            detail=f"Error de {service_name} ({status_code}): {error_msg}",
        )
    elif isinstance(e, HTTPException):
        raise e
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error inesperado al conectar con {service_name}: {str(e)}",
    )


async def _get_user_access_token(user_id: str) -> str:
    """Retrieve and decrypt the Google access token for a user from MongoDB."""
    credentials_col = get_credentials_collection()
    if credentials_col is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos no disponible.",
        )

    cred_doc = await credentials_col.find_one({"_id": user_id})
    if not cred_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron credenciales de Google para este usuario. Inicia sesión nuevamente.",
        )

    encrypted_token = cred_doc.get("google_access_token_encrypted")
    if not encrypted_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token de acceso de Google no encontrado. Inicia sesión nuevamente.",
        )

    token = decrypt_token(encrypted_token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al descifrar el token de acceso de Google.",
        )
    return token


# ═══════════════════════════════════════════════════════════════
#  LISTA DE DESEOS (WISHLIST)
# ═══════════════════════════════════════════════════════════════

@router.get("/wishlist", response_model=WishlistListResponse)
async def get_wishlist(
    status: Optional[str] = Query(None, description="Filtrar por estado (PENDING, PURCHASED, ARCHIVED)"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    priority: Optional[str] = Query(None, description="Filtrar por prioridad (ALTA, MEDIA, BAJA)"),
    search: Optional[str] = Query(None, description="Buscar por nombre"),
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Obtiene la lista de deseos con estadísticas de inversión y filtros."""
    user_id = payload.get("sub")
    return await lists_service.list_wishlist(
        user_id=user_id,
        status_filter=status,
        category=category,
        priority=priority,
        search=search
    )


@router.post("/wishlist", response_model=WishlistItemResponse, status_code=status.HTTP_201_CREATED)
async def create_wishlist_item(
    req: WishlistItemCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Registra un nuevo artículo en la lista de deseos."""
    user_id = payload.get("sub")
    return await lists_service.create_wishlist_item(user_id=user_id, req=req)


@router.put("/wishlist/{item_id}", response_model=WishlistItemResponse)
async def update_wishlist_item(
    item_id: str,
    req: WishlistItemUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza los datos de un artículo de la lista de deseos."""
    user_id = payload.get("sub")
    updated = await lists_service.update_wishlist_item(user_id=user_id, item_id=item_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado")
    return updated


@router.patch("/wishlist/{item_id}/status", response_model=WishlistItemResponse)
async def update_wishlist_status(
    item_id: str,
    req: WishlistItemStatusRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Cambia el estado de un deseo (PENDING, PURCHASED, ARCHIVED)."""
    user_id = payload.get("sub")
    updated = await lists_service.update_wishlist_status(user_id=user_id, item_id=item_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado")
    return updated


@router.post("/wishlist/{item_id}/upload-photo", response_model=WishlistItemResponse)
async def upload_wishlist_photo(
    item_id: str,
    file: UploadFile = File(...),
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Sube una foto del artículo directamente a Google Drive en la carpeta 'hermes/whitelist'."""
    user_id = payload.get("sub")
    access_token = await _get_user_access_token(user_id)
    content = await file.read()
    try:
        updated = await lists_service.upload_wishlist_photo(
            user_id=user_id,
            item_id=item_id,
            access_token=access_token,
            file_content=content,
            filename=file.filename or "foto_deseo.jpg",
            mime_type=file.content_type or "image/jpeg"
        )
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado")
        return updated
    except Exception as e:
        _handle_google_error(e, "Google Drive")


@router.delete("/wishlist/{item_id}")
async def delete_wishlist_item(
    item_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Elimina permanentemente un artículo de la lista de deseos."""
    user_id = payload.get("sub")
    success = await lists_service.delete_wishlist_item(user_id=user_id, item_id=item_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado")
    return {"message": "Artículo eliminado exitosamente"}


# ═══════════════════════════════════════════════════════════════
#  LISTA DE TAREAS & SECCIONES (MICROSOFT TO-DO STYLE)
# ═══════════════════════════════════════════════════════════════

@router.get("/todo/sections", response_model=TodoSectionListResponse)
async def get_todo_sections(payload: Dict[str, Any] = Depends(get_current_user_payload)):
    """Obtiene las secciones/categorías de tareas con contador de pendientes."""
    user_id = payload.get("sub")
    sections = await lists_service.list_sections(user_id=user_id)
    return TodoSectionListResponse(sections=sections, total=len(sections))


@router.post("/todo/sections", response_model=TodoSectionResponse, status_code=status.HTTP_201_CREATED)
async def create_todo_section(
    req: TodoSectionCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Crea una nueva sección temática para clasificar tareas."""
    user_id = payload.get("sub")
    return await lists_service.create_section(user_id=user_id, req=req)


@router.put("/todo/sections/{section_id}", response_model=TodoSectionResponse)
async def update_todo_section(
    section_id: str,
    req: TodoSectionUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza el nombre, icono o color de una sección."""
    user_id = payload.get("sub")
    updated = await lists_service.update_section(user_id=user_id, section_id=section_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sección no encontrada")
    return updated


@router.delete("/todo/sections/{section_id}")
async def delete_todo_section(
    section_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Elimina una sección de tareas."""
    user_id = payload.get("sub")
    success = await lists_service.delete_section(user_id=user_id, section_id=section_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sección no encontrada")
    return {"message": "Sección eliminada exitosamente"}


@router.get("/todo/tasks", response_model=TodoTaskListResponse)
async def get_todo_tasks(
    section_id: Optional[str] = Query(None, description="Filtrar por sección"),
    completed: Optional[bool] = Query(None, description="Filtrar por estado completado (true/false)"),
    search: Optional[str] = Query(None, description="Buscar en el título"),
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Obtiene el listado de tareas To-Do."""
    user_id = payload.get("sub")
    return await lists_service.list_todo_tasks(
        user_id=user_id,
        section_id=section_id,
        is_completed=completed,
        search=search
    )


@router.post("/todo/tasks", response_model=TodoTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_todo_task(
    req: TodoTaskCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Crea una tarea rápida To-Do."""
    user_id = payload.get("sub")
    return await lists_service.create_todo_task(user_id=user_id, req=req)


@router.put("/todo/tasks/{task_id}", response_model=TodoTaskResponse)
async def update_todo_task(
    task_id: str,
    req: TodoTaskUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Actualiza los datos de una tarea To-Do."""
    user_id = payload.get("sub")
    updated = await lists_service.update_todo_task(user_id=user_id, task_id=task_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return updated


@router.patch("/todo/tasks/{task_id}/toggle", response_model=TodoTaskResponse)
async def toggle_todo_task(
    task_id: str,
    req: TodoTaskToggleRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Conmuta inmediatamente el estado de completado de la tarea."""
    user_id = payload.get("sub")
    updated = await lists_service.toggle_todo_task(user_id=user_id, task_id=task_id, req=req)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return updated


@router.delete("/todo/tasks/{task_id}")
async def delete_todo_task(
    task_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload)
):
    """Elimina permanentemente una tarea To-Do."""
    user_id = payload.get("sub")
    success = await lists_service.delete_todo_task(user_id=user_id, task_id=task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada exitosamente"}
