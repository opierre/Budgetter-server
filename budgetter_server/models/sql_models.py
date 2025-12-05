"""
SQLModel database models for the Budgetter application.
"""
from enum import StrEnum
import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel, Column


class Mean(StrEnum):
    """Enumeration for transaction means."""
    CARD = 'CARD'
    CASH = 'CASH'
    TRANSFER = 'TRANSFER'


class TransactionType(StrEnum):
    """Enumeration for transaction types."""
    EXPENSES = 'EXPENSES'
    INCOME = 'INCOME'
    INTERNAL = 'INTERNAL'


class AccountType(StrEnum):
    """Enumeration for account types."""
    CREDIT_CARD = "CREDIT CARD"


class Status(StrEnum):
    """Enumeration for account status."""
    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'


class Bank(SQLModel, table=True):
    """
    Represents a banking institution.

    Attributes:
        id: Unique identifier for the bank.
        name: Name of the bank.
        swift: SWIFT code of the bank.
        bic: List of BIC codes associated with the bank.
        accounts: List of accounts belonging to this bank.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default='', max_length=1000, description="Name of the bank")
    swift: str = Field(default='', max_length=1000, description="SWIFT code")
    bic: list[str] = Field(default_factory=list, sa_column=Column(JSON), description="List of BIC codes")

    accounts: list["Account"] = Relationship(back_populates="bank")


class Account(SQLModel, table=True):
    """
    Represents a financial account.

    Attributes:
        id: Unique database identifier.
        name: User-friendly name of the account.
        account_id: Unique account number/identifier from the bank.
        account_type: Type of the account (e.g., Credit Card).
        bank_id: Foreign key to the Bank.
        amount: Current balance or amount.
        color: Visual color for the account in UI.
        last_update: Date of the last update.
        status: Active or Closed status.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default='', max_length=1000, description="Account name")
    account_id: str = Field(default='', max_length=1000, unique=True, index=True, description="Unique account identifier")
    account_type: AccountType = Field(default=AccountType.CREDIT_CARD, description="Type of account")
    
    bank_id: Optional[int] = Field(default=None, foreign_key="bank.id", description="ID of the associated bank")
    bank: Optional[Bank] = Relationship(back_populates="accounts")
    
    amount: float = Field(default=0.0, description="Current balance")
    color: str = Field(default='', max_length=1000, description="Display color")
    last_update: datetime.date = Field(default_factory=datetime.date.today, description="Last updated date")
    status: Status = Field(default=Status.ACTIVE, description="Account status")

    transactions: list["Transaction"] = Relationship(back_populates="account")


class Category(SQLModel, table=True):
    """
    Represents a transaction category.

    Attributes:
        id: Unique identifier.
        name: Name of the category.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default='', max_length=1000, description="Category name")
    
    categorization_rules: list["CategorizationRule"] = Relationship(back_populates="category")
    transactions: list["Transaction"] = Relationship(back_populates="category")


class CategorizationRule(SQLModel, table=True):
    """
    Rules for automatically categorizing transactions.

    Attributes:
        id: Unique identifier.
        keywords: Comma-separated keywords or regex patterns.
        category_id: ID of the category to assign.
        transaction_type: Optional filter for transaction type.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    keywords: str = Field(max_length=1000, description="Comma-separated keywords or regex")
    
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", description="Target category ID")
    category: Optional[Category] = Relationship(back_populates="categorization_rules")
    
    transaction_type: Optional[TransactionType] = Field(
        default=None, 
        description="Optional filter by transaction type"
    )

    def matches(self, name: str, memo: str) -> bool:
        """
        Check if the rule matches a transaction based on name or memo.

        Args:
            name: The name/payee of the transaction.
            memo: The description/memo of the transaction.

        Returns:
            bool: True if keywords match, False otherwise.
        """
        import re
        name_str = (name or '').lower()
        memo_str = (memo or '').lower()
        keyword_list = [kw.strip().lower() for kw in self.keywords.split(',')]
        
        for keyword in keyword_list:
            # Try exact match
            if keyword in name_str or keyword in memo_str:
                return True
            # Try regex
            try:
                if re.search(keyword, name_str) or re.search(keyword, memo_str):
                    return True
            except re.error:
                continue
        return False


class Transaction(SQLModel, table=True):
    """
    Represents a financial transaction.

    Attributes:
        id: Unique identifier.
        name: Transaction name/payee.
        amount: Transaction amount.
        date: Date of the transaction.
        account_id: ID of the account.
        category_id: ID of the category.
        comment: Optional comment/note.
        mean: Mean of payment (Card, Cash, etc.).
        transaction_type: Type (Expense, Income, etc.).
        reference: Unique reference string.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default='', max_length=1000, description="Transaction name/payee")
    amount: Decimal = Field(max_digits=11, decimal_places=2, description="Transaction amount")
    date: datetime.date = Field(description="Date of transaction")
    
    account_id: Optional[int] = Field(default=None, foreign_key="account.id", description="Account ID")
    account: Optional[Account] = Relationship(back_populates="transactions")
    
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", description="Category ID")
    category: Optional[Category] = Relationship(back_populates="transactions")
    
    comment: str = Field(default='', max_length=4000, description="User comment")
    mean: Mean = Field(default=Mean.CARD, description="Payment mean")
    transaction_type: TransactionType = Field(default=TransactionType.EXPENSES, description="Type of transaction")
    reference: str = Field(default='', max_length=1000, unique=True, index=True, description="Unique reference ID")
