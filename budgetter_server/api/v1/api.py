from fastapi import APIRouter

from .endpoints import accounts, transactions

api_router = APIRouter()
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
