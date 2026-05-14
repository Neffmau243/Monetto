import pytest
from httpx import AsyncClient
from sqlalchemy.exc import IntegrityError

from app.services.auth_service import auth_service


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


@pytest.mark.asyncio
async def test_register_login_and_duplicate_email(client: AsyncClient) -> None:
    payload = {"name": "Ada", "email": "ada@example.com", "password": "Strong123"}

    created = await client.post("/api/auth/register", json=payload)
    duplicate = await client.post("/api/auth/register", json=payload)
    login = await client.post(
        "/api/auth/login", json={"email": "ada@example.com", "password": "Strong123"}
    )
    me = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {login.json()['access_token']}"},
    )

    assert created.status_code == 201
    assert "hashed_password" not in created.json()
    assert duplicate.status_code == 409
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"
    assert me.status_code == 200
    assert me.json()["name"] == "Ada"


@pytest.mark.asyncio
async def test_register_rejects_weak_password(client: AsyncClient) -> None:
    response = await client.post(
        "/api/auth/register",
        json={"name": "Ada", "email": "ada@example.com", "password": "weakpass"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_integrity_error_returns_conflict(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def raise_integrity_error(*_: object, **__: object) -> None:
        raise IntegrityError("INSERT", {}, Exception("duplicate"))

    monkeypatch.setattr(auth_service, "create_user", raise_integrity_error)

    response = await client.post(
        "/api/auth/register",
        json={"name": "Ada", "email": "ada@example.com", "password": "Strong123"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Resource already exists or violates a database constraint"
