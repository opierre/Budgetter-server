import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from budgetter_server.models.sql_models import Mean, TransactionType

class TransactionBase(BaseModel):
    """
    Base schema for Transaction data.
    """
    name: str = Field(description="Name or payee of the transaction")
    amount: Decimal = Field(description="Transaction amount")
    date: datetime.date = Field(description="Date of the transaction")
    comment: Optional[str] = Field(default="", description="Optional user comment")
    mean: Mean = Field(default=Mean.CARD, description="Payment method used")
    transaction_type: TransactionType = Field(default=TransactionType.EXPENSES, description="Type of transaction (Income/Expense)")
    reference: str = Field(description="Unique reference ID for the transaction")
    account_id: Optional[int] = Field(default=None, description="ID of the associated account")
    category_id: Optional[int] = Field(default=None, description="ID of the associated category")

class TransactionCreate(TransactionBase):
    """
    Schema for creating a new Transaction.
    """
    pass

class TransactionRead(TransactionBase):
    """
    Schema for reading Transaction data.
    """
    id: int = Field(description="Unique database identifier")

class TransactionUpdate(BaseModel):
    """
    Schema for updating a Transaction.
    """
    name: Optional[str] = Field(default=None, description="New name")
    amount: Optional[Decimal] = Field(default=None, description="New amount")
    comment: Optional[str] = Field(default=None, description="New comment")
    category_id: Optional[int] = Field(default=None, description="New category ID")
