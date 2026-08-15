import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = "http://localhost:3000"

    # Database configuration
    MONGO_HOST: str = "mongodb://localhost:27017/"
    MONGO_DATABASE: str = "hermes_db"

    # Firebase Admin SDK configuration
    FIREBASE_CREDENTIALS_PATH: str = "config/serviceAccountKey.json"

    # Cryptography (Fernet symmetric key)
    ENCRYPTION_KEY: str = ""

    # JWT Session configuration (1 day default)
    JWT_SECRET_KEY: str = "hermes_default_secret_key_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
