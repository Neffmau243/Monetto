from datetime import date, timedelta

import pytest
from httpx import AsyncClient

from tests.conftest import get_category_id, register_and_login


@pytest.mark.asyncio
async def test_categories_require_auth(client: AsyncClient) -> None:
    response = await client.get("/api/categories")

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication token is required"


@pytest.mark.asyncio
async def test_categories_are_ordered_and_include_common_defaults(client: AsyncClient) -> None:
    headers = await register_and_login(client)

    response = await client.get("/api/categories", headers=headers)
    income_response = await client.get("/api/categories?type=INCOME", headers=headers)
    expense_response = await client.get("/api/categories?type=EXPENSE", headers=headers)

    assert response.status_code == 200
    assert income_response.status_code == 200
    assert expense_response.status_code == 200
    categories = response.json()
    income_categories = income_response.json()
    expense_categories = expense_response.json()
    names = [category["name"] for category in categories]
    types = [category["type"] for category in categories]
    assert categories[0]["name"] == "Salario"
    assert categories[0]["type"] == "INCOME"
    assert categories[0]["sort_order"] == 10
    assert categories[0]["display_order"] == 1
    assert types.index("INCOME") < types.index("EXPENSE")
    assert "Trabajos diarios" in names
    assert "Ventas" in names
    assert "Luz" in names
    assert "Agua" in names
    assert "Internet" in names
    assert "Juegos" in names
    assert "Salidas" in names
    assert {category["type"] for category in income_categories} == {"INCOME"}
    assert income_categories[0]["name"] == "Salario"
    assert income_categories[0]["display_order"] == 1
    assert {category["type"] for category in expense_categories} == {"EXPENSE"}
    assert expense_categories[0]["name"] == "Alimentacion"
    assert expense_categories[0]["display_order"] == 1


@pytest.mark.asyncio
async def test_category_crud_and_conflict_when_used(client: AsyncClient) -> None:
    headers = await register_and_login(client)

    unused = await client.post(
        "/api/categories",
        json={"name": "Regalos especiales", "type": "EXPENSE"},
        headers=headers,
    )
    created = await client.post(
        "/api/categories",
        json={"name": "Cursos", "type": "EXPENSE"},
        headers=headers,
    )
    unused_deleted = await client.delete(f"/api/categories/{unused.json()['id']}", headers=headers)
    updated = await client.put(
        f"/api/categories/{created.json()['id']}",
        json={"name": "Educacion"},
        headers=headers,
    )
    transaction = await client.post(
        "/api/transactions",
        json={
            "type": "EXPENSE",
            "amount": "50.00",
            "description": "Python",
            "date": date.today().isoformat(),
            "category_id": created.json()["id"],
        },
        headers=headers,
    )
    type_changed = await client.put(
        f"/api/categories/{created.json()['id']}",
        json={"type": "INCOME"},
        headers=headers,
    )
    deleted = await client.delete(f"/api/categories/{created.json()['id']}", headers=headers)

    assert unused.status_code == 201
    assert unused_deleted.status_code == 200
    assert unused_deleted.json()["message"] == "Categoria eliminada correctamente"
    assert created.status_code == 201
    assert updated.status_code == 200
    assert updated.json()["name"] == "Educacion"
    assert transaction.status_code == 201
    assert type_changed.status_code == 409
    assert deleted.status_code == 409


@pytest.mark.asyncio
async def test_transaction_crud_filters_validation_and_foreign_access(client: AsyncClient) -> None:
    headers = await register_and_login(client, email="ada@example.com")
    other_headers = await register_and_login(client, email="grace@example.com", name="Grace Hopper")
    income_category_id = await get_category_id(client, headers, type_="INCOME")
    expense_category_id = await get_category_id(client, headers, type_="EXPENSE")

    created = await client.post(
        "/api/transactions",
        json={
            "type": "INCOME",
            "amount": "1000.00",
            "description": "Salary",
            "date": date.today().isoformat(),
            "category_id": income_category_id,
        },
        headers=headers,
    )
    filtered = await client.get("/api/transactions?type=INCOME&page=1&limit=5", headers=headers)
    detail = await client.get(f"/api/transactions/{created.json()['id']}", headers=headers)
    updated = await client.put(
        f"/api/transactions/{created.json()['id']}",
        json={
            "type": "EXPENSE",
            "amount": "120.00",
            "category_id": expense_category_id,
            "date": date.today().isoformat(),
        },
        headers=headers,
    )
    forbidden = await client.get(f"/api/transactions/{created.json()['id']}", headers=other_headers)
    future = await client.post(
        "/api/transactions",
        json={
            "type": "EXPENSE",
            "amount": "10.00",
            "description": "Future",
            "date": (date.today() + timedelta(days=1)).isoformat(),
            "category_id": expense_category_id,
        },
        headers=headers,
    )
    deleted = await client.delete(f"/api/transactions/{created.json()['id']}", headers=headers)

    assert created.status_code == 201
    assert filtered.status_code == 200
    filtered_data = filtered.json()
    assert filtered_data["total"] == 1
    assert filtered_data["page"] == 1
    assert filtered_data["limit"] == 5
    assert filtered_data["total_pages"] == 1
    assert filtered_data["has_next"] is False
    assert filtered_data["has_previous"] is False
    assert detail.status_code == 200
    assert updated.status_code == 200
    assert updated.json()["type"] == "EXPENSE"
    assert forbidden.status_code == 403
    assert future.status_code == 422
    assert deleted.status_code == 200
    assert deleted.json()["message"] == "Transaccion eliminada correctamente"
