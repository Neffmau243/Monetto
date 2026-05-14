from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.dashboard_dto import (
    BudgetProgressOut,
    DashboardSummaryOut,
    ExpensesByCategoryOut,
    MonthlyTrendOut,
)
from app.repositories.budget_repository import BudgetRepository, budget_repository
from app.repositories.dashboard_repository import DashboardRepository, dashboard_repository
from app.utils.dates import iter_months, month_bounds, parse_month, subtract_months
from app.utils.money import money, percentage


class DashboardService:
    def __init__(
        self,
        repository: DashboardRepository,
        budget_repo: BudgetRepository,
    ) -> None:
        self.repository = repository
        self.budget_repo = budget_repo

    async def summary(
        self, db: AsyncSession, *, user_id: int, month: str | None = None
    ) -> DashboardSummaryOut:
        parsed_month = parse_month(month)
        start_date, end_date = month_bounds(parsed_month)
        total_income, total_expenses = await self.repository.summary_totals(
            db, user_id=user_id, start_date=start_date, end_date=end_date
        )
        budget_info = await self._budget_progress(
            db,
            user_id=user_id,
            month_value=parsed_month,
            income=total_income,
            spent=total_expenses,
        )
        return DashboardSummaryOut(
            month=parsed_month.strftime("%Y-%m"),
            total_income=money(total_income),
            total_expenses=money(total_expenses),
            balance=money(total_income - total_expenses),
            budget_info=budget_info,
        )

    async def expenses_by_category(
        self, db: AsyncSession, *, user_id: int, month: str | None = None
    ) -> list[ExpensesByCategoryOut]:
        parsed_month = parse_month(month)
        start_date, end_date = month_bounds(parsed_month)
        rows = await self.repository.expenses_by_category(
            db, user_id=user_id, start_date=start_date, end_date=end_date
        )
        return [
            ExpensesByCategoryOut(
                category_id=row["category_id"],
                category_name=row["category_name"],
                total=money(row["total"]),
                percentage=money(row["percentage"]),
            )
            for row in rows
        ]

    async def monthly_trend(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        months: int = 6,
    ) -> list[MonthlyTrendOut]:
        month_count = max(1, min(months, 24))
        current_month = date.today().replace(day=1)
        first_month = subtract_months(current_month, month_count - 1)
        end_month = month_bounds(current_month)[1]
        rows = await self.repository.monthly_trend(
            db, user_id=user_id, start_date=first_month, end_date=end_month
        )
        by_month = {row["month"]: row for row in rows}
        trend: list[MonthlyTrendOut] = []
        for month_value in iter_months(first_month, month_count):
            month_key = month_value.strftime("%Y-%m")
            row = by_month.get(month_key, {})
            trend.append(
                MonthlyTrendOut(
                    month=month_key,
                    income=money(row.get("income", Decimal("0"))),
                    expenses=money(row.get("expenses", Decimal("0"))),
                    balance=money(row.get("balance", Decimal("0"))),
                )
            )
        return trend

    async def _budget_progress(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        month_value: date,
        income: Decimal,
        spent: Decimal,
    ) -> BudgetProgressOut | None:
        budget = await self.budget_repo.get_by_user_month(db, user_id, month_value)
        if budget:
            amount = budget.amount
            return BudgetProgressOut(
                amount=money(amount),
                spent=money(spent),
                percentage=percentage(spent, amount),
                remaining=money(max(amount - spent, Decimal("0"))),
                source="FIXED",
                is_dynamic=False,
            )

        if income <= 0:
            return None

        amount = income
        return BudgetProgressOut(
            amount=money(amount),
            spent=money(spent),
            percentage=percentage(spent, amount),
            remaining=money(max(amount - spent, Decimal("0"))),
            source="DYNAMIC_INCOME",
            is_dynamic=True,
        )


dashboard_service = DashboardService(dashboard_repository, budget_repository)
