from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.dto.message_dto import MessageOut
from app.dto.transaction_dto import (
    PaginatedTransactionsOut,
    TransactionCreate,
    TransactionOut,
    TransactionUpdate,
)
from app.models.enums import TransactionType
from app.models.user import User
from app.services.transaction_service import transaction_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_in: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionOut:
    return await transaction_service.create_transaction(db, current_user.id, transaction_in)


@router.get("", response_model=PaginatedTransactionsOut)
async def list_transactions(
    type_: TransactionType | None = Query(default=None, alias="type"),
    category_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PaginatedTransactionsOut:
    return await transaction_service.list_transactions(
        db,
        user_id=current_user.id,
        type_=type_,
        category_id=category_id,
        date_from=date_from,
        date_to=date_to,
        page=page,
        limit=limit,
    )


@router.get("/{transaction_id}", response_model=TransactionOut)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionOut:
    return await transaction_service.get_transaction(db, current_user.id, transaction_id)


@router.put("/{transaction_id}", response_model=TransactionOut)
async def update_transaction(
    transaction_id: int,
    transaction_in: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionOut:
    return await transaction_service.update_transaction(
        db, current_user.id, transaction_id, transaction_in
    )


@router.delete("/{transaction_id}", response_model=MessageOut)
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageOut:
    await transaction_service.delete_transaction(db, current_user.id, transaction_id)
    return MessageOut(message="Transaccion eliminada correctamente")
