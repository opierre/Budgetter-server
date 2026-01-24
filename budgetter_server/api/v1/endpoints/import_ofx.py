from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session, select
from ofxtools.Parser import OFXTree
from ofxtools.models.bank.stmt import STMTRS
import io

from budgetter_server.db.session import get_session
from budgetter_server.models import Bank, Account, AccountType, Transaction, Mean, TransactionType

router = APIRouter()


@router.post("/ofx", response_model=dict[str, int])
async def import_ofx(
    file: Annotated[UploadFile, File()],
    session: Session = Depends(get_session)
) -> dict[str, int]:
    """
    Import transactions from an OFX file.

    Args:
        file: The OFX file to upload.
        session: Database session dependency.

    Returns:
        dict: Summary including the count of imported transactions.
    """
    if not file.filename.endswith(".ofx"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .ofx files are supported.")

    content = await file.read()
    
    # Parse OFX
    try:
        parser = OFXTree()
        parser.parse(io.BytesIO(content))
        ofx = parser.convert()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to parse OFX file: {exc}")

    imported_count = 0

    imported_count = 0

    # Use the statements shortcut provided by ofxtools (handles BANKMSGSRSV1 and CREDITCARDMSGSRSV1)
    if not hasattr(ofx, "statements"):
         # Fallback or empty
         return {"imported_count": 0}

    for stmt in ofx.statements:
        # Determine account info
        bank_id_str = "UNKNOWN"
        acct_id_str = "UNKNOWN"
        acct_type_enum = AccountType.CHECKING

        if hasattr(stmt, "bankacctfrom"):
            acct_info = stmt.bankacctfrom
            bank_id_str = str(acct_info.bankid) if hasattr(acct_info, "bankid") else "UNKNOWN"
            acct_id_str = str(acct_info.acctid)
            acct_type_node = acct_info.accttype if hasattr(acct_info, "accttype") else "CHECKING"
            try:
                acct_type_enum = AccountType(str(acct_type_node).upper())
            except ValueError:
                acct_type_enum = AccountType.CHECKING
        elif hasattr(stmt, "ccacctfrom"):
            acct_info = stmt.ccacctfrom
            bank_id_str = "UNKNOWN_CC"
            acct_id_str = str(acct_info.acctid)
            acct_type_enum = AccountType.CREDIT_CARD
        else:
            # Skip if no account info
            continue

        # Find or Create Bank
        bank = session.exec(select(Bank).where(Bank.swift == bank_id_str)).first()
        if not bank:
            bank = Bank(name=f"Bank {bank_id_str}", swift=bank_id_str)
            session.add(bank)
            session.commit()
            session.refresh(bank)

        # Find or Create Account
        account = session.exec(select(Account).where(Account.account_id == acct_id_str)).first()
        if not account:
            # Get balance
            balance = 0.0
            if hasattr(stmt, "ledgerbal") and hasattr(stmt.ledgerbal, "balamt"):
                balance = float(stmt.ledgerbal.balamt)
            
            account = Account(
                name=f"Imported {acct_id_str}",
                account_id=acct_id_str,
                account_type=acct_type_enum,
                bank_id=bank.id,
                amount=balance
            )
            session.add(account)
            session.commit()
            session.refresh(account)

        # Process Transactions
        transactions = []
        if hasattr(stmt, "banktranlist"):
            btl = stmt.banktranlist
            try:
                # Check for stmttrn (list or single)
                txns = btl.stmttrn
                if not isinstance(txns, list):
                    txns = [txns]
                transactions = txns
            except (AttributeError, KeyError):
                # Fallback
                if hasattr(btl, "__iter__"):
                     # Try iterating directly
                     transactions = list(btl)
        
        for txn in transactions:
            fitid = str(txn.fitid) if hasattr(txn, "fitid") else None
            if not fitid and hasattr(txn, "FITID"): fitid = str(txn.FITID)
            
            if not fitid: continue

            existing = session.exec(select(Transaction).where(Transaction.reference == fitid)).first()
            if existing:
                continue
            
            # Extract fields
            t_type = txn.trntype if hasattr(txn, "trntype") else "OTHER"
            amount = txn.trnamt if hasattr(txn, "trnamt") else 0
            
            # Date handling
            dt = None
            if hasattr(txn, "dtposted"):
                dt = txn.dtposted
            elif hasattr(txn, "dtuser"):
                dt = txn.dtuser
            
            if dt and hasattr(dt, "date"): 
                date_val = dt.date()
            else:
                import datetime
                date_val = datetime.date.today()

            name = str(txn.name) if hasattr(txn, "name") else ""
            memo = str(txn.memo) if hasattr(txn, "memo") else ""
            final_name = name if name else memo

            new_txn = Transaction(
                name=final_name,
                amount=amount,
                date=date_val,
                mean=Mean.CARD,
                transaction_type=TransactionType.EXPENSES if amount < 0 else TransactionType.INCOME,
                reference=fitid,
                account_id=account.id,
                comment=memo
            )
            session.add(new_txn)
            imported_count += 1
        
        session.commit()

    return {"imported_count": imported_count}
