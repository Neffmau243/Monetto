from collections.abc import Sequence
from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.enums import TransactionType
from app.models.transaction import Transaction


class DashboardRepository:
    async def summary_totals(
        self, db: AsyncSession, *, user_id: int, start_date: date, end_date: date
    ) -> tuple[Decimal, Decimal]:
        income_expr = self._sum_by_type(TransactionType.INCOME)
        expense_expr = self._sum_by_type(TransactionType.EXPENSE)
        result = await db.execute(
            select(income_expr.label("income"), expense_expr.label("expenses")).where(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date < end_date,
            )
        )
        row = result.one()
        return Decimal(row.income), Decimal(row.expenses)

    async def expenses_by_category(
        self, db: AsyncSession, *, user_id: int, start_date: date, end_date: date
    ) -> Sequence[dict[str, Any]]:
        category_totals = (
            select(
                Category.id.label("category_id"),
                Category.name.label("category_name"),
                func.sum(Transaction.amount).label("total"),
            )
            .join(Category, Category.id == Transaction.category_id)
            .where(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.EXPENSE,
                Transaction.date >= start_date,
                Transaction.date < end_date,
            )
            .group_by(Category.id, Category.name)
            .subquery()
        )
        total_window = func.sum(category_totals.c.total).over()
        percentage_expr = func.coalesce(
            (category_totals.c.total * 100) / func.nullif(total_window, 0), 0
        )
        result = await db.execute(
            select(
                category_totals.c.category_id,
                category_totals.c.category_name,
                category_totals.c.total,
                percentage_expr.label("percentage"),
            ).order_by(category_totals.c.total.desc(), category_totals.c.category_name.asc())
        )
        return [dict(row) for row in result.mappings().all()]

    async def monthly_trend(
        self, db: AsyncSession, *, user_id: int, start_date: date, end_date: date
    ) -> Sequence[dict[str, Any]]:
        month_expr = self._month_expression(db)
        income_expr = self._sum_by_type(TransactionType.INCOME)
        expense_expr = self._sum_by_type(TransactionType.EXPENSE)
        result = await db.execute(
            select(
                month_expr.label("month"),
                income_expr.label("income"),
                expense_expr.label("expenses"),
                (income_expr - expense_expr).label("balance"),
            )
            .where(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date < end_date,
            )
            .group_by(month_expr)
            .order_by(month_expr.asc())
        )
        return [dict(row) for row in result.mappings().all()]

    def _month_expression(self, db: AsyncSession):
        dialect_name = db.get_bind().dialect.name
        if dialect_name == "mysql":
            return func.date_format(Transaction.date, "%Y-%m")
        if dialect_name == "postgresql":
            return func.to_char(Transaction.date, "YYYY-MM")
        return func.strftime("%Y-%m", Transaction.date)

    def _sum_by_type(self, transaction_type: TransactionType):
        return func.coalesce(
            func.sum(case((Transaction.type == transaction_type, Transaction.amount), else_=0)),
            0,
        )


dashboard_repository = DashboardRepository()
