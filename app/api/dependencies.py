from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import user_repository

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/login",
    auto_error=False,
)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str | None = Depends(oauth2_scheme),
) -> User:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        raw_user_id = payload.get("user_id") or payload.get("sub")
        user_id = int(raw_user_id)
    except (JWTError, TypeError, ValueError) as exc:
        raise credentials_exception from exc

    user = await user_repository.get(db, user_id)
    if user is None:
        raise credentials_exception
    return user
