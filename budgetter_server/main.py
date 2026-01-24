from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from budgetter_server.api.v1.api import api_router
from budgetter_server.core.config import settings
from budgetter_server.db.session import create_db_and_tables
from budgetter_server.models import Bank, Account, Category, Transaction  

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.

    Args:
        app: The FastAPI application instance.
    """
    create_db_and_tables()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root() -> dict[str, str]:
    """
    Root endpoint for health check.

    Returns:
        dict: detailed welcome message.
    """
    return {"message": "Welcome to Budgetter Server API"}
