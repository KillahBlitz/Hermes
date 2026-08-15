import logging
import os
from typing import Any, Dict, Optional
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials
from fastapi import HTTPException, status
from src.config.settings import get_settings

logger = logging.getLogger("hermes-api.firebase")


class FirebaseService:
    _instance: Optional["FirebaseService"] = None
    _initialized: bool = False

    def __new__(cls) -> "FirebaseService":
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self._initialize_app()
            self._initialized = True

    def _initialize_app(self) -> None:
        settings = get_settings()
        cred_path = settings.FIREBASE_CREDENTIALS_PATH

        # Check if already initialized in another part of the app
        if firebase_admin._apps:
            logger.info("Firebase Admin SDK ya se encuentra inicializado.")
            return

        # Resolve relative path from project root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        resolved_path = os.path.join(base_dir, cred_path) if not os.path.isabs(cred_path) else cred_path

        if os.path.exists(resolved_path):
            try:
                cred = credentials.Certificate(resolved_path)
                firebase_admin.initialize_app(cred)
                logger.info(f"Firebase Admin SDK inicializado correctamente con credenciales desde: {resolved_path}")
            except Exception as e:
                logger.error(f"Error al inicializar Firebase Admin SDK con certificado: {e}")
        else:
            logger.warning(
                f"Archivo de credenciales de Firebase no encontrado en '{resolved_path}'. "
                f"Para producción, descarga 'serviceAccountKey.json' de Firebase Console y colócalo en '{cred_path}'."
            )
            try:
                # Attempt default credentials
                firebase_admin.initialize_app()
                logger.info("Firebase Admin SDK inicializado con credenciales por defecto de Google Cloud.")
            except Exception as e:
                logger.warning(f"No se pudieron cargar credenciales por defecto de Firebase: {e}")

    def verify_token(self, id_token: str) -> Dict[str, Any]:
        """
        Verifica un Firebase ID Token y devuelve los datos decodificados.
        """
        if not id_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID Token de Firebase es requerido.",
            )

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            return decoded_token
        except firebase_auth.ExpiredIdTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El ID Token de Firebase ha expirado.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except firebase_auth.InvalidIdTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El ID Token de Firebase es inválido.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.error(f"Error durante la verificación del token de Firebase: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Fallo de autenticación con Firebase: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Singleton instance
firebase_service = FirebaseService()
