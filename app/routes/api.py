from fastapi import APIRouter

from routes.auth_routes import router as auth_router
from routes.dividends_routes import router as dividends_router
from routes.user_routes import router as user_router
from routes.transaction_routes import router as transaction_router
from routes.portfolio_routes import router as portfolio_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(dividends_router)
api_router.include_router(user_router)
api_router.include_router(transaction_router)
api_router.include_router(portfolio_router)