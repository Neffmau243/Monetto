from collections.abc import Sequence

from sqlalchemy import case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.enums import TransactionType
from app.models.transaction import Transaction
from app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    async def list_for_user(
        self,
        db: AsyncSession,
        user_id: int,
        category_type: TransactionType | None = None,
    ) -> Sequence[Category]:
        type_order = case((Category.type == TransactionType.INCOME, 0), else_=1)
        statement = select(Category).where(
            or_(Category.user_id.is_(None), Category.user_id == user_id)
        )
        if category_type:
            statement = statement.where(Category.type == category_type)
        result = await db.execute(
            statement.order_by(
                type_order.asc(),
                Category.is_default.desc(),
                Category.sort_order.asc(),
                Category.name.asc(),
                Category.id.asc(),
            )
        )
        return result.scalars().all()

    async def get_owned(self, db: AsyncSession, category_id: int, user_id: int) -> Category | None:
        result = await db.execute(
            select(Category).where(Category.id == category_id, Category.user_id == user_id)
        )
        return result.scalars().first()

    async def get_visible(
        self,
        db: AsyncSession,
        category_id: int,
        user_id: int,
        category_type: TransactionType | None = None,
    ) -> Category | None:
        statement = select(Category).where(
            Category.id == category_id,
            or_(Category.user_id.is_(None), Category.user_id == user_id),
        )
        if category_type:
            statement = statement.where(Category.type == category_type)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_duplicate(
        self,
        db: AsyncSession,
        *,
        user_id: int | None,
        name: str,
        category_type: TransactionType,
        exclude_id: int | None = None,
    ) -> Category | None:
        statement = select(Category).where(
            func.lower(Category.name) == name.lower(),
            Category.type == category_type,
        )
        if user_id is None:
            statement = statement.where(Category.user_id.is_(None))
        else:
            statement = statement.where(Category.user_id == user_id)
        if exclude_id:
            statement = statement.where(Category.id != exclude_id)
        result = await db.execute(statement)
        return result.scalars().first()

    async def count_transactions(self, db: AsyncSession, category_id: int) -> int:
        result = await db.execute(
            select(func.count(Transaction.id)).where(Transaction.category_id == category_id)
        )
        return int(result.scalar_one())


category_repository = CategoryRepository(Category)
