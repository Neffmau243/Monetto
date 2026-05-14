"""Initial Monetto schema.

Revision ID: 20260511_0001
Revises:
Create Date: 2026-05-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

revision: str = "20260511_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

id_type = sa.BigInteger().with_variant(mysql.BIGINT(unsigned=True), "mysql")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", id_type, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "categories",
        sa.Column("id", id_type, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("user_id", id_type, nullable=True),
        sa.Column("is_default", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.CheckConstraint(
            "type in ('INCOME', 'EXPENSE')", name="ck_categories_category_type_allowed"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_categories_user_id_users",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("user_id", "type", "name", name="uq_categories_user_type_name"),
    )
    op.create_index("ix_categories_user_type", "categories", ["user_id", "type"], unique=False)

    categories_table = sa.table(
        "categories",
        sa.column("name", sa.String),
        sa.column("type", sa.String),
        sa.column("user_id", id_type),
        sa.column("is_default", sa.Boolean),
    )
    op.bulk_insert(
        categories_table,
        [
            {"name": "Salario", "type": "INCOME", "user_id": None, "is_default": True},
            {"name": "Freelance", "type": "INCOME", "user_id": None, "is_default": True},
            {"name": "Inversiones", "type": "INCOME", "user_id": None, "is_default": True},
            {"name": "Alimentacion", "type": "EXPENSE", "user_id": None, "is_default": True},
            {"name": "Transporte", "type": "EXPENSE", "user_id": None, "is_default": True},
            {"name": "Vivienda", "type": "EXPENSE", "user_id": None, "is_default": True},
            {"name": "Servicios", "type": "EXPENSE", "user_id": None, "is_default": True},
            {"name": "Salud", "type": "EXPENSE", "user_id": None, "is_default": True},
            {"name": "Entretenimiento", "type": "EXPENSE", "user_id": None, "is_default": True},
        ],
    )

    op.create_table(
        "transactions",
        sa.Column("id", id_type, primary_key=True, autoincrement=True),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("category_id", id_type, nullable=False),
        sa.Column("user_id", id_type, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("amount > 0", name="ck_transactions_transaction_amount_positive"),
        sa.CheckConstraint(
            "type in ('INCOME', 'EXPENSE')", name="ck_transactions_transaction_type_allowed"
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name="fk_transactions_category_id_categories",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_transactions_user_id_users",
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_transactions_category", "transactions", ["category_id"], unique=False)
    op.create_index("ix_transactions_user_date", "transactions", ["user_id", "date"], unique=False)
    op.create_index(
        "ix_transactions_user_type_date", "transactions", ["user_id", "type", "date"], unique=False
    )

    op.create_table(
        "budgets",
        sa.Column("id", id_type, primary_key=True, autoincrement=True),
        sa.Column("user_id", id_type, nullable=False),
        sa.Column("month", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("amount > 0", name="ck_budgets_budget_amount_positive"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_budgets_user_id_users",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("user_id", "month", name="uq_budgets_user_month"),
    )
    op.create_index("ix_budgets_user_month", "budgets", ["user_id", "month"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_budgets_user_month", table_name="budgets")
    op.drop_table("budgets")
    op.drop_index("ix_transactions_user_type_date", table_name="transactions")
    op.drop_index("ix_transactions_user_date", table_name="transactions")
    op.drop_index("ix_transactions_category", table_name="transactions")
    op.drop_table("transactions")
    op.drop_index("ix_categories_user_type", table_name="categories")
    op.drop_table("categories")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
