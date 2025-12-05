from typing import Generator

from sqlmodel import Session, create_engine, SQLModel

from core.config import settings

engine = create_engine(settings.DATABASE_URL)


def create_db_and_tables() -> None:
    """
    Create the database structure and tables.
    
    This function uses SQLModel metadata to create tables in the database
    that do not already exist.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to provide a database session.
    
    Yields:
        Session: A SQLModel database session.
    """
    with Session(engine) as session:
        yield session
