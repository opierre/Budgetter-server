from datetime import date
from typing import Optional

from pydantic import BaseModel, Field
from models.sql_models import AccountType, Status

class AccountBase(BaseModel):
    """
    Base schema for Account data.
    """
    name: Optional[str] = Field(default=None, description="Name of the account")
    account_id: str = Field(description="Unique account identifier from the bank")
    account_type: AccountType = Field(default=AccountType.CREDIT_CARD, description="Type of the account")
    amount: float = Field(default=0.0, description="Current balance")
    color: str = Field(default="", description="Color code for UI display")
    last_update: date = Field(description="Date of last update")
    status: Status = Field(default=Status.ACTIVE, description="Status of the account")
    bank_id: Optional[int] = Field(default=None, description="ID of the associated bank")

class AccountCreate(AccountBase):
    """
    Schema for creating a new Account.
    """
    pass

class AccountRead(AccountBase):
    """
    Schema for reading Account data (includes ID).
    """
    id: int = Field(description="Unique database identifier")

class AccountUpdate(BaseModel):
    """
    Schema for updating an Account.
    """
    name: Optional[str] = Field(default=None, description="New name for the account")
    amount: Optional[float] = Field(default=None, description="New balance amount")
    color: Optional[str] = Field(default=None, description="New color code")
