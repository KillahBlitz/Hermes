import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from bson import ObjectId
from src.database.mongo import (
    get_todo_sections_collection,
    get_todo_tasks_collection,
    get_wishlist_collection,
)
from src.models.request.lists import (
    TodoSectionCreateRequest,
    TodoSectionUpdateRequest,
    TodoTaskCreateRequest,
    TodoTaskToggleRequest,
    TodoTaskUpdateRequest,
    WishlistItemCreateRequest,
    WishlistItemStatusRequest,
    WishlistItemUpdateRequest,
)
from src.models.response.lists import (
    TodoSectionListResponse,
    TodoSectionResponse,
    TodoTaskListResponse,
    TodoTaskResponse,
    WishlistImageResponse,
    WishlistItemResponse,
    WishlistListResponse,
    WishlistStatsResponse,
)
from src.services.drive_service import DriveService

logger = logging.getLogger("hermes-api.lists")

DEFAULT_TODO_SECTIONS = [
    {
        "name": "Mi Día",
        "icon": "☀️",
        "color": "#00FFC6",
        "order": 1,
        "is_default": True
    },
    {
        "name": "Rutinas Diarias",
        "icon": "🔁",
        "color": "#00E5FF",
        "order": 2,
        "is_default": True
    },
    {
        "name": "Hogar & Personal",
        "icon": "🏠",
        "color": "#FFD166",
        "order": 3,
        "is_default": True
    },
    {
        "name": "Trabajo & Proyectos",
        "icon": "💼",
        "color": "#FF007F",
        "order": 4,
        "is_default": True
    }
]


