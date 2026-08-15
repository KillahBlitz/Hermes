import logging
from datetime import datetime
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from src.models.request.finance import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
    TransactionCreateRequest,
    TransactionUpdateRequest,
)
from src.models.response.finance import (
    CategoryBreakdownResponse,
    CategoryListResponse,
    CategoryResponse,
    FinanceSummaryResponse,
    MonthlyTrendsResponse,
    TransactionListResponse,
    TransactionResponse,
)
from src.services.finance_service import finance_service
from src.utils.jwt import get_current_user_payload

logger = logging.getLogger("hermes-api.finance")
router = APIRouter(prefix="/finance", tags=["Finance & Economy"])


# ═══════════════════════════════════════════════════════════════
#  CATEGORÍAS ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/categories", response_model=CategoryListResponse)
async def get_categories(
    type: Optional[str] = Query(None, pattern="^(INCOME|EXPENSE)$", description="Filtrar por tipo"),
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Obtiene las categorías disponibles para el usuario."""
    user_id = payload.get("sub")
    categories = await finance_service.list_categories(user_id=user_id, type_filter=type)
    return CategoryListResponse(categories=categories, total=len(categories))


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    req: CategoryCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Crea una nueva categoría personalizada para el usuario."""
    user_id = payload.get("sub")
    return await finance_service.create_category(user_id=user_id, req=req)


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    req: CategoryUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Actualiza una categoría de usuario existente."""
    user_id = payload.get("sub")
    updated = await finance_service.update_category(user_id=user_id, category_id=category_id, req=req)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada o no pertenece al usuario"
        )
    return updated


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Elimina una categoría personalizada del usuario."""
    user_id = payload.get("sub")
    success = await finance_service.delete_category(user_id=user_id, category_id=category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo eliminar la categoría (solo puedes eliminar categorías personalizadas propias)"
        )
    return {"message": "Categoría eliminada exitosamente", "category_id": category_id}


# ═══════════════════════════════════════════════════════════════
#  TRANSACCIONES ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/transactions", response_model=TransactionListResponse)
async def list_transactions(
    year: Optional[int] = Query(None, ge=2000, le=2100),
    month: Optional[int] = Query(None, ge=1, le=12),
    type: Optional[str] = Query(None, pattern="^(INCOME|EXPENSE)$"),
    category_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None, max_length=100),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Lista transacciones paginadas con filtros de fecha, tipo y categoría."""
    user_id = payload.get("sub")
    res = await finance_service.list_transactions(
        user_id=user_id,
        year=year,
        month=month,
        type_filter=type,
        category_id=category_id,
        search=search,
        page=page,
        limit=limit,
    )
    return TransactionListResponse(
        transactions=res["transactions"],
        total=res["total"],
        page=res["page"],
        limit=res["limit"],
        total_pages=res["total_pages"],
    )


@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    req: TransactionCreateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Registra una nueva transacción monetaria (Ingreso o Gasto)."""
    user_id = payload.get("sub")
    return await finance_service.create_transaction(user_id=user_id, req=req)


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Obtiene el detalle de una transacción."""
    user_id = payload.get("sub")
    tx = await finance_service.get_transaction(user_id=user_id, transaction_id=transaction_id)
    if not tx:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    return tx


@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    req: TransactionUpdateRequest,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Actualiza una transacción existente."""
    user_id = payload.get("sub")
    tx = await finance_service.update_transaction(user_id=user_id, transaction_id=transaction_id, req=req)
    if not tx:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada o no pertenece al usuario"
        )
    return tx


@router.delete("/transactions/{transaction_id}")
async def delete_transaction(
    transaction_id: str,
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Elimina una transacción del usuario."""
    user_id = payload.get("sub")
    success = await finance_service.delete_transaction(user_id=user_id, transaction_id=transaction_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    return {"message": "Transacción eliminada exitosamente", "transaction_id": transaction_id}


# ═══════════════════════════════════════════════════════════════
#  ANALÍTICA Y REPORTES ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/analytics/summary", response_model=FinanceSummaryResponse)
async def get_monthly_summary(
    year: int = Query(default_factory=lambda: datetime.utcnow().year, ge=2000, le=2100),
    month: int = Query(default_factory=lambda: datetime.utcnow().month, ge=1, le=12),
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Calcula el resumen financiero del mes y comparativa con el mes anterior (MoM)."""
    user_id = payload.get("sub")
    return await finance_service.get_summary(user_id=user_id, year=year, month=month)


@router.get("/analytics/category-breakdown", response_model=CategoryBreakdownResponse)
async def get_category_breakdown(
    year: int = Query(default_factory=lambda: datetime.utcnow().year, ge=2000, le=2100),
    month: int = Query(default_factory=lambda: datetime.utcnow().month, ge=1, le=12),
    type: str = Query("EXPENSE", pattern="^(INCOME|EXPENSE)$"),
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Calcula el desglose porcentual y montos por categoría para gráficas circulares."""
    user_id = payload.get("sub")
    return await finance_service.get_category_breakdown(user_id=user_id, year=year, month=month, type_filter=type)


@router.get("/analytics/monthly-trends", response_model=MonthlyTrendsResponse)
async def get_monthly_trends(
    year: int = Query(default_factory=lambda: datetime.utcnow().year, ge=2000, le=2100),
    month: int = Query(default_factory=lambda: datetime.utcnow().month, ge=1, le=12),
    count: int = Query(6, ge=1, le=24, description="Número de meses históricos a incluir"),
    payload: Dict[str, Any] = Depends(get_current_user_payload),
):
    """Calcula las tendencias de ingresos vs gastos en los últimos N meses para la gráfica de barras."""
    user_id = payload.get("sub")
    return await finance_service.get_monthly_trends(user_id=user_id, end_year=year, end_month=month, months_count=count)
