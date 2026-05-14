from sqlalchemy.ext.asyncio import AsyncSession

from app.config.security import create_access_token, get_password_hash, verify_password
from app.dto.auth_dto import Token
from app.dto.user_dto import UserCreate, UserLogin, UserOut
from app.exceptions.domain import ConflictError, UnauthorizedError
from app.mappers.user_mapper import user_to_out
from app.models.user import User
from app.repositories.user_repository import UserRepository, user_repository


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> UserOut:
        email = user_in.email.lower()
        existing_user = await self.repository.get_by_email(db, email)
        if existing_user:
            raise ConflictError("Email already registered")

        user = await self.repository.create(
            db,
            {
                "name": user_in.name,
                "email": email,
                "hashed_password": get_password_hash(user_in.password),
            },
        )
        return user_to_out(user)

    async def authenticate_user(self, db: AsyncSession, login: UserLogin) -> User:
        user = await self.repository.get_by_email(db, login.email.lower())
        if not user or not verify_password(login.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        return user

    async def login(self, db: AsyncSession, login: UserLogin) -> Token:
        user = await self.authenticate_user(db, login)
        return Token(access_token=create_access_token(subject=user.id))


auth_service = AuthService(user_repository)
