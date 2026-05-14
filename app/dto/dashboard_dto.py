from decimal import Decimal
from typing import Literal

from app.dto.base_dto import DTO


class BudgetProgressOut(DTO):
    amount: Decimal
    spent: Decimal
    percentage: Decimal
    remaining: Decimal
    source: Literal["FIXED", "DYNAMIC_INCOME"]
    is_dynamic: bool


class DashboardSummaryOut(DTO):
    month: str
    total_income: Decimal
    total_expenses: Decimal
    balance: Decimal
    budget_info: BudgetProgressOut | None = None


class ExpensesByCategoryOut(DTO):
    category_id: int
    category_name: str
    total: Decimal
    percentage: Decimal


class MonthlyTrendOut(DTO):
    month: str
    income: Decimal
    expenses: Decimal
    balance: Decimal
