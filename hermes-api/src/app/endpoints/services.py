import logging
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Response, UploadFile, status
from src.database.mongo import get_credentials_collection
from src.models.request.services import (
    CalendarEventCreateRequest,
    CalendarEventUpdateRequest,
    CalendarQuickAddRequest,
    CreateFolderRequest,
)
from src.models.response.services import (
    AuditLogListResponse,
    AuditLogResponse,
    CalendarEventListResponse,
    CalendarEventResponse,
    DriveBucketResponse,
    DriveFileListResponse,
    DriveFileResponse,
    DrivePreviewResponse,
    EmailDetailResponse,
    EmailListResponse,
    EmailSummaryResponse,
    FileUploadResponse,
    FolderCreatedResponse,
    ServiceActionResponse,
)
from src.services.audit_service import audit_service
from src.services.calendar_service import CalendarService
from src.services.drive_service import DriveService
from src.services.gmail_service import GmailService
from src.utils.crypto import decrypt_token
from src.utils.jwt import get_current_user_from_query_or_header, get_current_user_payload

import json
from googleapiclient.errors import HttpError

logger = logging.getLogger("hermes-api.services")
router = APIRouter(prefix="/services", tags=["Services"])


# ── Helper: Error handler for Google API calls ──

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


# ── Helper: Get decrypted access token for the current user ──

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
            detail="Error al descifrar el token de acceso.",
        )
    return token


