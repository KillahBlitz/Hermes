import logging
import re
import unicodedata
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from bson import ObjectId
from src.database.mongo import (
    get_progress_milestones_collection,
    get_progress_notes_collection,
    get_progress_roadmaps_collection,
)
from src.models.request.progress import (
    MilestoneCreateRequest,
    MilestoneTopicToggleRequest,
    MilestoneUpdateRequest,
    NoteCreateRequest,
    NoteUpdateRequest,
    RoadmapCreateRequest,
    RoadmapUpdateRequest,
)
from src.models.response.progress import (
    BacklinkItemResponse,
    GraphEdgeResponse,
    GraphNodeResponse,
    KnowledgeGraphResponse,
    MilestoneListResponse,
    MilestoneResponse,
    MilestoneTopicResponse,
    NoteListResponse,
    NoteResponse,
    RoadmapEdgeResponse,
    RoadmapListResponse,
    RoadmapNodeResponse,
    RoadmapResponse,
)

logger = logging.getLogger("hermes-api.progress")


def slugify(value: str) -> str:
    """Convierte un texto en un slug normalizado."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower()).strip()
    return re.sub(r"[-\s]+", "-", value)


def extract_wikilinks(content_md: str) -> List[str]:
    """Extrae todos los wikilinks [[Nombre de Nota]] del texto en Markdown."""
    if not content_md:
        return []
    matches = re.findall(r"\[\[(.*?)\]\]", content_md)
    seen: Set[str] = set()
    result: List[str] = []
    for m in matches:
        clean = m.strip()
        if clean and clean.lower() not in seen:
            seen.add(clean.lower())
            result.append(clean)
    return result


def extract_tags(content_md: str) -> List[str]:
    """Extrae todos los hashtags (#tag) del texto en Markdown."""
    if not content_md:
        return []
    matches = re.findall(r"(?<!\S)#([a-zA-Z0-9_\-]+)", content_md)
    seen: Set[str] = set()
    result: List[str] = []
    for t in matches:
        clean = t.strip().lower()
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)
    return result


