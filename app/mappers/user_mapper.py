from app.dto.user_dto import UserOut
from app.models.user import User


def user_to_out(user: User) -> UserOut:
    return UserOut.model_validate(user)
