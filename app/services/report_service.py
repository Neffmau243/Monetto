from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.report_dto import ReportMonthlyOut
from app.mappers.transaction_mapper import transaction_to_out
from app.mappers.user_mapper import user_to_out
from app.models.user import User
from app.repositories.transaction_repository import TransactionRepository, transaction_repository
from app.services.dashboard_service import DashboardService, dashboard_service
from app.utils.dates import month_bounds, parse_month


class ReportService:
    def __init__(
        self,
        dashboard: DashboardService,
        transactions: TransactionRepository,
    ) -> None:
        self.dashboard = dashboard
        self.transactions = transactions

    async def monthly_json(
        self, db: AsyncSession, *, user: User, month: str | None = None
    ) -> ReportMonthlyOut:
        parsed_month = parse_month(month)
        start_date, end_date = month_bounds(parsed_month)
        month_key = parsed_month.strftime("%Y-%m")
        summary = await self.dashboard.summary(db, user_id=user.id, month=month_key)
        expenses_by_category = await self.dashboard.expenses_by_category(
            db, user_id=user.id, month=month_key
        )
        transactions = await self.transactions.list_for_user_month(
            db, user_id=user.id, start_date=start_date, end_date=end_date
        )
        return ReportMonthlyOut(
            user=user_to_out(user),
            month=month_key,
            summary=summary,
            transactions=[transaction_to_out(transaction) for transaction in transactions],
            expenses_by_category=expenses_by_category,
        )

    async def monthly_pdf(
        self,
        db: AsyncSession,
        *,
        user: User,
        month: str | None = None,
    ) -> BytesIO:
        report = await self.monthly_json(db, user=user, month=month)
        buffer = BytesIO()
        document = SimpleDocTemplate(buffer, pagesize=letter, title=f"Monetto {report.month}")
        styles = getSampleStyleSheet()
        elements = [
            Paragraph("Reporte mensual Monetto", styles["Title"]),
            Paragraph(f"Usuario: {report.user.name} ({report.user.email})", styles["Normal"]),
            Paragraph(f"Mes: {report.month}", styles["Normal"]),
            Spacer(1, 12),
        ]

        elements.append(self._summary_table(report))
        elements.append(Spacer(1, 16))
        elements.append(Paragraph("Transacciones", styles["Heading2"]))
        elements.append(self._transactions_table(report))
        elements.append(Spacer(1, 16))
        elements.append(Paragraph("Gastos por categoria", styles["Heading2"]))
        elements.append(self._categories_table(report))

        document.build(elements)
        buffer.seek(0)
        return buffer

    def _summary_table(self, report: ReportMonthlyOut) -> Table:
        data = [
            ["Ingresos", "Gastos", "Balance"],
            [
                str(report.summary.total_income),
                str(report.summary.total_expenses),
                str(report.summary.balance),
            ],
        ]
        if report.summary.budget_info:
            budget_mode = (
                "Dinamico por ingresos"
                if report.summary.budget_info.is_dynamic
                else "Fijo mensual"
            )
            data.extend(
                [
                    ["Presupuesto", "Gastado", "Uso"],
                    [
                        str(report.summary.budget_info.amount),
                        str(report.summary.budget_info.spent),
                        f"{report.summary.budget_info.percentage}%",
                    ],
                    ["Disponible", "Modo", ""],
                    [
                        str(report.summary.budget_info.remaining),
                        budget_mode,
                        "",
                    ],
                ]
            )
        return self._styled_table(data)

    def _transactions_table(self, report: ReportMonthlyOut) -> Table:
        data = [["Fecha", "Tipo", "Categoria", "Descripcion", "Monto"]]
        data.extend(
            [
                [
                    item.date.isoformat(),
                    item.type.value,
                    item.category.name if item.category else "-",
                    item.description or "-",
                    str(item.amount),
                ]
                for item in report.transactions
            ]
        )
        if len(data) == 1:
            data.append(["-", "-", "-", "Sin transacciones", "-"])
        return self._styled_table(data)

    def _categories_table(self, report: ReportMonthlyOut) -> Table:
        data = [["Categoria", "Total", "Porcentaje"]]
        data.extend(
            [
                [item.category_name, str(item.total), f"{item.percentage}%"]
                for item in report.expenses_by_category
            ]
        )
        if len(data) == 1:
            data.append(["Sin gastos", "0.00", "0.00%"])
        return self._styled_table(data)

    def _styled_table(self, data: list[list[str]]) -> Table:
        table = Table(data, hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F2937")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D1D5DB")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#F9FAFB")],
                    ),
                ]
            )
        )
        return table


report_service = ReportService(dashboard_service, transaction_repository)
