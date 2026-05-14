from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.exceptions.domain import MonettoError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(MonettoError)
    async def handle_monetto_error(_: Request, exc: MonettoError) -> JSONResponse:
        return JSONResponse(status_code=int(exc.status_code), content={"detail": exc.detail})

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(_: Request, __: IntegrityError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": "Resource already exists or violates a database constraint"},
        )
