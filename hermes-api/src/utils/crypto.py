import base64
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
from src.config.settings import get_settings


def get_fernet_instance() -> Optional[Fernet]:
    settings = get_settings()
    key = settings.ENCRYPTION_KEY
    if not key:
        return None
    try:
        # Ensure key is valid Fernet key
        return Fernet(key.encode() if isinstance(key, str) else key)
    except Exception:
        # If key is not 32 url-safe base64-encoded bytes, pad/format it
        try:
            padded_key = base64.urlsafe_b64encode(key.encode().ljust(32)[:32])
            return Fernet(padded_key)
        except Exception:
            return None


def encrypt_token(token: Optional[str]) -> Optional[str]:
    if not token:
        return None
    fernet = get_fernet_instance()
    if not fernet:
        # Fallback if no encryption key configured in dev
        return token
    return fernet.encrypt(token.encode("utf-8")).decode("utf-8")


def decrypt_token(encrypted_token: Optional[str]) -> Optional[str]:
    if not encrypted_token:
        return None
    fernet = get_fernet_instance()
    if not fernet:
        return encrypted_token
    try:
        return fernet.decrypt(encrypted_token.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        return encrypted_token
