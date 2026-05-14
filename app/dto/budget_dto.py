from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import Field, field_validator

from app.dto.base_dto import DTO

Money = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=2)]


def normalize_month(value: date) -> date:
    return value.replace(day=1)


class BudgetCreate(DTO):
    month: date
    amount: Money

    @field_validator("month")
    @classmethod
    def validate_month(cls, value: date) -> date:
        return normalize_month(value)


class BudgetUpdate(DTO):
    month: date | None = None
    amount: Money | None = None

    @field_validator("month")
    @classmethod
    def validate_month(cls, value: date | None) -> date | None:
        return normalize_month(value) if value else value


class BudgetOut(DTO):
    id: int
    user_id: int
    month: date
    amount: Decimal
    created_at: datetime
    updated_at: datetime