class ProgressService:

    # ─────────────────────────────────────────────────────────────
    # 1. ÁRBOL DE MAPAS (ROADMAPS)
    # ─────────────────────────────────────────────────────────────

    def _doc_to_roadmap(self, doc: Dict[str, Any], notes_map: Dict[str, str] = {}) -> RoadmapResponse:
        nodes = []
        for n in doc.get("nodes", []):
            note_id = n.get("note_id")
            note_title = notes_map.get(str(note_id)) if note_id else None
            nodes.append(RoadmapNodeResponse(
                id=n["id"],
                title=n["title"],
                icon=n.get("icon", "⚡"),
                color=n.get("color", "#00E5FF"),
                status=n.get("status", "PENDIENTE"),
                x=float(n.get("x", 100.0)),
                y=float(n.get("y", 100.0)),
                description=n.get("description"),
                note_id=note_id,
                note_title=note_title
            ))

        edges = []
        for e in doc.get("edges", []):
            edges.append(RoadmapEdgeResponse(
                id=e["id"],
                source_node_id=e["source_node_id"],
                target_node_id=e["target_node_id"],
                label=e.get("label")
            ))

        return RoadmapResponse(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            title=doc["title"],
            description=doc.get("description"),
            category=doc.get("category", "General"),
            color=doc.get("color", "#00FFC6"),
            nodes=nodes,
            edges=edges,
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at")
        )

    async def _get_user_notes_map(self, user_id: str) -> Dict[str, str]:
        col = get_progress_notes_collection()
        if col is None:
            return {}
        cursor = col.find({"user_id": user_id}, {"_id": 1, "title": 1})
        res = {}
        async for doc in cursor:
            res[str(doc["_id"])] = doc["title"]
        return res

    async def list_roadmaps(self, user_id: str) -> RoadmapListResponse:
        col = get_progress_roadmaps_collection()
        if col is None:
            return RoadmapListResponse(roadmaps=[], total=0)

        notes_map = await self._get_user_notes_map(user_id)
        cursor = col.find({"user_id": user_id}).sort([("updated_at", -1)])
        roadmaps = []
        async for doc in cursor:
            roadmaps.append(self._doc_to_roadmap(doc, notes_map))

        return RoadmapListResponse(roadmaps=roadmaps, total=len(roadmaps))

    async def get_roadmap(self, user_id: str, roadmap_id: str) -> Optional[RoadmapResponse]:
        col = get_progress_roadmaps_collection()
        if col is None or not ObjectId.is_valid(roadmap_id):
            return None

        doc = await col.find_one({"_id": ObjectId(roadmap_id), "user_id": user_id})
        if not doc:
            return None

        notes_map = await self._get_user_notes_map(user_id)
        return self._doc_to_roadmap(doc, notes_map)

    async def create_roadmap(self, user_id: str, req: RoadmapCreateRequest) -> RoadmapResponse:
        col = get_progress_roadmaps_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        now = datetime.utcnow()
        nodes_data = [n.model_dump() for n in req.nodes]
        edges_data = [e.model_dump() for e in req.edges]

        doc = {
            "user_id": user_id,
            "title": req.title.strip(),
            "description": req.description.strip() if req.description else None,
            "category": req.category.strip(),
            "color": req.color,
            "nodes": nodes_data,
            "edges": edges_data,
            "created_at": now,
            "updated_at": now
        }
        res = await col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._doc_to_roadmap(doc)

    async def update_roadmap(
        self,
        user_id: str,
        roadmap_id: str,
        req: RoadmapUpdateRequest
    ) -> Optional[RoadmapResponse]:
        col = get_progress_roadmaps_collection()
        if col is None or not ObjectId.is_valid(roadmap_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}
        if req.title is not None:
            update_data["title"] = req.title.strip()
        if req.description is not None:
            update_data["description"] = req.description.strip()
        if req.category is not None:
            update_data["category"] = req.category.strip()
        if req.color is not None:
            update_data["color"] = req.color
        if req.nodes is not None:
            update_data["nodes"] = [n.model_dump() for n in req.nodes]
        if req.edges is not None:
            update_data["edges"] = [e.model_dump() for e in req.edges]

        res = await col.find_one_and_update(
            {"_id": ObjectId(roadmap_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        notes_map = await self._get_user_notes_map(user_id)
        return self._doc_to_roadmap(res, notes_map)

    async def delete_roadmap(self, user_id: str, roadmap_id: str) -> bool:
        col = get_progress_roadmaps_collection()
        if col is None or not ObjectId.is_valid(roadmap_id):
            return False
        res = await col.delete_one({"_id": ObjectId(roadmap_id), "user_id": user_id})
        return res.deleted_count > 0

    # ─────────────────────────────────────────────────────────────
    # 2. GESTOR DE HITOS (MILESTONES TRACKER)
    # ─────────────────────────────────────────────────────────────

    def _doc_to_milestone(self, doc: Dict[str, Any]) -> MilestoneResponse:
        raw_topics = doc.get("topics", [])
        topics = []
        completed_count = 0

        for t in raw_topics:
            is_comp = bool(t.get("is_completed", False))
            if is_comp:
                completed_count += 1
            topics.append(MilestoneTopicResponse(
                id=t["id"],
                title=t["title"],
                is_completed=is_comp,
                completed_at=t.get("completed_at")
            ))

        total_topics = len(topics)
        progress_pct = (completed_count / total_topics * 100.0) if total_topics > 0 else 0.0

        target_date: datetime = doc["target_date"]
        # Calcular días restantes
        now = datetime.utcnow()
        diff = target_date.date() - now.date()
        days_remaining = diff.days
        status = doc.get("status", "IN_PROGRESS")
        is_overdue = days_remaining < 0 and status != "COMPLETED"

        return MilestoneResponse(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            title=doc["title"],
            category=doc.get("category", "PROYECTO"),
            icon=doc.get("icon", "🎯"),
            color=doc.get("color", "#00FFC6"),
            target_date=target_date,
            description=doc.get("description"),
            topics=topics,
            total_topics=total_topics,
            completed_topics=completed_count,
            progress_percentage=round(progress_pct, 1),
            days_remaining=days_remaining,
            is_overdue=is_overdue,
            status=status,
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at")
        )

    async def list_milestones(
        self,
        user_id: str,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> MilestoneListResponse:
        col = get_progress_milestones_collection()
        if col is None:
            return MilestoneListResponse(milestones=[], total=0, active_count=0, completed_count=0)

        query: Dict[str, Any] = {"user_id": user_id}
        if category and category.strip():
            query["category"] = category.strip().upper()
        if status and status in ("IN_PROGRESS", "COMPLETED", "ARCHIVED"):
            query["status"] = status

        cursor = col.find(query).sort([("target_date", 1)])
        milestones = []
        active_count = 0
        completed_count = 0

        async for doc in cursor:
            m = self._doc_to_milestone(doc)
            milestones.append(m)
            if m.status == "COMPLETED":
                completed_count += 1
            else:
                active_count += 1

        return MilestoneListResponse(
            milestones=milestones,
            total=len(milestones),
            active_count=active_count,
            completed_count=completed_count
        )

    async def create_milestone(self, user_id: str, req: MilestoneCreateRequest) -> MilestoneResponse:
        col = get_progress_milestones_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        now = datetime.utcnow()
        topics_data = [t.model_dump() for t in req.topics]

        doc = {
            "user_id": user_id,
            "title": req.title.strip(),
            "category": req.category.strip().upper(),
            "icon": req.icon,
            "color": req.color,
            "target_date": req.target_date,
            "description": req.description.strip() if req.description else None,
            "topics": topics_data,
            "status": "IN_PROGRESS",
            "created_at": now,
            "updated_at": now
        }
        res = await col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._doc_to_milestone(doc)

    async def update_milestone(
        self,
        user_id: str,
        milestone_id: str,
        req: MilestoneUpdateRequest
    ) -> Optional[MilestoneResponse]:
        col = get_progress_milestones_collection()
        if col is None or not ObjectId.is_valid(milestone_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}
        if req.title is not None:
            update_data["title"] = req.title.strip()
        if req.category is not None:
            update_data["category"] = req.category.strip().upper()
        if req.icon is not None:
            update_data["icon"] = req.icon
        if req.color is not None:
            update_data["color"] = req.color
        if req.target_date is not None:
            update_data["target_date"] = req.target_date
        if req.description is not None:
            update_data["description"] = req.description.strip()
        if req.topics is not None:
            update_data["topics"] = [t.model_dump() for t in req.topics]
        if req.status is not None:
            update_data["status"] = req.status

        res = await col.find_one_and_update(
            {"_id": ObjectId(milestone_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None
        return self._doc_to_milestone(res)

    async def toggle_milestone_topic(
        self,
        user_id: str,
        milestone_id: str,
        topic_id: str,
        req: MilestoneTopicToggleRequest
    ) -> Optional[MilestoneResponse]:
        col = get_progress_milestones_collection()
        if col is None or not ObjectId.is_valid(milestone_id):
            return None

        doc = await col.find_one({"_id": ObjectId(milestone_id), "user_id": user_id})
        if not doc:
            return None

        topics = doc.get("topics", [])
        found = False
        all_completed = True
        now = datetime.utcnow()

        for t in topics:
            if t["id"] == topic_id:
                t["is_completed"] = req.is_completed
                t["completed_at"] = now if req.is_completed else None
                found = True
            if not t.get("is_completed", False):
                all_completed = False

        if not found:
            return None

        new_status = "COMPLETED" if (all_completed and len(topics) > 0) else "IN_PROGRESS"

        res = await col.find_one_and_update(
            {"_id": ObjectId(milestone_id), "user_id": user_id},
            {
                "$set": {
                    "topics": topics,
                    "status": new_status,
                    "updated_at": now
                }
            },
            return_document=True
        )
        if not res:
            return None
        return self._doc_to_milestone(res)

    async def delete_milestone(self, user_id: str, milestone_id: str) -> bool:
        col = get_progress_milestones_collection()
        if col is None or not ObjectId.is_valid(milestone_id):
            return False
        res = await col.delete_one({"_id": ObjectId(milestone_id), "user_id": user_id})
        return res.deleted_count > 0

    # ─────────────────────────────────────────────────────────────
    # 3. BÓVEDA ZETTELKASTEN (MARKDOWN NOTES, WIKILINKS & GRAPH)
    # ─────────────────────────────────────────────────────────────

    async def _compute_backlinks(self, user_id: str, note_title: str, current_note_id: str) -> List[BacklinkItemResponse]:
        col = get_progress_notes_collection()
        if col is None:
            return []

        # Buscar todas las notas que tengan en 'outgoing_links' el título de esta nota
        cursor = col.find({
            "user_id": user_id,
            "_id": {"$ne": ObjectId(current_note_id)},
            "outgoing_links": {"$regex": f"^{re.escape(note_title.strip())}$", "$options": "i"}
        }, {"_id": 1, "title": 1, "slug": 1})

        backlinks = []
        async for doc in cursor:
            backlinks.append(BacklinkItemResponse(
                id=str(doc["_id"]),
                title=doc["title"],
                slug=doc.get("slug", slugify(doc["title"]))
            ))
        return backlinks

    async def _doc_to_note(self, doc: Dict[str, Any]) -> NoteResponse:
        note_id = str(doc["_id"])
        user_id = doc["user_id"]
        title = doc["title"]
        backlinks = await self._compute_backlinks(user_id, title, note_id)

        return NoteResponse(
            id=note_id,
            user_id=user_id,
            title=title,
            slug=doc.get("slug", slugify(title)),
            content_md=doc.get("content_md", ""),
            tags=doc.get("tags", []),
            outgoing_links=doc.get("outgoing_links", []),
            backlinks=backlinks,
            roadmap_node_id=doc.get("roadmap_node_id"),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at")
        )

    async def list_notes(
        self,
        user_id: str,
        search: Optional[str] = None,
        tag: Optional[str] = None
    ) -> NoteListResponse:
        col = get_progress_notes_collection()
        if col is None:
            return NoteListResponse(notes=[], total=0)

        query: Dict[str, Any] = {"user_id": user_id}
        if tag and tag.strip():
            query["tags"] = tag.strip().lower()
        if search and search.strip():
            s = search.strip()
            query["$or"] = [
                {"title": {"$regex": s, "$options": "i"}},
                {"content_md": {"$regex": s, "$options": "i"}}
            ]

        cursor = col.find(query).sort([("updated_at", -1)])
        notes = []
        async for doc in cursor:
            notes.append(await self._doc_to_note(doc))

        return NoteListResponse(notes=notes, total=len(notes))

    async def get_note(self, user_id: str, note_id_or_title: str) -> Optional[NoteResponse]:
        col = get_progress_notes_collection()
        if col is None:
            return None

        doc = None
        if ObjectId.is_valid(note_id_or_title):
            doc = await col.find_one({"_id": ObjectId(note_id_or_title), "user_id": user_id})

        if not doc:
            # Buscar por título exacto (case-insensitive) o slug
            doc = await col.find_one({
                "user_id": user_id,
                "$or": [
                    {"title": {"$regex": f"^{re.escape(note_id_or_title.strip())}$", "$options": "i"}},
                    {"slug": slugify(note_id_or_title)}
                ]
            })

        if not doc:
            return None
        return await self._doc_to_note(doc)

    async def create_note(self, user_id: str, req: NoteCreateRequest) -> NoteResponse:
        col = get_progress_notes_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        now = datetime.utcnow()
        title = req.title.strip()
        outgoing = extract_wikilinks(req.content_md)
        body_tags = extract_tags(req.content_md)
        manual_tags = [t.strip().lower() for t in (req.tags or []) if t.strip()]
        all_tags = list(set(body_tags + manual_tags))

        doc = {
            "user_id": user_id,
            "title": title,
            "slug": slugify(title),
            "content_md": req.content_md,
            "tags": all_tags,
            "outgoing_links": outgoing,
            "roadmap_node_id": req.roadmap_node_id,
            "created_at": now,
            "updated_at": now
        }
        res = await col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return await self._doc_to_note(doc)

    async def update_note(
        self,
        user_id: str,
        note_id: str,
        req: NoteUpdateRequest
    ) -> Optional[NoteResponse]:
        col = get_progress_notes_collection()
        if col is None or not ObjectId.is_valid(note_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}

        if req.title is not None:
            update_data["title"] = req.title.strip()
            update_data["slug"] = slugify(req.title.strip())

        if req.content_md is not None:
            update_data["content_md"] = req.content_md
            outgoing = extract_wikilinks(req.content_md)
            body_tags = extract_tags(req.content_md)
            manual_tags = [t.strip().lower() for t in (req.tags or []) if t.strip()]
            update_data["outgoing_links"] = outgoing
            update_data["tags"] = list(set(body_tags + manual_tags))
        elif req.tags is not None:
            manual_tags = [t.strip().lower() for t in req.tags if t.strip()]
            update_data["tags"] = manual_tags

        res = await col.find_one_and_update(
            {"_id": ObjectId(note_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None
        return await self._doc_to_note(res)

    async def delete_note(self, user_id: str, note_id: str) -> bool:
        col = get_progress_notes_collection()
        if col is None or not ObjectId.is_valid(note_id):
            return False
        res = await col.delete_one({"_id": ObjectId(note_id), "user_id": user_id})
        return res.deleted_count > 0

    async def get_knowledge_graph(self, user_id: str) -> KnowledgeGraphResponse:
        """Genera la estructura de nodos y aristas de la red Zettelkasten para el usuario."""
        col = get_progress_notes_collection()
        if col is None:
            return KnowledgeGraphResponse(nodes=[], edges=[], all_tags=[], total_notes=0, total_connections=0)

        cursor = col.find({"user_id": user_id})
        raw_notes = []
        title_to_id: Dict[str, str] = {}
        all_tags_set: Set[str] = set()

        async for doc in cursor:
            n_id = str(doc["_id"])
            n_title = doc["title"]
            n_tags = doc.get("tags", [])
            outgoing = doc.get("outgoing_links", [])

            title_to_id[n_title.lower().strip()] = n_id
            for t in n_tags:
                all_tags_set.add(t)

            raw_notes.append({
                "id": n_id,
                "title": n_title,
                "tags": n_tags,
                "outgoing": outgoing
            })

        edges: List[GraphEdgeResponse] = []
        connections_counter: Dict[str, int] = {n["id"]: 0 for n in raw_notes}
        edges_set: Set[str] = set()

        for n in raw_notes:
            src_id = n["id"]
            for target_title in n["outgoing"]:
                tgt_id = title_to_id.get(target_title.lower().strip())
                if tgt_id and tgt_id != src_id:
                    edge_key = f"{min(src_id, tgt_id)}--{max(src_id, tgt_id)}"
                    if edge_key not in edges_set:
                        edges_set.add(edge_key)
                        edges.append(GraphEdgeResponse(source=src_id, target=tgt_id))
                        connections_counter[src_id] = connections_counter.get(src_id, 0) + 1
                        connections_counter[tgt_id] = connections_counter.get(tgt_id, 0) + 1

        nodes: List[GraphNodeResponse] = []
        for n in raw_notes:
            nodes.append(GraphNodeResponse(
                id=n["id"],
                title=n["title"],
                tags=n["tags"],
                connections_count=connections_counter.get(n["id"], 0),
                group="Nota"
            ))

        return KnowledgeGraphResponse(
            nodes=nodes,
            edges=edges,
            all_tags=sorted(list(all_tags_set)),
            total_notes=len(nodes),
            total_connections=len(edges)
        )


progress_service = ProgressService()
