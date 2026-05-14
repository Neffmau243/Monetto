from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import TransactionType
from app.repositories.category_repository import category_repository
from app.repositories.transaction_repository import transaction_repository
from app.repositories.user_repository import user_repository


@pytest.mark.asyncio
async def test_user_repository_get_by_email(db_session: AsyncSession) -> None:
    await user_repository.create(
        db_session,
        {
            "name": "Ada",
            "email": "ada@example.com",
            "hashed_password": "hashed",
        },
    )

    user = await user_repository.get_by_email(db_session, "ada@example.com")

    assert user is not None
    assert user.name == "Ada"


@pytest.mark.asyncio
async def test_category_repository_lists_defaults_and_user_categories(
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
    await category_repository.create(
        db_session,
        {
            "name": "Bonos",
            "type": TransactionType.INCOME,
            "user_id": user.id,
            "is_default": False,
        },
    )

    categories = await category_repository.list_for_user(db_session, user.id)
    income_categories = await category_repository.list_for_user(
        db_session, user.id, TransactionType.INCOME
    )
    expense_categories = await category_repository.list_for_user(
        db_session, user.id, TransactionType.EXPENSE
    )

    assert any(category.is_default for category in categories)
    assert any(category.name == "Bonos" for category in categories)
    assert categories[0].type == TransactionType.INCOME
    assert categories[0].name == "Salario"
    assert categories[0].sort_order == 10
    assert {category.type for category in income_categories} == {TransactionType.INCOME}
    assert {category.type for category in expense_categories} == {TransactionType.EXPENSE}


@pytest.mark.asyncio
async def test_transaction_repository_filters_by_type(db_session: AsyncSession) -> None:
    user = await user_repository.create(
        db_session,
        {
            "name": "Ada",
            "email": "ada@example.com",
            "hashed_password": "hashed",
        },
    )
    income_category = await category_repository.get_visible(
        db_session, 1, user.id, TransactionType.INCOME
    )
    assert income_category is not None
    await transaction_repository.create(
        db_session,
        {
            "type": TransactionType.INCOME,
            "amount": Decimal("100.00"),
            "description": "Salary",
            "date": date(2026, 5, 1),
            "category_id": income_category.id,
            "user_id": user.id,
        },
    )

    transactions, total = await transaction_repository.list_for_user(
        db_session, user_id=user.id, type_=TransactionType.INCOME
    )

    assert total == 1
    assert transactions[0].type == TransactionType.INCOME
