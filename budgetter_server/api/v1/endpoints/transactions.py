from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from budgetter_server.db.session import get_session
from budgetter_server.models import Transaction, TransactionBase

router = APIRouter()


@router.post("/", response_model=Transaction)
def create_transaction(
    *, 
    session: Session = Depends(get_session), 
    transaction: TransactionBase
) -> Transaction:
    """
    Create a new transaction.

    Args:
        session: Database session dependency.
        transaction: Transaction creation data (TransactionBase).

    Returns:
        Transaction: The created transaction object.
    """
    db_transaction = Transaction.model_validate(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@router.get("/", response_model=list[Transaction], response_model_exclude={"account", "category"})
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


@router.get("/{transaction_id}", response_model=Transaction, response_model_exclude={"account", "category"})
def read_transaction(
    *,
    session: Session = Depends(get_session),
    transaction_id: int
) -> Transaction:
    """
    Retrieve a specific transaction by ID.

    Args:
        session: Database session dependency.
        transaction_id: ID of the transaction to retrieve.

    Returns:
        Transaction: The requested transaction.

    Raises:
        HTTPException: If the transaction is not found.
    """
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=Transaction, response_model_exclude={"account", "category"})
def update_transaction(
    *,
    session: Session = Depends(get_session),
    transaction_id: int,
    transaction_update: TransactionBase
) -> Transaction:
    """
    Update a transaction.

    Args:
        session: Database session dependency.
        transaction_id: ID of the transaction to update.
        transaction_update: Transaction update data (TransactionBase).

    Returns:
        Transaction: The updated transaction object.

    Raises:
        HTTPException: If the transaction is not found.
    """
    db_transaction = session.get(Transaction, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    transaction_data = transaction_update.model_dump(exclude_unset=True)
    for key, value in transaction_data.items():
        setattr(db_transaction, key, value)
        
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    *,
    session: Session = Depends(get_session),
    transaction_id: int
):
    """
    Delete a transaction.

    Args:
        session: Database session dependency.
        transaction_id: ID of the transaction to delete.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the transaction is not found.
    """
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    session.delete(transaction)
    session.commit()
    return {"ok": True}
