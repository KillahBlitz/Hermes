import calendar
import logging
from datetime import datetime, time
from typing import Any, Dict, List, Optional
from bson import ObjectId
from src.database.mongo import (
    get_finance_categories_collection,
    get_finance_transactions_collection,
)
from src.models.request.finance import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
    TransactionCreateRequest,
    TransactionUpdateRequest,
)
from src.models.response.finance import (
    CategoryBreakdownItem,
    CategoryBreakdownResponse,
    CategoryResponse,
    FinanceSummaryResponse,
    HighestCategoryInsight,
    HighestExpenseInsight,
    MomComparison,
    MonthlyTrendsResponse,
    MonthTrendItem,
    PeriodInfo,
    TopInsights,
    TotalsInfo,
    TransactionResponse,
)

logger = logging.getLogger("hermes-api.finance")

MONTH_NAMES_ES = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

DEFAULT_CATEGORIES = [
    # Gastos (EXPENSE)
    {"name": "Vivienda & Servicios", "type": "EXPENSE", "icon": "🏠", "color": "#00E5FF", "is_default": True},
    {"name": "Supermercado & Alimentación", "type": "EXPENSE", "icon": "🛒", "color": "#00FFC6", "is_default": True},
    {"name": "Transporte & Combustible", "type": "EXPENSE", "icon": "🚗", "color": "#FFD166", "is_default": True},
    {"name": "Entretenimiento & Ocio", "type": "EXPENSE", "icon": "🍿", "color": "#FF007F", "is_default": True},
    {"name": "Salud & Bienestar", "type": "EXPENSE", "icon": "💊", "color": "#06D6A0", "is_default": True},
    {"name": "Educación & Cursos", "type": "EXPENSE", "icon": "📚", "color": "#118AB2", "is_default": True},
    {"name": "Compras Personales", "type": "EXPENSE", "icon": "🛍️", "color": "#B5179E", "is_default": True},
    {"name": "Otros Gastos", "type": "EXPENSE", "icon": "⚙️", "color": "#94949E", "is_default": True},
    # Ingresos (INCOME)
    {"name": "Salario & Sueldo Principal", "type": "INCOME", "icon": "💼", "color": "#00FFC6", "is_default": True},
    {"name": "Freelance & Proyectos", "type": "INCOME", "icon": "💻", "color": "#00E5FF", "is_default": True},
    {"name": "Inversiones & Rendimientos", "type": "INCOME", "icon": "📈", "color": "#7209B7", "is_default": True},
    {"name": "Regalos & Bonos", "type": "INCOME", "icon": "🎁", "color": "#FF007F", "is_default": True},
    {"name": "Otros Ingresos", "type": "INCOME", "icon": "💰", "color": "#94949E", "is_default": True},
]


