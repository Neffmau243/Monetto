from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import ID_TYPE
from app.models.enums import TransactionType

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.user import User


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("type in ('INCOME', 'EXPENSE')", name="transaction_type_allowed"),
        CheckConstraint("amount > 0", name="transaction_amount_positive"),
        Index("ix_transactions_user_date", "user_id", "date"),
        Index("ix_transactions_user_type_date", "user_id", "type", "date"),
        Index("ix_transactions_category", "category_id"),
    )

    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, native_enum=False, length=20, validate_strings=True), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ID_TYPE, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ID_TYPE, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    category: Mapped[Category] = relationship(back_populates="transactions")
    user: Mapped[User] = relationship(back_populates="transactions")
