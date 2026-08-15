from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class TransactionCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=120, description="Concepto del movimiento")
    amount: float = Field(..., gt=0, description="Monto monetario (siempre positivo)")
    type: Literal["INCOME", "EXPENSE"] = Field(..., description="Tipo de movimiento: INCOME o EXPENSE")
    category_id: str = Field(..., description="ID de la categoría asignada")
    date: datetime = Field(default_factory=datetime.utcnow, description="Fecha de la transacción")
    notes: Optional[str] = Field(None, max_length=500, description="Notas o descripción adicional")
    payment_method: Optional[str] = Field(None, description="Método de pago (CASH, DEBIT_CARD, CREDIT_CARD, TRANSFER, OTHER)")
    tags: Optional[List[str]] = Field(default_factory=list, description="Etiquetas de búsqueda")


class TransactionUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[Literal["INCOME", "EXPENSE"]] = None
    category_id: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)
    payment_method: Optional[str] = None
    tags: Optional[List[str]] = None


class CategoryCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Nombre de la categoría")
    type: Literal["INCOME", "EXPENSE"] = Field(..., description="Tipo de categoría: INCOME o EXPENSE")
    icon: str = Field("🏷️", description="Icono o emoji")
    color: str = Field("#00FFC6", description="Color hexadecimal para gráficas y badges")


class CategoryUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    type: Optional[Literal["INCOME", "EXPENSE"]] = None
    icon: Optional[str] = None
    color: Optional[str] = None
