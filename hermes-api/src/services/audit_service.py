import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from src.database.mongo import get_audit_logs_collection

logger = logging.getLogger("hermes-api.audit")


class AuditService:
    """Service for persisting and querying service action audit logs in MongoDB."""

    @staticmethod
    async def log_action(
        user_id: str,
        user_email: str,
        service: str,
        action: str,
        resource_id: str,
        resource_title: str,
        details: Optional[Dict[str, Any]] = None,
        action_status: str = "SUCCESS",
    ) -> Optional[str]:
        """
        Persist an immutable audit log entry to MongoDB.
        Returns the inserted document ID or None if DB is unavailable.
        """
        collection = get_audit_logs_collection()
        if collection is None:
            logger.warning("Audit log collection unavailable, skipping log.")
            return None

        doc = {
            "user_id": user_id,
            "user_email": user_email,
            "service": service,
            "action": action,
            "resource_id": resource_id,
            "resource_title": resource_title,
            "details": details or {},
            "timestamp": datetime.now(timezone.utc),
            "status": action_status,
        }

        try:
            result = await collection.insert_one(doc)
            logger.info(
                f"Audit log: [{service}] {action} on '{resource_title}' by {user_email} — {action_status}"
            )
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to persist audit log: {e}")
            return None

    @staticmethod
    async def get_user_logs(
        user_id: str,
        service_filter: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Query audit logs for a specific user."""
        collection = get_audit_logs_collection()
        if collection is None:
            return []

        query: Dict[str, Any] = {"user_id": user_id}
        if service_filter:
            query["service"] = service_filter.upper()

        try:
            cursor = collection.find(query).sort("timestamp", -1).limit(limit)
            logs = []
            async for doc in cursor:
                logs.append({
                    "id": str(doc["_id"]),
                    "service": doc.get("service", ""),
                    "action": doc.get("action", ""),
                    "resource_id": doc.get("resource_id", ""),
                    "resource_title": doc.get("resource_title", ""),
                    "timestamp": doc.get("timestamp"),
                    "status": doc.get("status", ""),
                    "details": doc.get("details"),
                })
            return logs
        except Exception as e:
            logger.error(f"Failed to query audit logs: {e}")
            return []


audit_service = AuditService()
