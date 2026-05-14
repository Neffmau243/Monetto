from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.budget_dto import BudgetCreate
from app.dto.category_dto import CategoryCreate
from app.dto.transaction_dto import TransactionCreate
from app.dto.user_dto import UserCreate
from app.exceptions.domain import ConflictError, NotFoundError
from app.models.enums import TransactionType
from app.repositories.category_repository import category_repository
from app.repositories.user_repository import user_repository
from app.services.auth_service import auth_service
from app.services.budget_service import budget_service
from app.services.category_service import category_service
from app.services.transaction_service import transaction_service


@pytest.mark.asyncio
async def test_auth_service_hashes_password_and_rejects_duplicate(
    db_session: AsyncSession,
) -> None:
    user_in = UserCreate(name="Ada", email="ada@example.com", password="Strong123")
    await auth_service.create_user(db_session, user_in)

    user = await user_repository.get_by_email(db_session, "ada@example.com")
    assert user is not None
    assert user.hashed_password != "Strong123"

    with pytest.raises(ConflictError):
        await auth_service.create_user(db_session, user_in)


@pytest.mark.asyncio
async def test_category_service_rejects_duplicate_user_category(db_session: AsyncSession) -> None:
    user = await user_repository.create(
        db_session,
        {
            "name": "Ada",
            "email": "ada@example.com",
            "hashed_password": "hashed",
        },
    )
    category_in = CategoryCreate(name="Crypto", type=TransactionType.INCOME)
    await category_service.create_category(db_session, user.id, category_in)

    with pytest.raises(ConflictError):
        await category_service.create_category(db_session, user.id, category_in)


@pytest.mark.asyncio
async def test_transaction_service_requires_matching_category_type(
    db_session: AsyncSession,
) -> None:
    user = await user_repository.create(
        db_session,
        {
            "name": "Ada",
            "email": "ada@example.com",
            "hashed_password": "hashed",
        },
    )
    categories = await category_repository.list_for_user(db_session, user.id)
    expense_category = next(
        category for category in categories if category.type == TransactionType.EXPENSE
    )
    assert expense_category is not None

    with pytest.raises(NotFoundError):
        await transaction_service.create_transaction(
            db_session,
            user.id,
            TransactionCreate(
                type=TransactionType.INCOME,
                amount=Decimal("10.00"),
                description="Wrong",
                date=date(2026, 5, 1),
                category_id=expense_category.id,
            ),
        )


@pytest.mark.asyncio
async def test_budget_service_rejects_duplicate_month(db_session: AsyncSession) -> None:
    user = await user_repository.create(
        db_session,
        {
            "name": "Ada",
            "email": "ada@example.com",
            "hashed_password": "hashed",
        },
    )
    budget_in = BudgetCreate(month=date(2026, 5, 1), amount=Decimal("1000.00"))
    await budget_service.create_budget(db_session, user.id, budget_in)

    with pytest.raises(ConflictError):
        await budget_service.create_budget(db_session, user.id, budget_in)
