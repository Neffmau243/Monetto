"""Add category ordering and richer defaults.

Revision ID: 20260511_0002
Revises: 20260511_0001
Create Date: 2026-05-11
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260511_0002"
down_revision: str | None = "20260511_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

DEFAULT_CATEGORIES = (
    ("Salario", "INCOME", 10),
    ("Freelance", "INCOME", 20),
    ("Trabajos diarios", "INCOME", 30),
    ("Ventas", "INCOME", 40),
    ("Bonos", "INCOME", 50),
    ("Inversiones", "INCOME", 60),
    ("Regalos", "INCOME", 70),
    ("Reembolsos", "INCOME", 80),
    ("Otros ingresos", "INCOME", 90),
    ("Alimentacion", "EXPENSE", 100),
    ("Transporte", "EXPENSE", 110),
    ("Vivienda", "EXPENSE", 120),
    ("Luz", "EXPENSE", 130),
    ("Agua", "EXPENSE", 140),
    ("Internet", "EXPENSE", 150),
    ("Servicios", "EXPENSE", 160),
    ("Salud", "EXPENSE", 170),
    ("Educacion", "EXPENSE", 180),
    ("Suscripciones", "EXPENSE", 190),
    ("Entretenimiento", "EXPENSE", 200),
    ("Juegos", "EXPENSE", 210),
    ("Salidas", "EXPENSE", 220),
    ("Compras", "EXPENSE", 230),
    ("Emergencias", "EXPENSE", 240),
    ("Otros gastos", "EXPENSE", 250),
)

NEW_DEFAULT_NAMES = (
    "Trabajos diarios",
    "Ventas",
    "Bonos",
    "Regalos",
    "Reembolsos",
    "Otros ingresos",
    "Luz",
    "Agua",
    "Internet",
    "Educacion",
    "Suscripciones",
    "Juegos",
    "Salidas",
    "Compras",
    "Emergencias",
    "Otros gastos",
)


def upgrade() -> None:
    op.add_column(
        "categories",
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="1000"),
    )

    for name, category_type, sort_order in DEFAULT_CATEGORIES:
        op.execute(
            f"""
            UPDATE categories
            SET sort_order = {sort_order}, is_default = 1
            WHERE user_id IS NULL
              AND type = '{category_type}'
              AND LOWER(name) = LOWER('{name}')
            """
        )
        op.execute(
            f"""
            INSERT INTO categories (name, type, user_id, is_default, sort_order)
            SELECT '{name}', '{category_type}', NULL, 1, {sort_order}
            WHERE NOT EXISTS (
                SELECT 1
                FROM categories
                WHERE user_id IS NULL
                  AND type = '{category_type}'
                  AND LOWER(name) = LOWER('{name}')
            )
            """
        )


def downgrade() -> None:
    quoted_names = ", ".join(f"'{name}'" for name in NEW_DEFAULT_NAMES)
    op.execute(
        f"""
        DELETE c
        FROM categories c
        LEFT JOIN transactions t ON t.category_id = c.id
        WHERE c.user_id IS NULL
          AND t.id IS NULL
          AND c.name IN ({quoted_names})
        """
    )
    op.drop_column("categories", "sort_order")
