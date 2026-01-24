from fastapi import APIRouter

from budgetter_server.api.v1.endpoints import accounts, transactions, import_ofx

api_router = APIRouter()
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(import_ofx.router, prefix="/import", tags=["import"])
