from datetime import datetime

from pydantic import EmailStr, Field, field_validator

from app.dto.base_dto import DTO


class UserCreate(DTO):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_strong_password(cls, value: str) -> str:
        has_digit = any(char.isdigit() for char in value)
        has_upper = any(char.isupper() for char in value)
        if not has_digit or not has_upper:
            raise ValueError("Password must contain at least 1 digit and 1 uppercase letter")
        return value


class UserLogin(DTO):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserOut(DTO):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
