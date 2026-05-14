from app.dto.base_dto import DTO
from app.dto.dashboard_dto import DashboardSummaryOut, ExpensesByCategoryOut
from app.dto.transaction_dto import TransactionOut
from app.dto.user_dto import UserOut


class ReportMonthlyOut(DTO):
    user: UserOut
    month: str
    summary: DashboardSummaryOut
    transactions: list[TransactionOut]
    expenses_by_category: list[ExpensesByCategoryOut]
