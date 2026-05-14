from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.dto.report_dto import ReportMonthlyOut
from app.models.user import User
from app.services.report_service import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get(
    "/monthly",
    response_model=None,
    responses={
        status.HTTP_200_OK: {
            "model": ReportMonthlyOut,
            "description": "Monthly report returned as JSON or PDF.",
            "content": {
                "application/pdf": {
                    "schema": {"type": "string", "format": "binary"},
                },
            },
        },
    },
)
async def monthly_report(
    month: str = Query(pattern=r"^\d{4}-\d{2}$"),
    format_: Literal["pdf", "json"] = Query(default="pdf", alias="format"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportMonthlyOut | StreamingResponse:
    if format_ == "json":
        return await report_service.monthly_json(db, user=current_user, month=month)

    pdf_buffer = await report_service.monthly_pdf(db, user=current_user, month=month)
    headers = {"Content-Disposition": f'attachment; filename="monetto-{month}.pdf"'}
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)
