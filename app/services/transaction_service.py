from datetime import date
from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.transaction_dto import (
    PaginatedTransactionsOut,
    TransactionCreate,
    TransactionOut,
    TransactionUpdate,
)
from app.exceptions.domain import ForbiddenError, NotFoundError
from app.mappers.transaction_mapper import transaction_to_out
from app.models.enums import TransactionType
from app.models.transaction import Transaction
from app.repositories.category_repository import CategoryRepository, category_repository
from app.repositories.transaction_repository import TransactionRepository, transaction_repository


class TransactionService:
    def __init__(
        self,
        repository: TransactionRepository,
        category_repo: CategoryRepository,
    ) -> None:
        self.repository = repository
        self.category_repo = category_repo

    async def create_transaction(
        self, db: AsyncSession, user_id: int, transaction_in: TransactionCreate
    ) -> TransactionOut:
        await self._ensure_valid_category(
            db, user_id, transaction_in.category_id, transaction_in.type
        )
        transaction = await self.repository.create(
            db,
            {
                **transaction_in.model_dump(),
                "user_id": user_id,
            },
        )
        transaction = await self.repository.get_with_category(db, transaction.id) or transaction
        return transaction_to_out(transaction)

    async def list_transactions(
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
    ) -> PaginatedTransactionsOut:
        transactions, total = await self.repository.list_for_user(
            db,
            user_id=user_id,
            type_=type_,
            category_id=category_id,
            date_from=date_from,
            date_to=date_to,
            page=page,
            limit=limit,
        )
        total_pages = max(1, ceil(total / limit))
        return PaginatedTransactionsOut(
            items=[transaction_to_out(transaction) for transaction in transactions],
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )

    async def get_transaction(
        self,
        db: AsyncSession,
        user_id: int,
        transaction_id: int,
    ) -> TransactionOut:
        transaction = await self._get_owned_transaction(db, user_id, transaction_id)
        return transaction_to_out(transaction)

    async def update_transaction(
        self,
        db: AsyncSession,
        user_id: int,
        transaction_id: int,
        transaction_in: TransactionUpdate,
    ) -> TransactionOut:
        transaction = await self._get_owned_transaction(db, user_id, transaction_id)
        values = transaction_in.model_dump(exclude_unset=True)
        target_type = values.get("type", transaction.type)
        target_category_id = values.get("category_id", transaction.category_id)
        if "type" in values or "category_id" in values:
            await self._ensure_valid_category(db, user_id, target_category_id, target_type)
        updated = await self.repository.update(db, transaction, values)
        updated = await self.repository.get_with_category(db, updated.id) or updated
        return transaction_to_out(updated)

    async def delete_transaction(
        self,
        db: AsyncSession,
        user_id: int,
        transaction_id: int,
    ) -> None:
        transaction = await self._get_owned_transaction(db, user_id, transaction_id)
        await self.repository.delete(db, transaction)

    async def _get_owned_transaction(
        self, db: AsyncSession, user_id: int, transaction_id: int
    ) -> Transaction:
        transaction = await self.repository.get_with_category(db, transaction_id)
        if not transaction:
            raise NotFoundError("Transaction not found")
        if transaction.user_id != user_id:
            raise ForbiddenError("You can only access your own transactions")
        return transaction

    async def _ensure_valid_category(
        self,
        db: AsyncSession,
        user_id: int,
        category_id: int,
        transaction_type: TransactionType,
    ) -> None:
        category = await self.category_repo.get_visible(db, category_id, user_id, transaction_type)
        if not category:
            raise NotFoundError("Category not found for this user and transaction type")


transaction_service = TransactionService(transaction_repository, category_repository)
