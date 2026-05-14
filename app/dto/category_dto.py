from pydantic import Field

from app.dto.base_dto import DTO
from app.models.enums import TransactionType


class CategoryCreate(DTO):
    name: str = Field(min_length=2, max_length=120)
    type: TransactionType


class CategoryUpdate(DTO):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    type: TransactionType | None = None


class CategoryOut(DTO):
    id: int
    name: str
    type: TransactionType
    user_id: int | None
    is_default: bool
    sort_order: int
    display_order: int = 0
