import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.endpoints.auth import router as auth_router
from src.app.endpoints.boards import router as boards_router
from src.app.endpoints.finance import router as finance_router
from src.app.endpoints.lists import router as lists_router
from src.app.endpoints.services import router as services_router
from src.config.settings import get_settings
from src.database.mongo import db_manager

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("hermes-api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Iniciando Hermes API...")
    db_manager.connect()
    yield
    # Shutdown
    logger.info("Apagando Hermes API...")
    db_manager.close()


settings = get_settings()

app = FastAPI(
    title="Hermes API",
    description="Backend API para la plataforma modular Hermes con autenticación Firebase y Google OAuth",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
origins = settings.cors_origins_list
if not origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|100\.\d{1,3}\.\d{1,3}\.\d{1,3}|.*\.ts\.net)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(services_router, prefix="/api/v1")
app.include_router(finance_router, prefix="/api/v1")
app.include_router(boards_router, prefix="/api/v1")
app.include_router(lists_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "service": "Hermes API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development")
    )
