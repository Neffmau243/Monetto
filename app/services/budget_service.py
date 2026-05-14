from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.budget_dto import BudgetCreate, BudgetOut, BudgetUpdate
from app.exceptions.domain import ConflictError, ForbiddenError, NotFoundError
from app.mappers.budget_mapper import budget_to_out
from app.models.budget import Budget
from app.repositories.budget_repository import BudgetRepository, budget_repository


class BudgetService:
    def __init__(self, repository: BudgetRepository) -> None:
        self.repository = repository

    async def create_budget(
        self,
        db: AsyncSession,
        user_id: int,
        budget_in: BudgetCreate,
    ) -> BudgetOut:
        existing = await self.repository.get_by_user_month(db, user_id, budget_in.month)
        if existing:
            raise ConflictError("Budget already exists for this month")
        budget = await self.repository.create(
            db, {"user_id": user_id, "month": budget_in.month, "amount": budget_in.amount}
        )
        return budget_to_out(budget)

    async def list_budgets(self, db: AsyncSession, user_id: int) -> list[BudgetOut]:
        budgets = await self.repository.list_for_user(db, user_id)
        return [budget_to_out(budget) for budget in budgets]

    async def update_budget(
        self, db: AsyncSession, user_id: int, budget_id: int, budget_in: BudgetUpdate
    ) -> BudgetOut:
        budget = await self._get_owned_budget(db, user_id, budget_id)
        values = budget_in.model_dump(exclude_unset=True)
        target_month = values.get("month", budget.month)
        if target_month != budget.month:
            existing = await self.repository.get_by_user_month(db, user_id, target_month)
            if existing:
                raise ConflictError("Budget already exists for this month")
        updated = await self.repository.update(db, budget, values)
        return budget_to_out(updated)

    async def delete_budget(self, db: AsyncSession, user_id: int, budget_id: int) -> None:
        budget = await self._get_owned_budget(db, user_id, budget_id)
        await self.repository.delete(db, budget)

    async def _get_owned_budget(self, db: AsyncSession, user_id: int, budget_id: int) -> Budget:
        budget = await self.repository.get(db, budget_id)
        if not budget:
            raise NotFoundError("Budget not found")
        if budget.user_id != user_id:
            raise ForbiddenError("You can only access your own budgets")
        return budget


budget_service = BudgetService(budget_repository)
