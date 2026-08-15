from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class UserProfileResponse(BaseModel):
    uid: str = Field(..., description="Firebase Unique Identifier")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    display_name: Optional[str] = Field(None, description="Nombre visible del usuario")
    photo_url: Optional[str] = Field(None, description="URL de foto de perfil")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación de la cuenta")
    granted_scopes: Optional[List[str]] = Field(
        default_factory=list,
        description="Lista de scopes de Google actualmente vinculados"
    )


class LoginResponse(BaseModel):
    message: str = Field(default="Inicio de sesión exitoso")
    user: UserProfileResponse
    session_token: str = Field(..., description="Token de sesión JWT para autorizar peticiones en Hermes API")
    token_type: str = Field(default="Bearer")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos (86400 = 1 día)")


class UserMeResponse(BaseModel):
    user: UserProfileResponse


class LogoutResponse(BaseModel):
    message: str = Field(default="Sesión cerrada correctamente")
    success: bool = True
