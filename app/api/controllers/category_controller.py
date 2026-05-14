from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.dto.category_dto import CategoryCreate, CategoryOut, CategoryUpdate
from app.dto.message_dto import MessageOut
from app.models.enums import TransactionType
from app.models.user import User
from app.services.category_service import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryOut])
async def list_categories(
    type_: TransactionType | None = Query(default=None, alias="type"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CategoryOut]:
    return await category_service.list_categories(db, current_user.id, type_)


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CategoryOut:
    return await category_service.create_category(db, current_user.id, category_in)


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CategoryOut:
    return await category_service.update_category(db, current_user.id, category_id, category_in)


@router.delete("/{category_id}", response_model=MessageOut)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageOut:
    await category_service.delete_category(db, current_user.id, category_id)
    return MessageOut(message="Categoria eliminada correctamente")
