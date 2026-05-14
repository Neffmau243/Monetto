from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.dto.auth_dto import Token
from app.dto.user_dto import UserCreate, UserLogin, UserOut
from app.mappers.user_mapper import user_to_out
from app.models.user import User
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> UserOut:
    return await auth_service.create_user(db, user_in)


@router.post("/login", response_model=Token)
async def login(login_in: UserLogin, db: AsyncSession = Depends(get_db)) -> Token:
    return await auth_service.login(db, login_in)


@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)) -> UserOut:
    return user_to_out(current_user)
