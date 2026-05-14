from fastapi import APIRouter

from app.api.controllers import (
    auth_controller,
    budget_controller,
    category_controller,
    dashboard_controller,
    health_controller,
    report_controller,
    transaction_controller,
)

api_router = APIRouter()
api_router.include_router(health_controller.router)
api_router.include_router(auth_controller.router)
api_router.include_router(category_controller.router)
api_router.include_router(transaction_controller.router)
api_router.include_router(budget_controller.router)
api_router.include_router(dashboard_controller.router)
api_router.include_router(report_controller.router)
