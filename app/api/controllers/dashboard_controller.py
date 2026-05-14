from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.dto.dashboard_dto import DashboardSummaryOut, ExpensesByCategoryOut, MonthlyTrendOut
from app.models.user import User
from app.services.dashboard_service import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummaryOut)
async def summary(
    month: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardSummaryOut:
    return await dashboard_service.summary(db, user_id=current_user.id, month=month)


@router.get("/expenses-by-category", response_model=list[ExpensesByCategoryOut])
async def expenses_by_category(
    month: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ExpensesByCategoryOut]:
    return await dashboard_service.expenses_by_category(db, user_id=current_user.id, month=month)


@router.get("/monthly-trend", response_model=list[MonthlyTrendOut])
async def monthly_trend(
    months: int = Query(default=6, ge=1, le=24),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[MonthlyTrendOut]:
    return await dashboard_service.monthly_trend(db, user_id=current_user.id, months=months)