class FinanceService:

    async def ensure_default_categories(self, user_id: str) -> None:
        """Asegura que el usuario tenga sembradas las categorías predeterminadas sin duplicados."""
        col = get_finance_categories_collection()
        if col is None:
            return

        now = datetime.utcnow()

        # 1. Upsert atómico para cada categoría por defecto (inmune a concurrencia)
        for cat in DEFAULT_CATEGORIES:
            await col.update_one(
                {
                    "user_id": user_id,
                    "name": cat["name"],
                    "type": cat["type"]
                },
                {
                    "$setOnInsert": {
                        "user_id": user_id,
                        "name": cat["name"],
                        "type": cat["type"],
                        "icon": cat["icon"],
                        "color": cat["color"],
                        "is_default": True,
                        "created_at": now,
                        "updated_at": now,
                    }
                },
                upsert=True
            )

        # 2. Limpieza de duplicados residuales si existieran previamente en la base de datos
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": {"name": "$name", "type": "$type"}, "ids": {"$push": "$_id"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}
        ]
        async for dup in col.aggregate(pipeline):
            ids_to_remove = dup["ids"][1:]
            if ids_to_remove:
                await col.delete_many({"_id": {"$in": ids_to_remove}})

    # ─────────────────────────────────────────────────────────────
    # CATEGORÍAS
    # ─────────────────────────────────────────────────────────────

    async def list_categories(self, user_id: str, type_filter: Optional[str] = None) -> List[CategoryResponse]:
        await self.ensure_default_categories(user_id)
        col = get_finance_categories_collection()
        if col is None:
            return []

        query: Dict[str, Any] = {"user_id": user_id}
        if type_filter and type_filter in ("INCOME", "EXPENSE"):
            query["type"] = type_filter

        cursor = col.find(query).sort([("is_default", -1), ("name", 1)])
        results = []
        seen = set()
        async for doc in cursor:
            key = (doc["name"], doc["type"])
            if key in seen:
                continue
            seen.add(key)
            results.append(CategoryResponse(
                id=str(doc["_id"]),
                user_id=doc.get("user_id"),
                name=doc["name"],
                type=doc["type"],
                icon=doc.get("icon", "🏷️"),
                color=doc.get("color", "#00FFC6"),
                is_default=doc.get("is_default", False),
                created_at=doc.get("created_at")
            ))
        return results

    async def create_category(self, user_id: str, req: CategoryCreateRequest) -> CategoryResponse:
        col = get_finance_categories_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        # Evitar crear duplicados si ya existe una con el mismo nombre y tipo para este usuario
        existing = await col.find_one({
            "user_id": user_id,
            "name": {"$regex": f"^{req.name.strip()}$", "$options": "i"},
            "type": req.type
        })
        if existing:
            return CategoryResponse(
                id=str(existing["_id"]),
                user_id=existing.get("user_id"),
                name=existing["name"],
                type=existing["type"],
                icon=existing.get("icon", req.icon),
                color=existing.get("color", req.color),
                is_default=existing.get("is_default", False),
                created_at=existing.get("created_at")
            )

        now = datetime.utcnow()
        doc = {
            "user_id": user_id,
            "name": req.name.strip(),
            "type": req.type,
            "icon": req.icon,
            "color": req.color,
            "is_default": False,
            "created_at": now,
            "updated_at": now,
        }
        res = await col.insert_one(doc)
        return CategoryResponse(
            id=str(res.inserted_id),
            user_id=user_id,
            name=doc["name"],
            type=doc["type"],
            icon=doc["icon"],
            color=doc["color"],
            is_default=False,
            created_at=now
        )

    async def update_category(self, user_id: str, category_id: str, req: CategoryUpdateRequest) -> Optional[CategoryResponse]:
        col = get_finance_categories_collection()
        if col is None:
            return None

        if not ObjectId.is_valid(category_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}
        if req.name is not None:
            update_data["name"] = req.name.strip()
        if req.type is not None:
            update_data["type"] = req.type
        if req.icon is not None:
            update_data["icon"] = req.icon
        if req.color is not None:
            update_data["color"] = req.color

        res = await col.find_one_and_update(
            {"_id": ObjectId(category_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        return CategoryResponse(
            id=str(res["_id"]),
            user_id=res.get("user_id"),
            name=res["name"],
            type=res["type"],
            icon=res.get("icon", "🏷️"),
            color=res.get("color", "#00FFC6"),
            is_default=res.get("is_default", False),
            created_at=res.get("created_at")
        )

    async def delete_category(self, user_id: str, category_id: str) -> bool:
        col_cat = get_finance_categories_collection()
        col_tx = get_finance_transactions_collection()
        if col_cat is None or col_tx is None:
            return False

        if not ObjectId.is_valid(category_id):
            return False

        cat = await col_cat.find_one({"_id": ObjectId(category_id), "user_id": user_id})
        if not cat:
            return False

        # Reasignar transacciones asociadas a la categoría default "Otros"
        fallback_name = "Otros Gastos" if cat["type"] == "EXPENSE" else "Otros Ingresos"
        fallback_cat = await col_cat.find_one({
            "user_id": user_id,
            "type": cat["type"],
            "is_default": True,
            "name": fallback_name
        })

        fallback_id = str(fallback_cat["_id"]) if fallback_cat else None
        if fallback_id:
            await col_tx.update_many(
                {"user_id": user_id, "category_id": category_id},
                {"$set": {"category_id": fallback_id, "updated_at": datetime.utcnow()}}
            )

        await col_cat.delete_one({"_id": ObjectId(category_id), "user_id": user_id})
        return True

    # ─────────────────────────────────────────────────────────────
    # TRANSACCIONES
    # ─────────────────────────────────────────────────────────────

    async def _get_category_map(self, user_id: str) -> Dict[str, CategoryResponse]:
        categories = await self.list_categories(user_id)
        return {cat.id: cat for cat in categories}

    async def create_transaction(self, user_id: str, req: TransactionCreateRequest) -> TransactionResponse:
        col = get_finance_transactions_collection()
        if col is None:
            raise RuntimeError("Base de datos no disponible")

        now = datetime.utcnow()
        doc = {
            "user_id": user_id,
            "title": req.title.strip(),
            "amount": float(req.amount),
            "type": req.type,
            "category_id": req.category_id,
            "date": req.date,
            "notes": req.notes,
            "payment_method": req.payment_method,
            "tags": req.tags or [],
            "created_at": now,
            "updated_at": now,
        }
        res = await col.insert_one(doc)

        cat_map = await self._get_category_map(user_id)
        cat = cat_map.get(req.category_id)

        return TransactionResponse(
            id=str(res.inserted_id),
            user_id=user_id,
            title=doc["title"],
            amount=doc["amount"],
            type=doc["type"],
            category_id=doc["category_id"],
            category=cat,
            date=doc["date"],
            notes=doc["notes"],
            payment_method=doc["payment_method"],
            tags=doc["tags"],
            created_at=now,
            updated_at=now
        )

    async def get_transaction(self, user_id: str, transaction_id: str) -> Optional[TransactionResponse]:
        col = get_finance_transactions_collection()
        if col is None or not ObjectId.is_valid(transaction_id):
            return None

        doc = await col.find_one({"_id": ObjectId(transaction_id), "user_id": user_id})
        if not doc:
            return None

        cat_map = await self._get_category_map(user_id)
        return TransactionResponse(
            id=str(doc["_id"]),
            user_id=user_id,
            title=doc["title"],
            amount=doc["amount"],
            type=doc["type"],
            category_id=doc["category_id"],
            category=cat_map.get(doc["category_id"]),
            date=doc["date"],
            notes=doc.get("notes"),
            payment_method=doc.get("payment_method"),
            tags=doc.get("tags", []),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"]
        )

    async def update_transaction(self, user_id: str, transaction_id: str, req: TransactionUpdateRequest) -> Optional[TransactionResponse]:
        col = get_finance_transactions_collection()
        if col is None or not ObjectId.is_valid(transaction_id):
            return None

        update_data: Dict[str, Any] = {"updated_at": datetime.utcnow()}
        if req.title is not None:
            update_data["title"] = req.title.strip()
        if req.amount is not None:
            update_data["amount"] = float(req.amount)
        if req.type is not None:
            update_data["type"] = req.type
        if req.category_id is not None:
            update_data["category_id"] = req.category_id
        if req.date is not None:
            update_data["date"] = req.date
        if req.notes is not None:
            update_data["notes"] = req.notes
        if req.payment_method is not None:
            update_data["payment_method"] = req.payment_method
        if req.tags is not None:
            update_data["tags"] = req.tags

        res = await col.find_one_and_update(
            {"_id": ObjectId(transaction_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not res:
            return None

        cat_map = await self._get_category_map(user_id)
        return TransactionResponse(
            id=str(res["_id"]),
            user_id=user_id,
            title=res["title"],
            amount=res["amount"],
            type=res["type"],
            category_id=res["category_id"],
            category=cat_map.get(res["category_id"]),
            date=res["date"],
            notes=res.get("notes"),
            payment_method=res.get("payment_method"),
            tags=res.get("tags", []),
            created_at=res["created_at"],
            updated_at=res["updated_at"]
        )

    async def delete_transaction(self, user_id: str, transaction_id: str) -> bool:
        col = get_finance_transactions_collection()
        if col is None or not ObjectId.is_valid(transaction_id):
            return False

        res = await col.delete_one({"_id": ObjectId(transaction_id), "user_id": user_id})
        return res.deleted_count > 0

    async def list_transactions(
        self,
        user_id: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        type_filter: Optional[str] = None,
        category_id: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
    ) -> Dict[str, Any]:
        col = get_finance_transactions_collection()
        if col is None:
            return {"transactions": [], "total": 0, "page": page, "limit": limit, "total_pages": 0}

        query: Dict[str, Any] = {"user_id": user_id}

        # Filtro de fecha
        if year and month:
            last_day = calendar.monthrange(year, month)[1]
            start_date = datetime(year, month, 1, 0, 0, 0)
            end_date = datetime(year, month, last_day, 23, 59, 59, 999999)
            query["date"] = {"$gte": start_date, "$lte": end_date}
        elif year:
            start_date = datetime(year, 1, 1, 0, 0, 0)
            end_date = datetime(year, 12, 31, 23, 59, 59, 999999)
            query["date"] = {"$gte": start_date, "$lte": end_date}

        # Filtro por tipo
        if type_filter and type_filter in ("INCOME", "EXPENSE"):
            query["type"] = type_filter

        # Filtro por categoría
        if category_id:
            query["category_id"] = category_id

        # Filtro de búsqueda por texto en título o notas
        if search and search.strip():
            query["$or"] = [
                {"title": {"$regex": search.strip(), "$options": "i"}},
                {"notes": {"$regex": search.strip(), "$options": "i"}},
                {"tags": {"$in": [search.strip().lower()]}}
            ]

        total = await col.count_documents(query)
        total_pages = max(1, (total + limit - 1) // limit) if total > 0 else 0
        skip = (page - 1) * limit

        cursor = col.find(query).sort("date", -1).skip(skip).limit(limit)
        cat_map = await self._get_category_map(user_id)

        transactions = []
        async for doc in cursor:
            transactions.append(TransactionResponse(
                id=str(doc["_id"]),
                user_id=user_id,
                title=doc["title"],
                amount=doc["amount"],
                type=doc["type"],
                category_id=doc["category_id"],
                category=cat_map.get(doc["category_id"]),
                date=doc["date"],
                notes=doc.get("notes"),
                payment_method=doc.get("payment_method"),
                tags=doc.get("tags", []),
                created_at=doc["created_at"],
                updated_at=doc["updated_at"]
            ))

        return {
            "transactions": transactions,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }

    # ─────────────────────────────────────────────────────────────
    # ANALÍTICA Y REPORTES
    # ─────────────────────────────────────────────────────────────

    async def _calculate_month_totals(self, user_id: str, year: int, month: int) -> Dict[str, float]:
        col = get_finance_transactions_collection()
        if col is None:
            return {"income": 0.0, "expenses": 0.0}

        last_day = calendar.monthrange(year, month)[1]
        start_date = datetime(year, month, 1, 0, 0, 0)
        end_date = datetime(year, month, last_day, 23, 59, 59, 999999)

        pipeline = [
            {"$match": {"user_id": user_id, "date": {"$gte": start_date, "$lte": end_date}}},
            {"$group": {"_id": "$type", "total": {"$sum": "$amount"}}}
        ]
        results = await col.aggregate(pipeline).to_list(length=10)
        totals = {"INCOME": 0.0, "EXPENSE": 0.0}
        for item in results:
            totals[item["_id"]] = float(item["total"])

        return {"income": totals["INCOME"], "expenses": totals["EXPENSE"]}

    async def get_summary(self, user_id: str, year: int, month: int) -> FinanceSummaryResponse:
        await self.ensure_default_categories(user_id)
        current = await self._calculate_month_totals(user_id, year, month)
        total_income = current["income"]
        total_expenses = current["expenses"]
        net_savings = total_income - total_expenses
        savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0.0

        # Mes anterior
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        previous = await self._calculate_month_totals(user_id, prev_year, prev_month)
        prev_income = previous["income"]
        prev_expenses = previous["expenses"]
        prev_savings = prev_income - prev_expenses

        # Cálculo MoM
        inc_diff = total_income - prev_income
        inc_pct = ((total_income - prev_income) / prev_income * 100) if prev_income > 0 else (100.0 if total_income > 0 else None)

        exp_diff = total_expenses - prev_expenses
        exp_pct = ((total_expenses - prev_expenses) / prev_expenses * 100) if prev_expenses > 0 else (100.0 if total_expenses > 0 else None)

        sav_diff = net_savings - prev_savings
        sav_pct = ((net_savings - prev_savings) / abs(prev_savings) * 100) if prev_savings != 0 else (100.0 if net_savings > 0 else None)

        # Insights: Mayor gasto individual
        col = get_finance_transactions_collection()
        last_day = calendar.monthrange(year, month)[1]
        start_date = datetime(year, month, 1, 0, 0, 0)
        end_date = datetime(year, month, last_day, 23, 59, 59, 999999)

        cat_map = await self._get_category_map(user_id)

        highest_single_expense: Optional[HighestExpenseInsight] = None
        if col is not None:
            max_doc = await col.find(
                {"user_id": user_id, "type": "EXPENSE", "date": {"$gte": start_date, "$lte": end_date}}
            ).sort("amount", -1).limit(1).to_list(length=1)

            if max_doc:
                d = max_doc[0]
                cat = cat_map.get(d["category_id"])
                highest_single_expense = HighestExpenseInsight(
                    id=str(d["_id"]),
                    title=d["title"],
                    amount=d["amount"],
                    category_name=cat.name if cat else "Sin categoría",
                    date=d["date"]
                )

        # Insights: Categoría con mayor gasto
        highest_category: Optional[HighestCategoryInsight] = None
        if col is not None and total_expenses > 0:
            cat_pipeline = [
                {"$match": {"user_id": user_id, "type": "EXPENSE", "date": {"$gte": start_date, "$lte": end_date}}},
                {"$group": {"_id": "$category_id", "total": {"$sum": "$amount"}}},
                {"$sort": {"total": -1}},
                {"$limit": 1}
            ]
            cat_res = await col.aggregate(cat_pipeline).to_list(length=1)
            if cat_res:
                top_cat_id = cat_res[0]["_id"]
                top_cat_total = float(cat_res[0]["total"])
                cat = cat_map.get(top_cat_id)
                highest_category = HighestCategoryInsight(
                    category_id=top_cat_id,
                    category_name=cat.name if cat else "Otros Gastos",
                    icon=cat.icon if cat else "⚙️",
                    color=cat.color if cat else "#94949E",
                    total_amount=top_cat_total,
                    percentage_of_total_expenses=round((top_cat_total / total_expenses * 100), 2)
                )

        month_name = MONTH_NAMES_ES[month] if 1 <= month <= 12 else str(month)

        return FinanceSummaryResponse(
            period=PeriodInfo(year=year, month=month, month_name=month_name),
            totals=TotalsInfo(
                total_income=round(total_income, 2),
                total_expenses=round(total_expenses, 2),
                net_savings=round(net_savings, 2),
                savings_rate_percent=round(savings_rate, 2)
            ),
            comparison_previous_month=MomComparison(
                income_difference=round(inc_diff, 2),
                income_percentage_change=round(inc_pct, 2) if inc_pct is not None else None,
                expense_difference=round(exp_diff, 2),
                expense_percentage_change=round(exp_pct, 2) if exp_pct is not None else None,
                savings_difference=round(sav_diff, 2),
                savings_percentage_change=round(sav_pct, 2) if sav_pct is not None else None
            ),
            top_insights=TopInsights(
                highest_single_expense=highest_single_expense,
                highest_expense_category=highest_category
            )
        )

    async def get_category_breakdown(self, user_id: str, year: int, month: int, type_filter: str = "EXPENSE") -> CategoryBreakdownResponse:
        await self.ensure_default_categories(user_id)
        col = get_finance_transactions_collection()
        if col is None:
            return CategoryBreakdownResponse(year=year, month=month, type=type_filter, total=0.0, breakdown=[])

        last_day = calendar.monthrange(year, month)[1]
        start_date = datetime(year, month, 1, 0, 0, 0)
        end_date = datetime(year, month, last_day, 23, 59, 59, 999999)

        pipeline = [
            {"$match": {"user_id": user_id, "type": type_filter, "date": {"$gte": start_date, "$lte": end_date}}},
            {"$group": {"_id": "$category_id", "total": {"$sum": "$amount"}, "count": {"$sum": 1}}},
            {"$sort": {"total": -1}}
        ]
        results = await col.aggregate(pipeline).to_list(length=100)
        grand_total = sum(float(item["total"]) for item in results)

        cat_map = await self._get_category_map(user_id)
        breakdown_items = []
        for item in results:
            cat_id = item["_id"]
            cat_total = float(item["total"])
            cat = cat_map.get(cat_id)
            pct = round((cat_total / grand_total * 100), 2) if grand_total > 0 else 0.0
            breakdown_items.append(CategoryBreakdownItem(
                category_id=cat_id,
                name=cat.name if cat else "Sin categoría",
                icon=cat.icon if cat else "🏷️",
                color=cat.color if cat else "#94949E",
                total=round(cat_total, 2),
                percentage=pct,
                transaction_count=item["count"]
            ))

        return CategoryBreakdownResponse(
            year=year,
            month=month,
            type=type_filter,
            total=round(grand_total, 2),
            breakdown=breakdown_items
        )

    async def get_monthly_trends(self, user_id: str, end_year: int, end_month: int, months_count: int = 6) -> MonthlyTrendsResponse:
        await self.ensure_default_categories(user_id)
        # Construir lista de (año, mes) hacia atrás
        target_months = []
        curr_y = end_year
        curr_m = end_month
        for _ in range(months_count):
            target_months.append((curr_y, curr_m))
            curr_m -= 1
            if curr_m < 1:
                curr_m = 12
                curr_y -= 1

        target_months.reverse() # De más antiguo a más reciente

        items = []
        for y, m in target_months:
            totals = await self._calculate_month_totals(user_id, y, m)
            inc = totals["income"]
            exp = totals["expenses"]
            m_short = MONTH_NAMES_ES[m][:3] if 1 <= m <= 12 else str(m)
            label = f"{m_short} {str(y)[2:]}"
            items.append(MonthTrendItem(
                year=y,
                month=m,
                label=label,
                income=round(inc, 2),
                expenses=round(exp, 2),
                savings=round(inc - exp, 2)
            ))

        return MonthlyTrendsResponse(months=items)


finance_service = FinanceService()
