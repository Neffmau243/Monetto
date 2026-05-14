from app.dto.budget_dto import BudgetOut
from app.models.budget import Budget


def budget_to_out(budget: Budget) -> BudgetOut:
    return BudgetOut.model_validate(budget)
