from datetime import date

import pytest
from httpx import AsyncClient

from tests.conftest import get_category_id, register_and_login


@pytest.mark.asyncio
async def test_budget_crud_and_duplicate_month(client: AsyncClient) -> None:
    headers = await register_and_login(client)

    created = await client.post(
        "/api/budgets",
        json={"month": "2026-05-01", "amount": "800.00"},
        headers=headers,
    )
    duplicate = await client.post(
        "/api/budgets",
        json={"month": "2026-05-01", "amount": "900.00"},
        headers=headers,
    )
    listed = await client.get("/api/budgets", headers=headers)
    updated = await client.put(
        f"/api/budgets/{created.json()['id']}",
        json={"amount": "1000.00"},
        headers=headers,
    )
    deleted = await client.delete(f"/api/budgets/{created.json()['id']}", headers=headers)

    assert created.status_code == 201
    assert duplicate.status_code == 409
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert updated.status_code == 200
    assert updated.json()["amount"] == "1000.00"
    assert deleted.status_code == 200
    assert deleted.json()["message"] == "Presupuesto eliminado correctamente"


@pytest.mark.asyncio
async def test_dashboard_and_reports(client: AsyncClient) -> None:
    headers = await register_and_login(client)
    income_category_id = await get_category_id(client, headers, type_="INCOME")
    expense_category_id = await get_category_id(client, headers, type_="EXPENSE")
    today = date.today()
    month = today.strftime("%Y-%m")

    await client.post(
        "/api/budgets",
        json={"month": today.replace(day=1).isoformat(), "amount": "500.00"},
        headers=headers,
    )
    await client.post(
        "/api/transactions",
        json={
            "type": "INCOME",
            "amount": "1000.00",
            "description": "Salary",
            "date": today.isoformat(),
            "category_id": income_category_id,
        },
        headers=headers,
    )
    await client.post(
        "/api/transactions",
        json={
            "type": "EXPENSE",
            "amount": "125.00",
            "description": "Groceries",
            "date": today.isoformat(),
            "category_id": expense_category_id,
        },
        headers=headers,
    )

    summary = await client.get(f"/api/dashboard/summary?month={month}", headers=headers)
    by_category = await client.get(
        f"/api/dashboard/expenses-by-category?month={month}", headers=headers
    )
    trend = await client.get("/api/dashboard/monthly-trend?months=3", headers=headers)
    report_json = await client.get(
        f"/api/reports/monthly?month={month}&format=json", headers=headers
    )
    report_pdf = await client.get(
        f"/api/reports/monthly?month={month}&format=pdf",
        headers=headers,
    )

    assert summary.status_code == 200
    assert summary.json()["total_income"] == "1000.00"
    assert summary.json()["total_expenses"] == "125.00"
    assert summary.json()["budget_info"]["percentage"] == "25.00"
    assert summary.json()["budget_info"]["remaining"] == "375.00"
    assert summary.json()["budget_info"]["source"] == "FIXED"
    assert summary.json()["budget_info"]["is_dynamic"] is False
    assert by_category.status_code == 200
    assert by_category.json()[0]["total"] == "125.00"
    assert trend.status_code == 200
    assert len(trend.json()) == 3
    assert report_json.status_code == 200
    assert len(report_json.json()["transactions"]) == 2
    assert report_pdf.status_code == 200
    assert report_pdf.headers["content-type"] == "application/pdf"
    assert report_pdf.content.startswith(b"%PDF")


@pytest.mark.asyncio
async def test_dashboard_uses_income_as_dynamic_budget_without_fixed_budget(
    client: AsyncClient,
) -> None:
    headers = await register_and_login(client)
    income_category_id = await get_category_id(client, headers, type_="INCOME")
    expense_category_id = await get_category_id(client, headers, type_="EXPENSE")
    today = date.today()
    month = today.strftime("%Y-%m")

    await client.post(
        "/api/transactions",
        json={
            "type": "INCOME",
            "amount": "200.00",
            "description": "Freelance",
            "date": today.isoformat(),
            "category_id": income_category_id,
        },
        headers=headers,
    )
    await client.post(
        "/api/transactions",
        json={
            "type": "EXPENSE",
            "amount": "50.00",
            "description": "Snack",
            "date": today.isoformat(),
            "category_id": expense_category_id,
        },
        headers=headers,
    )

    summary = await client.get(f"/api/dashboard/summary?month={month}", headers=headers)

    assert summary.status_code == 200
    assert summary.json()["budget_info"]["amount"] == "200.00"
    assert summary.json()["budget_info"]["spent"] == "50.00"
    assert summary.json()["budget_info"]["percentage"] == "25.00"
    assert summary.json()["budget_info"]["remaining"] == "150.00"
    assert summary.json()["budget_info"]["source"] == "DYNAMIC_INCOME"
    assert summary.json()["budget_info"]["is_dynamic"] is True