class ListsService:

    # ─────────────────────────────────────────────────────────────
    # LISTA DE DESEOS (WISHLIST)
    # ─────────────────────────────────────────────────────────────

    def _doc_to_wishlist_item(self, doc: Dict[str, Any]) -> WishlistItemResponse:
        import re
        images_raw = doc.get("images", [])
        images = []
        for img in images_raw:
            drive_id = img.get("drive_file_id") or ""
            if not drive_id:
                link = img.get("thumbnail_link") or img.get("web_view_link") or ""
                m = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', link) or re.search(r'/d/([a-zA-Z0-9_-]+)', link)
                if m:
                    drive_id = m.group(1)

            images.append(WishlistImageResponse(
                drive_file_id=drive_id,
                name=img.get("name", "foto.jpg"),
                mime_type=img.get("mime_type", "image/jpeg"),
                size=int(img.get("size", 0)),
                thumbnail_link=img.get("thumbnail_link"),
                web_view_link=img.get("web_view_link")
            ))

        return WishlistItemResponse(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            name=doc["name"],
            price=float(doc.get("price", 0.0)),
            currency=doc.get("currency", "MXN"),
            category=doc.get("category", "General"),
            priority=doc.get("priority", "MEDIA"),
            description=doc.get("description"),
            url=doc.get("url"),
            images=images,
            status=doc.get("status", "PENDING"),
            purchased_at=doc.get("purchased_at"),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at")
        )

    async def list_wishlist(
        self,
        user_id: str,
        status_filter: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        search: Optional[str] = None
    ) -> WishlistListResponse:
        col = get_wishlist_collection()
        if col is None:
            return WishlistListResponse(
                items=[],
                stats=WishlistStatsResponse(),
                total=0
            )

        query: Dict[str, Any] = {"user_id": user_id}
        if status_filter and status_filter in ("PENDING", "PURCHASED", "ARCHIVED"):
            query["status"] = status_filter
        if category and category.strip():
            query["category"] = category.strip()
        if priority and priority in ("ALTA", "MEDIA", "BAJA"):
            query["priority"] = priority
        if search and search.strip():
            query["name"] = {"$regex": search.strip(), "$options": "i"}

        cursor = col.find(query).sort([("created_at", -1)])
        items = []
        async for doc in cursor:
            items.append(self._doc_to_wishlist_item(doc))

        # Calcular Estadísticas / KPIs globales para el usuario
        pipeline = [
            {"$match": {"user_id": user_id}},
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                    "total_value": {"$sum": "$price"}
                }
            }
        ]
        total_items = 0
        pending_items = 0
        purchased_items = 0
        total_pending_value = 0.0
        total_purchased_value = 0.0

        async for group in col.aggregate(pipeline):
            st = group["_id"]
            cnt = group["count"]
            val = float(group.get("total_value", 0.0))
            total_items += cnt

            if st == "PENDING":
                pending_items = cnt
                total_pending_value = val
            elif st == "PURCHASED":
                purchased_items = cnt
                total_purchased_value = val

        stats = WishlistStatsResponse(
            total_items=total_items,
            pending_items=pending_items,
            purchased_items=purchased_items,
            total_pending_value=round(total_pending_value, 2),
            total_purchased_value=round(total_purchased_value, 2),
            currency="MXN"
        )

        return WishlistListResponse(
            items=items,
            stats=stats,
            total=len(items)
        )

    async def create_wishlist_item(self, user_id: str, req: WishlistItemCreateRequest) -> WishlistItemResponse:
        col = get_wishlist_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        now = datetime.utcnow()
        doc = {
            "user_id": user_id,
            "name": req.name.strip(),
            "price": float(req.price),
            "currency": req.currency.strip().upper(),
            "category": req.category.strip() if req.category else "General",
            "priority": req.priority,
            "description": req.description.strip() if req.description else None,
            "url": req.url.strip() if req.url else None,
            "images": [],
            "status": req.status,
            "purchased_at": now if req.status == "PURCHASED" else None,
            "created_at": now,
            "updated_at": now,
        }
        res = await col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._doc_to_wishlist_item(doc)

    async def update_wishlist_item(
        self,
        user_id: str,
        item_id: str,
        req: WishlistItemUpdateRequest
    ) -> Optional[WishlistItemResponse]:
        col = get_wishlist_collection()
        if col is None or not ObjectId.is_valid(item_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}
        if req.name is not None:
            update_data["name"] = req.name.strip()
        if req.price is not None:
            update_data["price"] = float(req.price)
        if req.currency is not None:
            update_data["currency"] = req.currency.strip().upper()
        if req.category is not None:
            update_data["category"] = req.category.strip()
        if req.priority is not None:
            update_data["priority"] = req.priority
        if req.description is not None:
            update_data["description"] = req.description.strip()
        if req.url is not None:
            update_data["url"] = req.url.strip()
        if req.status is not None:
            update_data["status"] = req.status
            if req.status == "PURCHASED":
                update_data["purchased_at"] = datetime.utcnow()
            else:
                update_data["purchased_at"] = None

        res = await col.find_one_and_update(
            {"_id": ObjectId(item_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None
        return self._doc_to_wishlist_item(res)

    async def update_wishlist_status(
        self,
        user_id: str,
        item_id: str,
        req: WishlistItemStatusRequest
    ) -> Optional[WishlistItemResponse]:
        col = get_wishlist_collection()
        if col is None or not ObjectId.is_valid(item_id):
            return None

        now = datetime.utcnow()
        update_data: Dict[str, Any] = {
            "status": req.status,
            "updated_at": now,
            "purchased_at": now if req.status == "PURCHASED" else None
        }

        res = await col.find_one_and_update(
            {"_id": ObjectId(item_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None
        return self._doc_to_wishlist_item(res)

    async def upload_wishlist_photo(
        self,
        user_id: str,
        item_id: str,
        access_token: str,
        file_content: bytes,
        filename: str,
        mime_type: str
    ) -> Optional[WishlistItemResponse]:
        col = get_wishlist_collection()
        if col is None or not ObjectId.is_valid(item_id):
            return None

        # 1. Asegurar la subcarpeta 'whitelist' en Google Drive
        drive_svc = DriveService(access_token)
        whitelist_folder_id = drive_svc.ensure_whitelist_folder()

        # 2. Subir archivo a Drive
        uploaded = drive_svc.upload_file(
            file_content=file_content,
            filename=filename,
            mime_type=mime_type,
            folder_id=whitelist_folder_id
        )

        file_id = uploaded["id"]
        raw_size = uploaded.get("size")
        size_num = int(raw_size) if (raw_size is not None and str(raw_size).isdigit()) else len(file_content)
        thumbnail = uploaded.get("thumbnail_link") or uploaded.get("thumbnailLink") or f"https://drive.google.com/thumbnail?id={file_id}"
        web_view = uploaded.get("web_view_link") or uploaded.get("webViewLink") or f"https://drive.google.com/file/d/{file_id}/view"

        image_entry = {
            "drive_file_id": file_id,
            "name": uploaded.get("name", filename),
            "mime_type": uploaded.get("mime_type") or uploaded.get("mimeType", mime_type),
            "size": size_num,
            "thumbnail_link": thumbnail,
            "web_view_link": web_view
        }

        res = await col.find_one_and_update(
            {"_id": ObjectId(item_id), "user_id": user_id},
            {
                "$push": {"images": image_entry},
                "$set": {"updated_at": datetime.utcnow()}
            },
            return_document=True
        )
        if not res:
            return None
        return self._doc_to_wishlist_item(res)

    async def delete_wishlist_item(self, user_id: str, item_id: str) -> bool:
        col = get_wishlist_collection()
        if col is None or not ObjectId.is_valid(item_id):
            return False
        res = await col.delete_one({"_id": ObjectId(item_id), "user_id": user_id})
        return res.deleted_count > 0

    # ─────────────────────────────────────────────────────────────
    # LISTA DE TAREAS (MICROSOFT TO-DO STYLE)
    # ─────────────────────────────────────────────────────────────

    async def ensure_default_sections(self, user_id: str) -> None:
        """Siembra atómicamente las 4 secciones predeterminadas para el usuario."""
        col = get_todo_sections_collection()
        if col is None:
            return

        now = datetime.utcnow()
        for sec in DEFAULT_TODO_SECTIONS:
            await col.update_one(
                {"user_id": user_id, "name": sec["name"]},
                {
                    "$setOnInsert": {
                        "user_id": user_id,
                        "name": sec["name"],
                        "icon": sec["icon"],
                        "color": sec["color"],
                        "order": sec["order"],
                        "is_default": True,
                        "created_at": now
                    }
                },
                upsert=True
            )

        # Deduplicación
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": "$name", "ids": {"$push": "$_id"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}
        ]
        async for dup in col.aggregate(pipeline):
            ids_to_remove = dup["ids"][1:]
            if ids_to_remove:
                await col.delete_many({"_id": {"$in": ids_to_remove}})

    async def list_sections(self, user_id: str) -> List[TodoSectionResponse]:
        await self.ensure_default_sections(user_id)
        col_sec = get_todo_sections_collection()
        col_tasks = get_todo_tasks_collection()
        if col_sec is None:
            return []

        cursor = col_sec.find({"user_id": user_id}).sort([("order", 1), ("name", 1)])
        sections = []
        async for doc in cursor:
            sec_id_str = str(doc["_id"])
            pending_count = 0
            completed_count = 0

            if col_tasks is not None:
                pending_count = await col_tasks.count_documents({
                    "user_id": user_id,
                    "section_id": sec_id_str,
                    "is_completed": False
                })
                completed_count = await col_tasks.count_documents({
                    "user_id": user_id,
                    "section_id": sec_id_str,
                    "is_completed": True
                })

            sections.append(TodoSectionResponse(
                id=sec_id_str,
                user_id=doc.get("user_id"),
                name=doc["name"],
                icon=doc.get("icon", "📋"),
                color=doc.get("color", "#00E5FF"),
                is_default=doc.get("is_default", False),
                order=doc.get("order", 0),
                pending_count=pending_count,
                completed_count=completed_count,
                created_at=doc.get("created_at")
            ))
        return sections

    async def create_section(self, user_id: str, req: TodoSectionCreateRequest) -> TodoSectionResponse:
        col = get_todo_sections_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        now = datetime.utcnow()
        doc = {
            "user_id": user_id,
            "name": req.name.strip(),
            "icon": req.icon,
            "color": req.color,
            "order": 10,
            "is_default": False,
            "created_at": now
        }
        res = await col.insert_one(doc)
        return TodoSectionResponse(
            id=str(res.inserted_id),
            user_id=user_id,
            name=doc["name"],
            icon=doc["icon"],
            color=doc["color"],
            is_default=False,
            order=10,
            pending_count=0,
            completed_count=0,
            created_at=now
        )

    async def update_section(
        self,
        user_id: str,
        section_id: str,
        req: TodoSectionUpdateRequest
    ) -> Optional[TodoSectionResponse]:
        col = get_todo_sections_collection()
        if col is None or not ObjectId.is_valid(section_id):
            return None

        update_data: Dict[str, Any] = {}
        if req.name is not None:
            update_data["name"] = req.name.strip()
        if req.icon is not None:
            update_data["icon"] = req.icon
        if req.color is not None:
            update_data["color"] = req.color

        res = await col.find_one_and_update(
            {"_id": ObjectId(section_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        return TodoSectionResponse(
            id=str(res["_id"]),
            user_id=res.get("user_id"),
            name=res["name"],
            icon=res.get("icon", "📋"),
            color=res.get("color", "#00E5FF"),
            is_default=res.get("is_default", False),
            order=res.get("order", 0),
            created_at=res.get("created_at")
        )

    async def delete_section(self, user_id: str, section_id: str) -> bool:
        col_sec = get_todo_sections_collection()
        col_tasks = get_todo_tasks_collection()
        if col_sec is None or not ObjectId.is_valid(section_id):
            return False

        # Desvincular tareas de esta sección
        if col_tasks is not None:
            await col_tasks.update_many(
                {"user_id": user_id, "section_id": section_id},
                {"$set": {"section_id": None, "updated_at": datetime.utcnow()}}
            )

        res = await col_sec.delete_one({"_id": ObjectId(section_id), "user_id": user_id})
        return res.deleted_count > 0

    # ── Tareas To-Do ──

    async def _populate_section(self, user_id: str, section_id: Optional[str]) -> Optional[TodoSectionResponse]:
        if not section_id or not ObjectId.is_valid(section_id):
            return None
        col = get_todo_sections_collection()
        if col is None:
            return None
        doc = await col.find_one({"_id": ObjectId(section_id), "user_id": user_id})
        if not doc:
            return None
        return TodoSectionResponse(
            id=str(doc["_id"]),
            user_id=doc.get("user_id"),
            name=doc["name"],
            icon=doc.get("icon", "📋"),
            color=doc.get("color", "#00E5FF"),
            is_default=doc.get("is_default", False),
            order=doc.get("order", 0),
            created_at=doc.get("created_at")
        )

    def _doc_to_todo_task(self, doc: Dict[str, Any], sec_resp: Optional[TodoSectionResponse] = None) -> TodoTaskResponse:
        return TodoTaskResponse(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            section_id=doc.get("section_id"),
            section=sec_resp,
            title=doc["title"],
            difficulty_points=int(doc.get("difficulty_points", 1)),
            repeat=doc.get("repeat", "NONE"),
            due_date=doc.get("due_date"),
            notes=doc.get("notes"),
            is_completed=bool(doc.get("is_completed", False)),
            completed_at=doc.get("completed_at"),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at")
        )

    async def list_todo_tasks(
        self,
        user_id: str,
        section_id: Optional[str] = None,
        is_completed: Optional[bool] = None,
        search: Optional[str] = None
    ) -> TodoTaskListResponse:
        col = get_todo_tasks_collection()
        if col is None:
            return TodoTaskListResponse(tasks=[], total=0, pending_count=0, completed_count=0)

        query: Dict[str, Any] = {"user_id": user_id}
        if section_id and ObjectId.is_valid(section_id):
            query["section_id"] = section_id
        if is_completed is not None:
            query["is_completed"] = is_completed
        if search and search.strip():
            query["title"] = {"$regex": search.strip(), "$options": "i"}

        sections_map = {s.id: s for s in await self.list_sections(user_id)}
        cursor = col.find(query).sort([("is_completed", 1), ("created_at", -1)])
        tasks = []
        pending_count = 0
        completed_count = 0

        async for doc in cursor:
            sec_resp = sections_map.get(doc.get("section_id"))
            task_resp = self._doc_to_todo_task(doc, sec_resp)
            tasks.append(task_resp)
            if task_resp.is_completed:
                completed_count += 1
            else:
                pending_count += 1

        return TodoTaskListResponse(
            tasks=tasks,
            total=len(tasks),
            pending_count=pending_count,
            completed_count=completed_count
        )

    async def create_todo_task(self, user_id: str, req: TodoTaskCreateRequest) -> TodoTaskResponse:
        col = get_todo_tasks_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        now = datetime.utcnow()
        doc = {
            "user_id": user_id,
            "section_id": req.section_id if (req.section_id and ObjectId.is_valid(req.section_id)) else None,
            "title": req.title.strip(),
            "difficulty_points": req.difficulty_points if req.difficulty_points in (1, 2, 3, 5) else 1,
            "repeat": req.repeat,
            "due_date": req.due_date,
            "notes": req.notes.strip() if req.notes else None,
            "is_completed": False,
            "completed_at": None,
            "created_at": now,
            "updated_at": now
        }
        res = await col.insert_one(doc)
        doc["_id"] = res.inserted_id
        sec_resp = await self._populate_section(user_id, doc["section_id"])
        return self._doc_to_todo_task(doc, sec_resp)

    async def update_todo_task(
        self,
        user_id: str,
        task_id: str,
        req: TodoTaskUpdateRequest
    ) -> Optional[TodoTaskResponse]:
        col = get_todo_tasks_collection()
        if col is None or not ObjectId.is_valid(task_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}
        if req.title is not None:
            update_data["title"] = req.title.strip()
        if req.section_id is not None:
            update_data["section_id"] = req.section_id if (req.section_id and ObjectId.is_valid(req.section_id)) else None
        if req.difficulty_points is not None:
            update_data["difficulty_points"] = req.difficulty_points
        if req.repeat is not None:
            update_data["repeat"] = req.repeat
        if req.due_date is not None:
            update_data["due_date"] = req.due_date
        if req.notes is not None:
            update_data["notes"] = req.notes.strip()
        if req.is_completed is not None:
            update_data["is_completed"] = req.is_completed
            if req.is_completed:
                update_data["completed_at"] = datetime.utcnow()
            else:
                update_data["completed_at"] = None

        res = await col.find_one_and_update(
            {"_id": ObjectId(task_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        sec_resp = await self._populate_section(user_id, res.get("section_id"))
        return self._doc_to_todo_task(res, sec_resp)

    async def toggle_todo_task(
        self,
        user_id: str,
        task_id: str,
        req: TodoTaskToggleRequest
    ) -> Optional[TodoTaskResponse]:
        col = get_todo_tasks_collection()
        if col is None or not ObjectId.is_valid(task_id):
            return None

        now = datetime.utcnow()
        update_data: Dict[str, Any] = {
            "is_completed": req.is_completed,
            "completed_at": now if req.is_completed else None,
            "updated_at": now
        }

        res = await col.find_one_and_update(
            {"_id": ObjectId(task_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        sec_resp = await self._populate_section(user_id, res.get("section_id"))
        return self._doc_to_todo_task(res, sec_resp)

    async def delete_todo_task(self, user_id: str, task_id: str) -> bool:
        col = get_todo_tasks_collection()
        if col is None or not ObjectId.is_valid(task_id):
            return False
        res = await col.delete_one({"_id": ObjectId(task_id), "user_id": user_id})
        return res.deleted_count > 0


lists_service = ListsService()
