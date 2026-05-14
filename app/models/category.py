from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import ID_TYPE
from app.models.enums import TransactionType

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.user import User


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint("type in ('INCOME', 'EXPENSE')", name="category_type_allowed"),
        UniqueConstraint("user_id", "type", "name", name="uq_categories_user_type_name"),
        Index("ix_categories_user_type", "user_id", "type"),
    )

    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, native_enum=False, length=20, validate_strings=True), nullable=False
    )
    user_id: Mapped[int | None] = mapped_column(
        ID_TYPE, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1000, server_default="1000"
    )

    user: Mapped[User | None] = relationship(back_populates="categories")
    transactions: Mapped[list[Transaction]] = relationship(back_populates="category")