# ═══════════════════════════════════════════════════════════════
#  GMAIL ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/emails", response_model=EmailListResponse)
async def list_priority_emails(
    filter_type: str = Query("all", regex="^(all|starred|important)$"),
    search: str = Query("", max_length=200),
    page_token: Optional[str] = Query(None),
    max_results: int = Query(10, ge=1, le=50, description="Número de correos por página"),
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Lista correos destacados e importantes del usuario."""
    user_id = payload.get("sub")
    access_token = await _get_user_access_token(user_id)

    try:
        gmail = GmailService(access_token)
        result = gmail.list_priority_emails(
            filter_type=filter_type,
            search_query=search,
            page_token=page_token,
            max_results=max_results,
        )
        return EmailListResponse(**result)
    except Exception as e:
        _handle_google_error(e, "Gmail")


@router.get("/emails/{message_id}", response_model=EmailDetailResponse)
async def get_email_detail(
    message_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Obtiene el detalle completo de un correo."""
    user_id = payload.get("sub")
    access_token = await _get_user_access_token(user_id)

    try:
        gmail = GmailService(access_token)
        detail = gmail.get_email_detail(message_id)
        return EmailDetailResponse(**detail)
    except Exception as e:
        _handle_google_error(e, "Gmail")


@router.delete("/emails/{message_id}", response_model=ServiceActionResponse)
async def trash_email(
    message_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Mueve un correo a la papelera de Gmail y registra la acción en auditoría."""
    user_id = payload.get("sub")
    user_email = payload.get("email", "")
    access_token = await _get_user_access_token(user_id)

    try:
        gmail = GmailService(access_token)

        # Get email info before trashing for audit purposes
        try:
            email_info = gmail.get_email_detail(message_id)
        except Exception:
            email_info = {"subject": "Unknown", "sender": "Unknown", "snippet": "", "labels": []}

        gmail.trash_email(message_id)

        # Audit log
        await audit_service.log_action(
            user_id=user_id,
            user_email=user_email,
            service="GMAIL",
            action="DELETE_EMAIL",
            resource_id=message_id,
            resource_title=email_info.get("subject", ""),
            details={
                "sender": email_info.get("sender", ""),
                "snippet": email_info.get("snippet", "")[:200] if email_info.get("snippet") else "",
                "labels_before_delete": email_info.get("labels", []),
            },
        )

        return ServiceActionResponse(success=True, message="Correo enviado a la papelera exitosamente.")
    except Exception as e:
        _handle_google_error(e, "Gmail")


# ═══════════════════════════════════════════════════════════════
#  GOOGLE DRIVE ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/drive/bucket", response_model=DriveBucketResponse)
async def get_or_create_bucket(
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Verifica y aprovisiona la carpeta hermes con subcarpetas por defecto en Drive."""
    user_id = payload.get("sub")
    access_token = await _get_user_access_token(user_id)

    try:
        drive = DriveService(access_token)
        bucket = drive.ensure_hermes_bucket()
        return DriveBucketResponse(**bucket)
    except Exception as e:
        _handle_google_error(e, "Google Drive")


@router.get("/drive/files", response_model=DriveFileListResponse)
async def list_drive_files(
    folder_id: str = Query(..., description="ID de la carpeta a listar"),
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Lista archivos y subcarpetas dentro de una carpeta."""
    user_id = payload.get("sub")
    access_token = await _get_user_access_token(user_id)

    try:
        drive = DriveService(access_token)
        result = drive.list_folder_contents(folder_id)
        return DriveFileListResponse(**result)
    except Exception as e:
        _handle_google_error(e, "Google Drive")


@router.post("/drive/folders", response_model=FolderCreatedResponse)
async def create_drive_folder(
    request: CreateFolderRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Crea una nueva subcarpeta en Google Drive."""
    user_id = payload.get("sub")
    user_email = payload.get("email", "")
    access_token = await _get_user_access_token(user_id)

    try:
        drive = DriveService(access_token)
        result = drive.create_folder(request.name, request.parent_folder_id)

        await audit_service.log_action(
            user_id=user_id,
            user_email=user_email,
            service="DRIVE",
            action="CREATE_FOLDER",
            resource_id=result["id"],
            resource_title=request.name,
            details={"parent_folder_id": request.parent_folder_id},
        )

        return FolderCreatedResponse(**result)
    except Exception as e:
        _handle_google_error(e, "Google Drive")


@router.post("/drive/upload", response_model=FileUploadResponse)
async def upload_drive_file(
    file: UploadFile = File(...),
    folder_id: str = Form(...),
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Sube un archivo a una carpeta de Google Drive."""
    user_id = payload.get("sub")
    user_email = payload.get("email", "")
    access_token = await _get_user_access_token(user_id)

    try:
        content = await file.read()
        mime = file.content_type or "application/octet-stream"
        filename = file.filename or "unnamed_file"

        drive = DriveService(access_token)
        result = drive.upload_file(content, filename, mime, folder_id)

        await audit_service.log_action(
            user_id=user_id,
            user_email=user_email,
            service="DRIVE",
            action="UPLOAD_FILE",
            resource_id=result["id"],
            resource_title=filename,
            details={"folder_id": folder_id, "mime_type": mime, "size": result.get("size")},
        )

        return FileUploadResponse(**result)
    except Exception as e:
        _handle_google_error(e, "Google Drive")


@router.delete("/drive/files/{file_id}", response_model=ServiceActionResponse)
async def trash_drive_file(
    file_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Envía un archivo a la papelera de Google Drive y registra la acción."""
    user_id = payload.get("sub")
    user_email = payload.get("email", "")
    access_token = await _get_user_access_token(user_id)

    try:
        drive = DriveService(access_token)

        # Get file info before trashing
        try:
            file_info = drive.get_preview_info(file_id)
            file_name = file_info.get("file_name", "Unknown")
        except Exception:
            file_name = "Unknown"

        drive.trash_file(file_id)

        await audit_service.log_action(
            user_id=user_id,
            user_email=user_email,
            service="DRIVE",
            action="DELETE_FILE",
            resource_id=file_id,
            resource_title=file_name,
        )

        return ServiceActionResponse(success=True, message="Archivo enviado a la papelera exitosamente.")
    except Exception as e:
        _handle_google_error(e, "Google Drive")


@router.get("/drive/files/{file_id}/preview", response_model=DrivePreviewResponse)
async def get_file_preview(
    file_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Obtiene URL de previsualización y descarga de un archivo."""
    user_id = payload.get("sub")
    access_token = await _get_user_access_token(user_id)

    try:
        drive = DriveService(access_token)
        info = drive.get_preview_info(file_id)
        return DrivePreviewResponse(**info)
    except Exception as e:
        _handle_google_error(e, "Google Drive")


@router.get("/drive/files/{file_id}/content")
async def get_drive_file_content(
    file_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_from_query_or_header),
):
    """
    Descarga y sirve directamente el flujo binario del archivo/imagen de Google Drive
    usando las credenciales autorizadas del usuario, permitiendo el renderizado confiable
    en etiquetas <img> sin problemas de cookies de terceros o bloqueos CORS.
    """
    user_id = payload.get("sub")
    access_token = await _get_user_access_token(user_id)

    try:
        drive = DriveService(access_token)
        content_bytes, mime_type, filename = drive.get_file_content(file_id)

        headers = {
            "Content-Disposition": f'inline; filename="{filename}"',
            "Cache-Control": "public, max-age=86400, stale-while-revalidate=604800",
        }
        return Response(content=content_bytes, media_type=mime_type, headers=headers)
    except Exception as e:
        _handle_google_error(e, "Google Drive")


# ═══════════════════════════════════════════════════════════════
#  AUDIT ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/audit-logs", response_model=AuditLogListResponse)
async def get_audit_logs(
    service: Optional[str] = Query(None, regex="^(GMAIL|DRIVE|CALENDAR)?$"),
    limit: int = Query(50, ge=1, le=200),
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Consulta el historial de auditoría del usuario autenticado."""
    user_id = payload.get("sub")
    logs = await audit_service.get_user_logs(
        user_id=user_id,
        service_filter=service,
        limit=limit,
    )
    return AuditLogListResponse(logs=logs, total=len(logs))


# ═══════════════════════════════════════════════════════════════
#  GOOGLE CALENDAR ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/calendar/events", response_model=CalendarEventListResponse)
async def list_calendar_events(
    time_min: Optional[str] = Query(None, description="Fecha/hora mínima (ISO 8601)"),
    time_max: Optional[str] = Query(None, description="Fecha/hora máxima (ISO 8601)"),
    q: Optional[str] = Query(None, description="Búsqueda por texto en eventos"),
    max_results: int = Query(100, ge=1, le=250),
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Obtiene los eventos del Google Calendar del usuario."""
    user_id = payload.get("sub")
    access_token = await _get_user_access_token(user_id)

    try:
        cal = CalendarService(access_token)
        events = cal.list_events(
            time_min=time_min,
            time_max=time_max,
            q=q,
            max_results=max_results,
        )
        return CalendarEventListResponse(
            events=events,
            total=len(events),
            time_min=time_min,
            time_max=time_max,
        )
    except Exception as e:
        _handle_google_error(e, "Google Calendar")


@router.post("/calendar/events", response_model=CalendarEventResponse, status_code=status.HTTP_201_CREATED)
async def create_calendar_event(
    req: CalendarEventCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Crea un nuevo evento en Google Calendar y registra auditoría."""
    user_id = payload.get("sub")
    user_email = payload.get("email", "")
    access_token = await _get_user_access_token(user_id)

    try:
        cal = CalendarService(access_token)
        created = cal.create_event(req)

        await audit_service.log_action(
            user_id=user_id,
            user_email=user_email,
            service="CALENDAR",
            action="CREATE_EVENT",
            resource_id=created.get("id", ""),
            resource_title=created.get("summary", ""),
            details={
                "start": created.get("start"),
                "end": created.get("end"),
                "location": created.get("location"),
            },
        )

        return CalendarEventResponse(**created)
    except Exception as e:
        _handle_google_error(e, "Google Calendar")


@router.get("/calendar/events/{event_id}", response_model=CalendarEventResponse)
async def get_calendar_event(
    event_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Obtiene el detalle de un evento específico de Google Calendar."""
    user_id = payload.get("sub")
    access_token = await _get_user_access_token(user_id)

    try:
        cal = CalendarService(access_token)
        item = cal.get_event(event_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
        return CalendarEventResponse(**item)
    except Exception as e:
        _handle_google_error(e, "Google Calendar")


@router.put("/calendar/events/{event_id}", response_model=CalendarEventResponse)
async def update_calendar_event(
    event_id: str,
    req: CalendarEventUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Actualiza un evento existente en Google Calendar."""
    user_id = payload.get("sub")
    user_email = payload.get("email", "")
    access_token = await _get_user_access_token(user_id)

    try:
        cal = CalendarService(access_token)
        updated = cal.update_event(event_id, req)

        await audit_service.log_action(
            user_id=user_id,
            user_email=user_email,
            service="CALENDAR",
            action="UPDATE_EVENT",
            resource_id=event_id,
            resource_title=updated.get("summary", ""),
            details={
                "start": updated.get("start"),
                "end": updated.get("end"),
                "location": updated.get("location"),
            },
        )

        return CalendarEventResponse(**updated)
    except Exception as e:
        _handle_google_error(e, "Google Calendar")


@router.delete("/calendar/events/{event_id}", response_model=ServiceActionResponse)
async def delete_calendar_event(
    event_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Elimina un evento de Google Calendar y registra auditoría."""
    user_id = payload.get("sub")
    user_email = payload.get("email", "")
    access_token = await _get_user_access_token(user_id)

    try:
        cal = CalendarService(access_token)
        cal.delete_event(event_id)

        await audit_service.log_action(
            user_id=user_id,
            user_email=user_email,
            service="CALENDAR",
            action="DELETE_EVENT",
            resource_id=event_id,
            resource_title=f"Evento {event_id}",
        )

        return ServiceActionResponse(success=True, message="Evento eliminado exitosamente de Google Calendar.")
    except Exception as e:
        _handle_google_error(e, "Google Calendar")


@router.post("/calendar/quick-add", response_model=CalendarEventResponse, status_code=status.HTTP_201_CREATED)
async def quick_add_calendar_event(
    req: CalendarQuickAddRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Creación rápida de evento mediante lenguaje natural en Google Calendar."""
    user_id = payload.get("sub")
    user_email = payload.get("email", "")
    access_token = await _get_user_access_token(user_id)

    try:
        cal = CalendarService(access_token)
        created = cal.quick_add_event(req.text)

        await audit_service.log_action(
            user_id=user_id,
            user_email=user_email,
            service="CALENDAR",
            action="QUICK_ADD_EVENT",
            resource_id=created.get("id", ""),
            resource_title=created.get("summary", req.text),
            details={"raw_text": req.text},
        )

        return CalendarEventResponse(**created)
    except Exception as e:
        _handle_google_error(e, "Google Calendar")

