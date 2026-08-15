import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from src.config.settings import get_settings

logger = logging.getLogger("hermes-api.database")


class MongoDBManager:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    def connect(self) -> None:
        settings = get_settings()
        try:
            logger.info(f"Conectando a MongoDB en: {settings.MONGO_HOST}...")
            self.client = AsyncIOMotorClient(
                settings.MONGO_HOST,
                serverSelectionTimeoutMS=3000
            )
            self.db = self.client[settings.MONGO_DATABASE]
            logger.info(f"Base de datos seleccionada: {settings.MONGO_DATABASE}")
        except Exception as e:
            logger.warning(f"No se pudo conectar a MongoDB de inmediato: {e}")

    def close(self) -> None:
        if self.client:
            self.client.close()
            logger.info("Conexión con MongoDB cerrada.")

    def get_collection(self, name: str) -> Optional[AsyncIOMotorCollection]:
        if self.db is not None:
            return self.db[name]
        return None


db_manager = MongoDBManager()


def get_users_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("users")


def get_credentials_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("user_credentials")


def get_audit_logs_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("service_audit_logs")


def get_finance_transactions_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("finance_transactions")


def get_finance_categories_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("finance_categories")


def get_board_epics_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("board_epics")


def get_board_tasks_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("board_tasks")


def get_board_habits_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("board_habits")


def get_board_sticky_notes_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("board_sticky_notes")


def get_wishlist_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("wishlist_items")


def get_todo_sections_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("todo_sections")


def get_todo_tasks_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("todo_tasks")


def get_progress_roadmaps_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("progress_roadmaps")


def get_progress_milestones_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("progress_milestones")


def get_progress_notes_collection() -> Optional[AsyncIOMotorCollection]:
    return db_manager.get_collection("progress_notes")


