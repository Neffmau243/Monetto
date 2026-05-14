from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class HealthService:
    async def check_database(self, db: AsyncSession) -> dict[str, str]:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}


health_service = HealthService()
