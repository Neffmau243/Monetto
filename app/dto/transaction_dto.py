from __future__ import annotations

from datetime import date as date_type
from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import Field, field_validator

from app.dto.base_dto import DTO
from app.dto.category_dto import CategoryOut
from app.models.enums import TransactionType

Money = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=2)]


def _date_not_future(value: date_type) -> date_type:
    if value > date_type.today():
        raise ValueError("Date cannot be in the future")
    return value


class TransactionCreate(DTO):
    type: TransactionType
    amount: Money
    description: str | None = Field(default=None, max_length=255)
    date: date_type
    category_id: int

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: date_type) -> date_type:
        return _date_not_future(value)


class TransactionUpdate(DTO):
    type: TransactionType | None = None
    amount: Money | None = None
    description: str | None = Field(default=None, max_length=255)
    date: date_type | None = None
    category_id: int | None = None

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: date_type | None) -> date_type | None:
        return _date_not_future(value) if value else value


class TransactionOut(DTO):
    id: int
    type: TransactionType
    amount: Decimal
    description: str | None
    date: date_type
    category_id: int
    user_id: int
    created_at: datetime
    category: CategoryOut | None = None


class PaginatedTransactionsOut(DTO):
    items: list[TransactionOut]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool
