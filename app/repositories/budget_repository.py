from collections.abc import Sequence
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.budget import Budget
from app.repositories.base_repository import BaseRepository


class BudgetRepository(BaseRepository[Budget]):
    async def get_for_user(
        self,
        db: AsyncSession,
        budget_id: int,
        user_id: int,
    ) -> Budget | None:
        result = await db.execute(
            select(Budget).where(Budget.id == budget_id, Budget.user_id == user_id)
        )
        return result.scalars().first()

    async def get_by_user_month(
        self,
        db: AsyncSession,
        user_id: int,
        month: date,
    ) -> Budget | None:
        result = await db.execute(
            select(Budget).where(Budget.user_id == user_id, Budget.month == month)
        )
        return result.scalars().first()

    async def list_for_user(self, db: AsyncSession, user_id: int) -> Sequence[Budget]:
        result = await db.execute(
            select(Budget).where(Budget.user_id == user_id).order_by(Budget.month.desc())
        )
        return result.scalars().all()


budget_repository = BudgetRepository(Budget)
