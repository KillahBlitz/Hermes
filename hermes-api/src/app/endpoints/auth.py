import logging
from datetime import datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from src.config.settings import get_settings
from src.database.mongo import get_credentials_collection, get_users_collection
from src.models.request.auth import GoogleLoginRequest
from src.models.response.auth import (
    LoginResponse,
    LogoutResponse,
    UserMeResponse,
    UserProfileResponse,
)
from src.services.firebase_service import firebase_service
from src.utils.crypto import encrypt_token
from src.utils.jwt import create_access_token, get_current_user_payload

logger = logging.getLogger("hermes-api.auth")
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login_with_google(request: GoogleLoginRequest):
    """
    Autentica al usuario mediante Firebase ID Token y almacena sus credenciales
    de Google OAuth (con scopes de Drive, Calendar, Gmail) en MongoDB.
    """
    settings = get_settings()

    # 1. Verificar ID Token de Firebase
    firebase_user = firebase_service.verify_token(request.id_token)
    uid = firebase_user.get("uid")
    email = firebase_user.get("email")
    display_name = firebase_user.get("name") or firebase_user.get("display_name", "")
    photo_url = firebase_user.get("picture") or firebase_user.get("photo_url")

    if not uid or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token de Firebase no contiene información válida de usuario (uid/email).",
        )

    now = datetime.now(timezone.utc)

    # 2. Cifrar los tokens de Google OAuth antes de persistir
    encrypted_access_token = encrypt_token(request.google_access_token)
    encrypted_refresh_token = encrypt_token(request.google_refresh_token)

    # 3. Guardar / Actualizar en MongoDB si la base de datos está disponible
    users_col = get_users_collection()
    credentials_col = get_credentials_collection()

    if users_col is not None and credentials_col is not None:
        try:
            # Upsert en colección 'users'
            await users_col.update_one(
                {"_id": uid},
                {
                    "$set": {
                        "email": email,
                        "display_name": display_name,
                        "photo_url": photo_url,
                        "updated_at": now,
                    },
                    "$setOnInsert": {
                        "created_at": now,
                    },
                },
                upsert=True,
            )

            # Upsert en colección 'user_credentials'
            cred_payload = {
                "google_access_token_encrypted": encrypted_access_token,
                "google_token_expiry": request.google_token_expiry,
                "scopes": request.scopes or [],
                "updated_at": now,
            }
            if encrypted_refresh_token:
                cred_payload["google_refresh_token_encrypted"] = encrypted_refresh_token

            await credentials_col.update_one(
                {"_id": uid},
                {"$set": cred_payload},
                upsert=True,
            )
            logger.info(f"Usuario {email} ({uid}) persistido exitosamente en MongoDB.")
        except Exception as e:
            logger.error(f"Error al persistir usuario en MongoDB: {e}")
            # Continuamos para no bloquear la sesión si la BD tiene un problema transitorio

    # 4. Generar Token de Sesión JWT interno de Hermes (1 día = 1440 mins)
    session_payload = {
        "sub": uid,
        "email": email,
        "name": display_name,
        "picture": photo_url,
        "scopes": request.scopes or [],
    }
    session_token = create_access_token(session_payload)
    expires_in = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60

    user_profile = UserProfileResponse(
        uid=uid,
        email=email,
        display_name=display_name,
        photo_url=photo_url,
        created_at=now,
        granted_scopes=request.scopes or [],
    )

    return LoginResponse(
        message="Inicio de sesión exitoso con Google",
        user=user_profile,
        session_token=session_token,
        token_type="Bearer",
        expires_in=expires_in,
    )


@router.get("/me", response_model=UserMeResponse)
async def get_current_user_profile(
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """
    Retorna la información del usuario autenticado en la sesión actual.
    """
    uid = payload.get("sub")
    email = payload.get("email")
    name = payload.get("name")
    picture = payload.get("picture")
    scopes = payload.get("scopes", [])

    users_col = get_users_collection()
    user_data = None
    if users_col is not None and uid:
        try:
            user_data = await users_col.find_one({"_id": uid})
        except Exception as e:
            logger.warning(f"No se pudo consultar MongoDB para /me: {e}")

    if user_data:
        return UserMeResponse(
            user=UserProfileResponse(
                uid=user_data.get("_id", uid),
                email=user_data.get("email", email),
                display_name=user_data.get("display_name", name),
                photo_url=user_data.get("photo_url", picture),
                created_at=user_data.get("created_at"),
                granted_scopes=scopes,
            )
        )

    # Fallback al payload del JWT
    return UserMeResponse(
        user=UserProfileResponse(
            uid=uid,
            email=email,
            display_name=name,
            photo_url=picture,
            granted_scopes=scopes,
        )
    )


@router.post("/logout", response_model=LogoutResponse)
async def logout(payload: Dict[str, Any] = Depends(get_current_user_payload)):
    """
    Invalida o finaliza la sesión activa del usuario.
    """
    user_email = payload.get("email", "Desconocido")
    logger.info(f"Usuario {user_email} cerró sesión.")
    return LogoutResponse(
        message="Sesión finalizada exitosamente.",
        success=True,
    )
