from enum import StrEnum
import datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel, Column


# Enums
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
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"


class Status(StrEnum):
    """Enumeration for account status."""
    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'


class BankBase(SQLModel):
    name: str = Field(default='', max_length=1000, description="Name of the bank")
    swift: str = Field(default='', max_length=1000, description="SWIFT code")
    bic: List[str] = Field(default_factory=list, sa_column=Column(JSON), description="List of BIC codes")


class Bank(BankBase, table=True):
    """Represents a banking institution."""
    id: Optional[int] = Field(default=None, primary_key=True)
    accounts: List["Account"] = Relationship(back_populates="bank")


class AccountBase(SQLModel):
    name: Optional[str] = Field(default='', max_length=1000, description="Account name")
    account_id: str = Field(default='', max_length=1000, unique=True, index=True, description="Unique account identifier")
    account_type: AccountType = Field(default=AccountType.CREDIT_CARD, description="Type of account")
    amount: float = Field(default=0.0, description="Current balance")
    color: str = Field(default='', max_length=1000, description="Display color")
    last_update: datetime.date = Field(default_factory=datetime.date.today, description="Last updated date")
    status: Status = Field(default=Status.ACTIVE, description="Account status")
    bank_id: Optional[int] = Field(default=None, foreign_key="bank.id", description="ID of the associated bank")


class Account(AccountBase, table=True):
    """Represents a financial account."""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    bank: Optional[Bank] = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(back_populates="account")


class CategoryBase(SQLModel):
    name: str = Field(default='', max_length=1000, description="Category name")


class Category(CategoryBase, table=True):
    """Represents a transaction category."""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    categorization_rules: List["CategorizationRule"] = Relationship(back_populates="category")
    transactions: List["Transaction"] = Relationship(back_populates="category")


class CategorizationRuleBase(SQLModel):
    keywords: str = Field(max_length=1000, description="Comma-separated keywords or regex")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", description="Target category ID")
    transaction_type: Optional[TransactionType] = Field(
        default=None, 
        description="Optional filter by transaction type"
    )

    def matches(self, name: str, memo: str) -> bool:
        """
        Check if the rule matches a transaction based on name or memo.
        """
        import re
        name_str = (name or '').lower()
        memo_str = (memo or '').lower()
        keyword_list = [kw.strip().lower() for kw in self.keywords.split(',')]
        
        for keyword in keyword_list:
            if keyword in name_str or keyword in memo_str:
                return True
            try:
                if re.search(keyword, name_str) or re.search(keyword, memo_str):
                    return True
            except re.error:
                continue
        return False


class CategorizationRule(CategorizationRuleBase, table=True):
    """Rules for automatically categorizing transactions."""
    id: Optional[int] = Field(default=None, primary_key=True)
    category: Optional[Category] = Relationship(back_populates="categorization_rules")


class TransactionBase(SQLModel):
    name: str = Field(default='', max_length=1000, description="Transaction name/payee")
    amount: Decimal = Field(max_digits=11, decimal_places=2, description="Transaction amount")
    date: datetime.date = Field(description="Date of transaction")
    comment: str = Field(default='', max_length=4000, description="User comment")
    mean: Mean = Field(default=Mean.CARD, description="Payment mean")
    transaction_type: TransactionType = Field(default=TransactionType.EXPENSES, description="Type of transaction")
    reference: str = Field(default='', max_length=1000, unique=True, index=True, description="Unique reference ID")
    account_id: Optional[int] = Field(default=None, foreign_key="account.id", description="Account ID")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", description="Category ID")


class Transaction(TransactionBase, table=True):
    """Represents a financial transaction."""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    account: Optional[Account] = Relationship(back_populates="transactions")
    category: Optional[Category] = Relationship(back_populates="transactions")
