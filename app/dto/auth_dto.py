from app.dto.base_dto import DTO


class Token(DTO):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(DTO):
    sub: str | None = None
    user_id: int | None = None
