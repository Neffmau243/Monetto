from http import HTTPStatus


class MonettoError(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class ConflictError(MonettoError):
    status_code = HTTPStatus.CONFLICT


class UnauthorizedError(MonettoError):
    status_code = HTTPStatus.UNAUTHORIZED


class ForbiddenError(MonettoError):
    status_code = HTTPStatus.FORBIDDEN


class NotFoundError(MonettoError):
    status_code = HTTPStatus.NOT_FOUND


class ValidationError(MonettoError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
