import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import make_url
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

TEST_DATABASE_URL = os.getenv(
    "TEST_DB_URL",
    "mysql+aiomysql://root:1234@localhost:3306/monetto_test",
)


def _assert_safe_test_database_url(database_url: str) -> None:
    url = make_url(database_url)
    database_name = url.database or ""
    if url.drivername.startswith("sqlite") and database_name in {"", ":memory:"}:
        return
    if not database_name.endswith("_test"):
        raise RuntimeError(
            "Refusing to run destructive tests against a non-test database. "
            "Set TEST_DB_URL to a database whose name ends with '_test'."
        )


def _is_ci() -> bool:
    return os.getenv("CI", "").lower() in {"1", "true", "yes"}


_assert_safe_test_database_url(TEST_DATABASE_URL)
os.environ["DB_URL"] = TEST_DATABASE_URL
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DEBUG"] = "false"

from app import models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.category import Category
from app.utils.default_categories import DEFAULT_CATEGORIES


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, pool_pre_ping=True)

    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
    except OperationalError as exc:
        await engine.dispose()
        message = (
            "MySQL test database is not available. Create database monetto_test or set TEST_DB_URL."
        )
        if _is_ci():
            raise RuntimeError(message) from exc
        pytest.skip(message)

    SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with SessionLocal() as session:
        for category in DEFAULT_CATEGORIES:
            session.add(
                Category(
                    name=str(category["name"]),
                    type=category["type"],
                    user_id=None,
                    is_default=True,
                    sort_order=int(category["sort_order"]),
                )
            )
        await session.commit()
        yield session

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        try:
            yield db_session
            await db_session.commit()
        except Exception:
            await db_session.rollback()
            raise

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client
    app.dependency_overrides.clear()


async def register_and_login(
    client: AsyncClient,
    *,
    email: str = "ada@example.com",
    name: str = "Ada Lovelace",
    password: str = "Strong123",
) -> dict[str, str]:
    await client.post(
        "/api/auth/register",
        json={"name": name, "email": email, "password": password},
    )
    response = await client.post("/api/auth/login", json={"email": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def get_category_id(
    client: AsyncClient, headers: dict[str, str], *, type_: str, name: str | None = None
) -> int:
    response = await client.get("/api/categories", headers=headers)
    categories = response.json()
    for category in categories:
        if category["type"] == type_ and (name is None or category["name"] == name):
            return category["id"]
    raise AssertionError(f"Category {type_}/{name} not found")
