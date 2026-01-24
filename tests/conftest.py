import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Set env var BEFORE importing app modules to satisfy Settings validation
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from budgetter_server.main import app
from budgetter_server.db.session import get_session


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    """
    Creates a new database session for each test.
    
    This fixture:
    1. Creates an in-memory SQLite engine.
    2. Creates all tables defined in SQLModel metadata.
    3. Yields a session connected to this engine.
    4. Drops all tables after the test.
    """
    # Use SQLite in-memory database for tests
    engine = create_engine(
        "sqlite:///:memory:", # In-memory DB
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
    
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """
    Creates a TestClient with overridden database dependency.
    
    This ensures that the API uses the test database session
    instead of the production one.
    """
    def get_session_override():
        return session

    # Override the dependency
    app.dependency_overrides[get_session] = get_session_override
    
    client = TestClient(app)
    yield client
    
    # Clean up overrides
    app.dependency_overrides.clear()
