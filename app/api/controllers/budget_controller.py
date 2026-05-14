from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.dto.budget_dto import BudgetCreate, BudgetOut, BudgetUpdate
from app.dto.message_dto import MessageOut
from app.models.user import User
from app.services.budget_service import budget_service

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("", response_model=BudgetOut, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_in: BudgetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BudgetOut:
    return await budget_service.create_budget(db, current_user.id, budget_in)


@router.get("", response_model=list[BudgetOut])
async def list_budgets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[BudgetOut]:
    return await budget_service.list_budgets(db, current_user.id)


@router.put("/{budget_id}", response_model=BudgetOut)
async def update_budget(
    budget_id: int,
    budget_in: BudgetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BudgetOut:
    return await budget_service.update_budget(db, current_user.id, budget_id, budget_in)


@router.delete("/{budget_id}", response_model=MessageOut)
async def delete_budget(
    budget_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageOut:
    await budget_service.delete_budget(db, current_user.id, budget_id)
    return MessageOut(message="Presupuesto eliminado correctamente")
