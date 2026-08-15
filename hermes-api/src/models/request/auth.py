from typing import List, Optional
from pydantic import BaseModel, Field


class GoogleLoginRequest(BaseModel):
    id_token: str = Field(..., description="ID Token emitido por Firebase Auth")
    google_access_token: str = Field(..., description="Access Token de Google OAuth para interactuar con APIs")
    google_refresh_token: Optional[str] = Field(None, description="Refresh Token de Google OAuth (opcional)")
    google_token_expiry: Optional[int] = Field(None, description="Timestamp de expiración del access token de Google")
    scopes: Optional[List[str]] = Field(
        default_factory=lambda: [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.modify"
        ],
        description="Lista de scopes solicitados y concedidos"
    )
