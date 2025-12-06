from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from budgetter_server.db.session import get_session
from budgetter_server.models import Transaction
from budgetter_server.schemas.transaction import TransactionCreate, TransactionRead

router = APIRouter()


@router.post("/", response_model=TransactionRead)
def create_transaction(
    *, 
    session: Session = Depends(get_session), 
    transaction: TransactionCreate
) -> Transaction:
    """
    Create a new transaction.

    Args:
        session: Database session dependency.
        transaction: Transaction creation data.

    Returns:
        Transaction: The created transaction object.
    """
    db_transaction = Transaction.model_validate(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@router.get("/", response_model=list[TransactionRead])
def read_transactions(
    *, 
    session: Session = Depends(get_session), 
    offset: int = 0, 
    limit: int = 100
) -> list[Transaction]:
    """
    Retrieve a list of transactions.

    Args:
        session: Database session dependency.
        offset: Number of records to skip (pagination).
        limit: Maximum number of records to return (pagination).

    Returns:
        list[Transaction]: List of transactions.
    """
    transactions = session.exec(select(Transaction).offset(offset).limit(limit)).all()
    return transactions
