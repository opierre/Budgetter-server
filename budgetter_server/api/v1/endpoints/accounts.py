from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from budgetter_server.db.session import get_session
from budgetter_server.models import Account, AccountBase

router = APIRouter()


@router.post("/", response_model=Account)
def create_account(
    *, 
    session: Session = Depends(get_session), 
    account: AccountBase
) -> Account:
    """
    Create a new account.

    Args:
        session: Database session dependency.
        account: Account creation data (AccountBase).

    Returns:
        Account: The created account object.
    """
    db_account = Account.model_validate(account)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


@router.get("/", response_model=list[Account], response_model_exclude={"transactions", "bank"})
def read_accounts(
    *, 
    session: Session = Depends(get_session), 
    offset: int = 0, 
    limit: int = 100
) -> list[Account]:
    """
    Retrieve a list of accounts.

    Args:
        session: Database session dependency.
        offset: Number of records to skip (pagination).
        limit: Maximum number of records to return (pagination).

    Returns:
        list[Account]: List of accounts.
    """
    accounts = session.exec(select(Account).offset(offset).limit(limit)).all()
    return accounts


@router.get("/{account_id}", response_model=Account, response_model_exclude={"transactions", "bank"})
def read_account(
    *, 
    session: Session = Depends(get_session), 
    account_id: int
) -> Account:
    """
    Retrieve a specific account by ID.

    Args:
        session: Database session dependency.
        account_id: ID of the account to retrieve.

    Returns:
        Account: The requested account.

    Raises:
        HTTPException: If the account is not found.
    """
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{account_id}", response_model=Account, response_model_exclude={"transactions", "bank"})
def update_account(
    *,
    session: Session = Depends(get_session),
    account_id: int,
    account_update: AccountBase
) -> Account:
    """
    Update an account.

    Args:
        session: Database session dependency.
        account_id: ID of the account to update.
        account_update: Account update data (AccountBase).

    Returns:
        Account: The updated account object.

    Raises:
        HTTPException: If the account is not found.
    """
    db_account = session.get(Account, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account_data = account_update.model_dump(exclude_unset=True)
    for key, value in account_data.items():
        setattr(db_account, key, value)
        
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


@router.delete("/{account_id}")
def delete_account(
    *,
    session: Session = Depends(get_session),
    account_id: int
):
    """
    Delete an account.

    Args:
        session: Database session dependency.
        account_id: ID of the account to delete.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the account is not found.
    """
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    session.delete(account)
    session.commit()
    return {"ok": True}
