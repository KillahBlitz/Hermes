import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from bson import ObjectId
from src.database.mongo import (
    get_board_epics_collection,
    get_board_habits_collection,
    get_board_sticky_notes_collection,
    get_board_tasks_collection,
)
from src.models.request.boards import (
    EpicCreateRequest,
    EpicUpdateRequest,
    HabitCheckDayRequest,
    HabitCreateRequest,
    HabitUpdateRequest,
    StickyNoteCreateRequest,
    StickyNotePositionRequest,
    StickyNoteUpdateRequest,
    TaskCreateRequest,
    TaskLocationUpdateRequest,
    TaskStatusUpdateRequest,
    TaskUpdateRequest,
)
from src.models.response.boards import (
    EpicListResponse,
    EpicResponse,
    HabitDayInfo,
    HabitListResponse,
    HabitResponse,
    KanbanBoardResponse,
    StickyNoteListResponse,
    StickyNoteResponse,
    TaskListResponse,
    TaskResponse,
)

logger = logging.getLogger("hermes-api.boards")

DEFAULT_EPICS = [
    {
        "name": "Escuela",
        "description": "Actividades académicas, proyectos escolares y entregas de estudio",
        "color": "#118AB2",
        "icon": "🎓",
        "is_default": True
    },
    {
        "name": "Trabajo",
        "description": "Proyectos profesionales, tareas laborales y entregables",
        "color": "#00E5FF",
        "icon": "💼",
        "is_default": True
    },
    {
        "name": "Cursos",
        "description": "Cursos, capacitaciones, certificaciones y desarrollo personal",
        "color": "#7209B7",
        "icon": "📚",
        "is_default": True
    }
]


