from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    name: str
    type: str
    icon: str
    color: str
    is_default: bool = False
    created_at: Optional[datetime] = None


class CategoryListResponse(BaseModel):
    categories: List[CategoryResponse]
    total: int


class TransactionResponse(BaseModel):
    id: str
    user_id: str
    title: str
    amount: float
    type: str
    category_id: str
    category: Optional[CategoryResponse] = None
    date: datetime
    notes: Optional[str] = None
    payment_method: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    page: int
    limit: int
    total_pages: int


# --- Modelos para Analítica y Reportes ---

class PeriodInfo(BaseModel):
    year: int
    month: int
    month_name: str


class TotalsInfo(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate_percent: float


class MomComparison(BaseModel):
    income_difference: float
    income_percentage_change: Optional[float] = None
    expense_difference: float
    expense_percentage_change: Optional[float] = None
    savings_difference: float
    savings_percentage_change: Optional[float] = None


class HighestExpenseInsight(BaseModel):
    id: str
    title: str
    amount: float
    category_name: str
    date: datetime


class HighestCategoryInsight(BaseModel):
    category_id: str
    category_name: str
    icon: str
    color: str
    total_amount: float
    percentage_of_total_expenses: float


class TopInsights(BaseModel):
    highest_single_expense: Optional[HighestExpenseInsight] = None
    highest_expense_category: Optional[HighestCategoryInsight] = None


class FinanceSummaryResponse(BaseModel):
    period: PeriodInfo
    totals: TotalsInfo
    comparison_previous_month: MomComparison
    top_insights: TopInsights


class CategoryBreakdownItem(BaseModel):
    category_id: str
    name: str
    icon: str
    color: str
    total: float
    percentage: float
    transaction_count: int


class CategoryBreakdownResponse(BaseModel):
    year: int
    month: int
    type: str
    total: float
    breakdown: List[CategoryBreakdownItem]


class MonthTrendItem(BaseModel):
    year: int
    month: int
    label: str
    income: float
    expenses: float
    savings: float


class MonthlyTrendsResponse(BaseModel):
    months: List[MonthTrendItem]
