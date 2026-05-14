from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.health_service import health_service

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    return await health_service.check_database(db)
