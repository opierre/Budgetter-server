from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from budgetter_server.db.session import get_session
from budgetter_server.models import Account
from budgetter_server.schemas.account import AccountCreate, AccountRead

router = APIRouter()


@router.post("/", response_model=AccountRead)
def create_account(
    *, 
    session: Session = Depends(get_session), 
    account: AccountCreate
) -> Account:
    """
    Create a new account.

    Args:
        session: Database session dependency.
        account: Account creation data.

    Returns:
        Account: The created account object.
    """
    db_account = Account.model_validate(account)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


@router.get("/", response_model=list[AccountRead])
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


@router.get("/{account_id}", response_model=AccountRead)
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