class BoardService:

    # ─────────────────────────────────────────────────────────────
    # ÉPICAS
    # ─────────────────────────────────────────────────────────────

    async def ensure_default_epics(self, user_id: str) -> None:
        """Asegura que el usuario tenga sembradas las 3 épicas predeterminadas sin duplicados."""
        col = get_board_epics_collection()
        if col is None:
            return

        now = datetime.utcnow()
        for ep in DEFAULT_EPICS:
            await col.update_one(
                {"user_id": user_id, "name": ep["name"]},
                {
                    "$setOnInsert": {
                        "user_id": user_id,
                        "name": ep["name"],
                        "description": ep["description"],
                        "color": ep["color"],
                        "icon": ep["icon"],
                        "is_default": True,
                        "created_at": now,
                        "updated_at": now,
                    }
                },
                upsert=True
            )

        # Limpieza de duplicados residuales si existieran
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": "$name", "ids": {"$push": "$_id"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}
        ]
        async for dup in col.aggregate(pipeline):
            ids_to_remove = dup["ids"][1:]
            if ids_to_remove:
                await col.delete_many({"_id": {"$in": ids_to_remove}})

    async def list_epics(self, user_id: str) -> List[EpicResponse]:
        await self.ensure_default_epics(user_id)
        col_epics = get_board_epics_collection()
        col_tasks = get_board_tasks_collection()
        if col_epics is None:
            return []

        cursor = col_epics.find({"user_id": user_id}).sort([("is_default", -1), ("name", 1)])
        epics = []
        async for doc in cursor:
            epic_id_str = str(doc["_id"])
            count = 0
            if col_tasks is not None:
                count = await col_tasks.count_documents({"user_id": user_id, "epic_id": epic_id_str})

            epics.append(EpicResponse(
                id=epic_id_str,
                user_id=doc.get("user_id"),
                name=doc["name"],
                description=doc.get("description"),
                color=doc.get("color", "#00E5FF"),
                icon=doc.get("icon", "💼"),
                is_default=doc.get("is_default", False),
                created_at=doc.get("created_at"),
                task_count=count
            ))
        return epics

    async def create_epic(self, user_id: str, req: EpicCreateRequest) -> EpicResponse:
        col = get_board_epics_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        # Comprobar si ya existe con el mismo nombre
        existing = await col.find_one({
            "user_id": user_id,
            "name": {"$regex": f"^{req.name.strip()}$", "$options": "i"}
        })
        if existing:
            return EpicResponse(
                id=str(existing["_id"]),
                user_id=existing.get("user_id"),
                name=existing["name"],
                description=existing.get("description"),
                color=existing.get("color", req.color),
                icon=existing.get("icon", req.icon),
                is_default=existing.get("is_default", False),
                created_at=existing.get("created_at"),
                task_count=0
            )

        now = datetime.utcnow()
        doc = {
            "user_id": user_id,
            "name": req.name.strip(),
            "description": req.description.strip() if req.description else None,
            "color": req.color,
            "icon": req.icon,
            "is_default": False,
            "created_at": now,
            "updated_at": now,
        }
        res = await col.insert_one(doc)
        return EpicResponse(
            id=str(res.inserted_id),
            user_id=user_id,
            name=doc["name"],
            description=doc["description"],
            color=doc["color"],
            icon=doc["icon"],
            is_default=False,
            created_at=now,
            task_count=0
        )

    async def update_epic(self, user_id: str, epic_id: str, req: EpicUpdateRequest) -> Optional[EpicResponse]:
        col = get_board_epics_collection()
        if col is None or not ObjectId.is_valid(epic_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}
        if req.name is not None:
            update_data["name"] = req.name.strip()
        if req.description is not None:
            update_data["description"] = req.description.strip()
        if req.color is not None:
            update_data["color"] = req.color
        if req.icon is not None:
            update_data["icon"] = req.icon

        res = await col.find_one_and_update(
            {"_id": ObjectId(epic_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        return EpicResponse(
            id=str(res["_id"]),
            user_id=res.get("user_id"),
            name=res["name"],
            description=res.get("description"),
            color=res.get("color", "#00E5FF"),
            icon=res.get("icon", "💼"),
            is_default=res.get("is_default", False),
            created_at=res.get("created_at"),
            task_count=0
        )

    async def delete_epic(self, user_id: str, epic_id: str) -> bool:
        col_epics = get_board_epics_collection()
        col_tasks = get_board_tasks_collection()
        if col_epics is None or not ObjectId.is_valid(epic_id):
            return False

        # Desvincular épica de las tareas asociadas
        if col_tasks is not None:
            await col_tasks.update_many(
                {"user_id": user_id, "epic_id": epic_id},
                {"$set": {"epic_id": None, "updated_at": datetime.utcnow()}}
            )

        res = await col_epics.delete_one({"_id": ObjectId(epic_id), "user_id": user_id})
        return res.deleted_count > 0

    # ─────────────────────────────────────────────────────────────
    # TAREAS & KANBAN (CON REGLA DE 7 DÍAS EN DONE)
    # ─────────────────────────────────────────────────────────────

    async def _populate_epic(self, user_id: str, epic_id: Optional[str]) -> Optional[EpicResponse]:
        if not epic_id or not ObjectId.is_valid(epic_id):
            return None
        col = get_board_epics_collection()
        if col is None:
            return None
        doc = await col.find_one({"_id": ObjectId(epic_id), "user_id": user_id})
        if not doc:
            return None
        return EpicResponse(
            id=str(doc["_id"]),
            user_id=doc.get("user_id"),
            name=doc["name"],
            description=doc.get("description"),
            color=doc.get("color", "#00E5FF"),
            icon=doc.get("icon", "💼"),
            is_default=doc.get("is_default", False),
            created_at=doc.get("created_at")
        )

    def _doc_to_task(self, doc: Dict[str, Any], epic_resp: Optional[EpicResponse] = None) -> TaskResponse:
        completed_at = doc.get("completed_at")
        days_since_comp = None
        if completed_at:
            delta = datetime.utcnow() - completed_at
            days_since_comp = max(0, delta.days)

        return TaskResponse(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            title=doc["title"],
            description=doc.get("description"),
            type=doc.get("type", "IMPROVEMENT"),
            complexity=doc.get("complexity", "M"),
            epic_id=doc.get("epic_id"),
            epic=epic_resp,
            status=doc.get("status", "TODO"),
            location=doc.get("location", "BOARD"),
            order=doc.get("order", 0),
            due_date=doc.get("due_date"),
            completed_at=completed_at,
            days_since_completion=days_since_comp,
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at")
        )

    async def create_task(self, user_id: str, req: TaskCreateRequest) -> TaskResponse:
        col = get_board_tasks_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        now = datetime.utcnow()
        completed_at = now if req.status == "DONE" else None

        doc = {
            "user_id": user_id,
            "title": req.title.strip(),
            "description": req.description.strip() if req.description else None,
            "type": req.type,
            "complexity": req.complexity,
            "epic_id": req.epic_id if (req.epic_id and ObjectId.is_valid(req.epic_id)) else None,
            "status": req.status,
            "location": req.location,
            "order": 0,
            "due_date": req.due_date,
            "completed_at": completed_at,
            "created_at": now,
            "updated_at": now,
        }
        res = await col.insert_one(doc)
        epic_resp = await self._populate_epic(user_id, doc["epic_id"])
        doc["_id"] = res.inserted_id
        return self._doc_to_task(doc, epic_resp)

    async def update_task(self, user_id: str, task_id: str, req: TaskUpdateRequest) -> Optional[TaskResponse]:
        col = get_board_tasks_collection()
        if col is None or not ObjectId.is_valid(task_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}
        if req.title is not None:
            update_data["title"] = req.title.strip()
        if req.description is not None:
            update_data["description"] = req.description.strip()
        if req.type is not None:
            update_data["type"] = req.type
        if req.complexity is not None:
            update_data["complexity"] = req.complexity
        if req.epic_id is not None:
            update_data["epic_id"] = req.epic_id if (req.epic_id and ObjectId.is_valid(req.epic_id)) else None
        if req.location is not None:
            update_data["location"] = req.location
        if req.due_date is not None:
            update_data["due_date"] = req.due_date

        if req.status is not None:
            update_data["status"] = req.status
            if req.status == "DONE":
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

        epic_resp = await self._populate_epic(user_id, res.get("epic_id"))
        return self._doc_to_task(res, epic_resp)

    async def update_task_status(self, user_id: str, task_id: str, req: TaskStatusUpdateRequest) -> Optional[TaskResponse]:
        col = get_board_tasks_collection()
        if col is None or not ObjectId.is_valid(task_id):
            return None

        now = datetime.utcnow()
        update_data: Dict[str, Any] = {
            "status": req.status,
            "updated_at": now
        }
        if req.status == "DONE":
            update_data["completed_at"] = now
        else:
            update_data["completed_at"] = None

        res = await col.find_one_and_update(
            {"_id": ObjectId(task_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        epic_resp = await self._populate_epic(user_id, res.get("epic_id"))
        return self._doc_to_task(res, epic_resp)

    async def update_task_location(self, user_id: str, task_id: str, req: TaskLocationUpdateRequest) -> Optional[TaskResponse]:
        col = get_board_tasks_collection()
        if col is None or not ObjectId.is_valid(task_id):
            return None

        res = await col.find_one_and_update(
            {"_id": ObjectId(task_id), "user_id": user_id},
            {"$set": {"location": req.location, "updated_at": datetime.utcnow()}},
            return_document=True
        )
        if not res:
            return None

        epic_resp = await self._populate_epic(user_id, res.get("epic_id"))
        return self._doc_to_task(res, epic_resp)

    async def delete_task(self, user_id: str, task_id: str) -> bool:
        col = get_board_tasks_collection()
        if col is None or not ObjectId.is_valid(task_id):
            return False
        res = await col.delete_one({"_id": ObjectId(task_id), "user_id": user_id})
        return res.deleted_count > 0

    async def get_kanban_board(
        self,
        user_id: str,
        epic_id: Optional[str] = None,
        type_filter: Optional[str] = None,
        search: Optional[str] = None
    ) -> KanbanBoardResponse:
        """
        Retorna las 4 columnas del tablero activo (TODO, IN_PROGRESS, TESTING, DONE).
        Aplica la regla de los 7 días: las tareas en DONE con más de 7 días se cuentan como
        archived_count y se excluyen de la columna activa 'done'.
        """
        col = get_board_tasks_collection()
        if col is None:
            return KanbanBoardResponse(todo=[], in_progress=[], testing=[], done=[], total_active=0, archived_count=0)

        query: Dict[str, Any] = {"user_id": user_id, "location": "BOARD"}
        if epic_id and ObjectId.is_valid(epic_id):
            query["epic_id"] = epic_id
        if type_filter and type_filter in ("IMPROVEMENT", "URGENT", "PENDING", "ANALYSIS"):
            query["type"] = type_filter
        if search and search.strip():
            query["title"] = {"$regex": search.strip(), "$options": "i"}

        epics_map = {e.id: e for e in await self.list_epics(user_id)}
        now = datetime.utcnow()
        seven_days_ago = now - timedelta(days=7)

        cursor = col.find(query).sort([("order", 1), ("created_at", -1)])
        todo: List[TaskResponse] = []
        in_progress: List[TaskResponse] = []
        testing: List[TaskResponse] = []
        done: List[TaskResponse] = []
        archived_count = 0

        async for doc in cursor:
            epic_resp = epics_map.get(doc.get("epic_id"))
            task_resp = self._doc_to_task(doc, epic_resp)

            st = doc.get("status", "TODO")
            if st == "TODO":
                todo.append(task_resp)
            elif st == "IN_PROGRESS":
                in_progress.append(task_resp)
            elif st == "TESTING":
                testing.append(task_resp)
            elif st == "DONE":
                comp_at = doc.get("completed_at")
                if comp_at and comp_at < seven_days_ago:
                    archived_count += 1
                else:
                    done.append(task_resp)

        total_active = len(todo) + len(in_progress) + len(testing) + len(done)
        return KanbanBoardResponse(
            todo=todo,
            in_progress=in_progress,
            testing=testing,
            done=done,
            total_active=total_active,
            archived_count=archived_count
        )

    async def get_backlog_tasks(
        self,
        user_id: str,
        epic_id: Optional[str] = None,
        type_filter: Optional[str] = None,
        search: Optional[str] = None
    ) -> TaskListResponse:
        col = get_board_tasks_collection()
        if col is None:
            return TaskListResponse(tasks=[], total=0)

        query: Dict[str, Any] = {"user_id": user_id, "location": "BACKLOG"}
        if epic_id and ObjectId.is_valid(epic_id):
            query["epic_id"] = epic_id
        if type_filter and type_filter in ("IMPROVEMENT", "URGENT", "PENDING", "ANALYSIS"):
            query["type"] = type_filter
        if search and search.strip():
            query["title"] = {"$regex": search.strip(), "$options": "i"}

        epics_map = {e.id: e for e in await self.list_epics(user_id)}
        cursor = col.find(query).sort([("created_at", -1)])
        tasks = []
        async for doc in cursor:
            epic_resp = epics_map.get(doc.get("epic_id"))
            tasks.append(self._doc_to_task(doc, epic_resp))

        return TaskListResponse(tasks=tasks, total=len(tasks))

    async def get_archived_tasks(
        self,
        user_id: str,
        epic_id: Optional[str] = None,
        search: Optional[str] = None
    ) -> TaskListResponse:
        """Retorna las tareas completadas hace más de 7 días."""
        col = get_board_tasks_collection()
        if col is None:
            return TaskListResponse(tasks=[], total=0)

        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        query: Dict[str, Any] = {
            "user_id": user_id,
            "status": "DONE",
            "completed_at": {"$lt": seven_days_ago}
        }
        if epic_id and ObjectId.is_valid(epic_id):
            query["epic_id"] = epic_id
        if search and search.strip():
            query["title"] = {"$regex": search.strip(), "$options": "i"}

        epics_map = {e.id: e for e in await self.list_epics(user_id)}
        cursor = col.find(query).sort([("completed_at", -1)])
        tasks = []
        async for doc in cursor:
            epic_resp = epics_map.get(doc.get("epic_id"))
            tasks.append(self._doc_to_task(doc, epic_resp))

        return TaskListResponse(tasks=tasks, total=len(tasks))

    # ─────────────────────────────────────────────────────────────
    # HÁBITOS (MÉTODO 21 DÍAS)
    # ─────────────────────────────────────────────────────────────

    def _doc_to_habit(self, doc: Dict[str, Any]) -> HabitResponse:
        raw_days = doc.get("days", [])
        days_info = []
        total_comp = 0
        current_streak = 0

        # Ordenar días del 1 al 21
        sorted_days = sorted(raw_days, key=lambda d: d.get("day_number", 0))
        counting_streak = True

        for d in sorted_days:
            st = d.get("status", "PENDING")
            days_info.append(HabitDayInfo(
                day_number=d.get("day_number", 1),
                status=st,
                date=d.get("date")
            ))
            if st == "COMPLETED":
                total_comp += 1
                if counting_streak:
                    current_streak += 1
            else:
                counting_streak = False

        pct = round((total_comp / 21) * 100, 1)
        is_consolidated = total_comp >= 21

        return HabitResponse(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            title=doc["title"],
            description=doc.get("description"),
            icon=doc.get("icon", "⚡"),
            color=doc.get("color", "#00FFC6"),
            start_date=doc.get("start_date"),
            days=days_info,
            current_streak=current_streak,
            total_completed=total_comp,
            completion_percentage=pct,
            is_consolidated=is_consolidated,
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at")
        )

    async def list_habits(self, user_id: str) -> List[HabitResponse]:
        col = get_board_habits_collection()
        if col is None:
            return []

        cursor = col.find({"user_id": user_id}).sort([("created_at", -1)])
        habits = []
        async for doc in cursor:
            habits.append(self._doc_to_habit(doc))
        return habits

    async def create_habit(self, user_id: str, req: HabitCreateRequest) -> HabitResponse:
        col = get_board_habits_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        now = datetime.utcnow()
        # Generar las 21 casillas de días
        days = []
        for i in range(1, 22):
            days.append({
                "day_number": i,
                "status": "PENDING",
                "date": None
            })

        doc = {
            "user_id": user_id,
            "title": req.title.strip(),
            "description": req.description.strip() if req.description else None,
            "icon": req.icon,
            "color": req.color,
            "start_date": now,
            "days": days,
            "current_streak": 0,
            "total_completed": 0,
            "is_consolidated": False,
            "created_at": now,
            "updated_at": now,
        }
        res = await col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._doc_to_habit(doc)

    async def update_habit(self, user_id: str, habit_id: str, req: HabitUpdateRequest) -> Optional[HabitResponse]:
        col = get_board_habits_collection()
        if col is None or not ObjectId.is_valid(habit_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}
        if req.title is not None:
            update_data["title"] = req.title.strip()
        if req.description is not None:
            update_data["description"] = req.description.strip()
        if req.icon is not None:
            update_data["icon"] = req.icon
        if req.color is not None:
            update_data["color"] = req.color

        res = await col.find_one_and_update(
            {"_id": ObjectId(habit_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        return self._doc_to_habit(res)

    async def check_habit_day(self, user_id: str, habit_id: str, req: HabitCheckDayRequest) -> Optional[HabitResponse]:
        col = get_board_habits_collection()
        if col is None or not ObjectId.is_valid(habit_id):
            return None

        habit_doc = await col.find_one({"_id": ObjectId(habit_id), "user_id": user_id})
        if not habit_doc:
            return None

        days = habit_doc.get("days", [])
        day_found = False
        today_str = datetime.utcnow().strftime("%Y-%m-%d")

        for d in days:
            if d.get("day_number") == req.day_number:
                d["status"] = req.status
                d["date"] = today_str if req.status == "COMPLETED" else None
                day_found = True
                break

        if not day_found:
            days.append({
                "day_number": req.day_number,
                "status": req.status,
                "date": today_str if req.status == "COMPLETED" else None
            })

        # Recalcular métricas
        total_comp = sum(1 for d in days if d.get("status") == "COMPLETED")
        is_cons = total_comp >= 21

        res = await col.find_one_and_update(
            {"_id": ObjectId(habit_id), "user_id": user_id},
            {
                "$set": {
                    "days": days,
                    "total_completed": total_comp,
                    "is_consolidated": is_cons,
                    "updated_at": datetime.utcnow()
                }
            },
            return_document=True
        )
        if not res:
            return None

        return self._doc_to_habit(res)

    async def delete_habit(self, user_id: str, habit_id: str) -> bool:
        col = get_board_habits_collection()
        if col is None or not ObjectId.is_valid(habit_id):
            return False
        res = await col.delete_one({"_id": ObjectId(habit_id), "user_id": user_id})
        return res.deleted_count > 0

    # ─────────────────────────────────────────────────────────────
    # PIZARRÓN DE IDEAS (STICKY NOTES LIBRES)
    # ─────────────────────────────────────────────────────────────

    def _doc_to_note(self, doc: Dict[str, Any]) -> StickyNoteResponse:
        return StickyNoteResponse(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            title=doc.get("title", ""),
            content=doc.get("content", ""),
            color=doc.get("color", "#FFD166"),
            x=float(doc.get("x", 100)),
            y=float(doc.get("y", 100)),
            z_index=int(doc.get("z_index", 1)),
            rotation=float(doc.get("rotation", 0.0)),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at")
        )

    async def list_sticky_notes(self, user_id: str) -> List[StickyNoteResponse]:
        col = get_board_sticky_notes_collection()
        if col is None:
            return []

        cursor = col.find({"user_id": user_id}).sort([("z_index", 1), ("created_at", 1)])
        notes = []
        async for doc in cursor:
            notes.append(self._doc_to_note(doc))
        return notes

    async def create_sticky_note(self, user_id: str, req: StickyNoteCreateRequest) -> StickyNoteResponse:
        col = get_board_sticky_notes_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        now = datetime.utcnow()
        # Generar rotación realista aleatoria entre -2.0 y 2.0 grados
        rot = round(random.uniform(-2.2, 2.2), 1)

        # Buscar el max z_index actual
        max_z = 1
        last_note = await col.find_one({"user_id": user_id}, sort=[("z_index", -1)])
        if last_note and "z_index" in last_note:
            max_z = int(last_note["z_index"]) + 1

        doc = {
            "user_id": user_id,
            "title": req.title.strip() if req.title else "",
            "content": req.content.strip(),
            "color": req.color,
            "x": req.x,
            "y": req.y,
            "z_index": max_z,
            "rotation": rot,
            "created_at": now,
            "updated_at": now,
        }
        res = await col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._doc_to_note(doc)

    async def update_sticky_note(self, user_id: str, note_id: str, req: StickyNoteUpdateRequest) -> Optional[StickyNoteResponse]:
        col = get_board_sticky_notes_collection()
        if col is None or not ObjectId.is_valid(note_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}
        if req.title is not None:
            update_data["title"] = req.title.strip()
        if req.content is not None:
            update_data["content"] = req.content.strip()
        if req.color is not None:
            update_data["color"] = req.color

        res = await col.find_one_and_update(
            {"_id": ObjectId(note_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        return self._doc_to_note(res)

    async def update_sticky_note_position(self, user_id: str, note_id: str, req: StickyNotePositionRequest) -> Optional[StickyNoteResponse]:
        col = get_board_sticky_notes_collection()
        if col is None or not ObjectId.is_valid(note_id):
            return None

        update_data: Dict[str, Any] = {
            "x": req.x,
            "y": req.y,
            "updated_at": datetime.utcnow()
        }
        if req.z_index is not None:
            update_data["z_index"] = req.z_index

        res = await col.find_one_and_update(
            {"_id": ObjectId(note_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        return self._doc_to_note(res)

    async def delete_sticky_note(self, user_id: str, note_id: str) -> bool:
        col = get_board_sticky_notes_collection()
        if col is None or not ObjectId.is_valid(note_id):
            return False
        res = await col.delete_one({"_id": ObjectId(note_id), "user_id": user_id})
        return res.deleted_count > 0


board_service = BoardService()
