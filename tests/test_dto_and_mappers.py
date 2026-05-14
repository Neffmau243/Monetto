from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.dto.budget_dto import BudgetCreate
from app.dto.user_dto import UserCreate
from app.main import app
from app.mappers.user_mapper import user_to_out
from app.models.user import User
from tests.conftest import _assert_safe_test_database_url


def test_user_create_requires_strong_password() -> None:
    with pytest.raises(ValidationError):
        UserCreate(name="Ada", email="ada@example.com", password="weakpass")


def test_budget_create_normalizes_month() -> None:
    budget = BudgetCreate(month=date(2026, 5, 22), amount=Decimal("1000.00"))
    assert budget.month == date(2026, 5, 1)


def test_user_mapper_hides_hashed_password() -> None:
    user = User(
        id=1,
        name="Ada",
        email="ada@example.com",
        hashed_password="hashed",
        created_at=datetime(2026, 5, 11, tzinfo=UTC),
    )
    dto = user_to_out(user)
    assert dto.email == "ada@example.com"
    assert not hasattr(dto, "hashed_password")


def test_test_database_guard_requires_test_suffix() -> None:
    _assert_safe_test_database_url("mysql+aiomysql://root:1234@localhost:3306/monetto_test")
    with pytest.raises(RuntimeError):
        _assert_safe_test_database_url("mysql+aiomysql://root:1234@localhost:3306/monetto")


def test_monthly_report_openapi_declares_json_and_pdf() -> None:
    content = app.openapi()["paths"]["/api/reports/monthly"]["get"]["responses"]["200"]["content"]

    assert "application/json" in content
    assert "application/pdf" in content
