from collections.abc import Sequence
from datetime import date

from sqlalchemy import ColumnElement, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.enums import TransactionType
from app.models.transaction import Transaction
from app.repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    async def get_with_category(self, db: AsyncSession, transaction_id: int) -> Transaction | None:
        result = await db.execute(
            select(Transaction)
            .options(joinedload(Transaction.category))
            .where(Transaction.id == transaction_id)
        )
        return result.scalars().first()

    async def list_for_user(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        type_: TransactionType | None = None,
        category_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[Sequence[Transaction], int]:
        filters = self._filters(user_id, type_, category_id, date_from, date_to)
        total_result = await db.execute(select(func.count(Transaction.id)).where(*filters))
        total = int(total_result.scalar_one())

        result = await db.execute(
            select(Transaction)
            .options(joinedload(Transaction.category))
            .where(*filters)
            .order_by(Transaction.date.desc(), Transaction.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
        return result.scalars().all(), total

    async def list_for_user_month(
        self, db: AsyncSession, *, user_id: int, start_date: date, end_date: date
    ) -> Sequence[Transaction]:
        result = await db.execute(
            select(Transaction)
            .options(joinedload(Transaction.category))
            .where(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date < end_date,
            )
            .order_by(Transaction.date.desc(), Transaction.id.desc())
        )
        return result.scalars().all()

    def _filters(
        self,
        user_id: int,
        type_: TransactionType | None,
        category_id: int | None,
        date_from: date | None,
        date_to: date | None,
    ) -> list[ColumnElement[bool]]:
        filters = [Transaction.user_id == user_id]
        if type_:
            filters.append(Transaction.type == type_)
        if category_id:
            filters.append(Transaction.category_id == category_id)
        if date_from:
            filters.append(Transaction.date >= date_from)
        if date_to:
            filters.append(Transaction.date <= date_to)
        return filters


transaction_repository = TransactionRepository(Transaction)
