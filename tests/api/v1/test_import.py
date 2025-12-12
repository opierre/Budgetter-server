from pathlib import Path
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from budgetter_server.models import Transaction, Bank, Account

class TestImport:
    """
    Test suite for OFX import.
    """

    def test_import_ofx(self, client: TestClient, session: Session) -> None:
        """
        Test importing an OFX file.
        
        Verifies:
            - Response 200 and count.
            - Bank, Account, and Transactions are created in DB.
        """
        file_path = Path(__file__).parent.parent.parent.joinpath("fixtures", "sample.ofx")
        with open(file_path, "rb") as f:
            response = client.post(
                "/api/v1/import/ofx",
                files={"file": ("sample.ofx", f, "application/x-ofx")}
            )
            
        assert response.status_code == 200
        data = response.json()
        assert data["imported_count"] == 2
        
        # Verify DB
        bank = session.exec(select(Bank).where(Bank.swift == "TESTBANK")).first()
        assert bank is not None
        assert bank.name == "Bank TESTBANK"
        
        account = session.exec(select(Account).where(Account.account_id == "123456789")).first()
        assert account is not None
        assert account.amount == 5000.00
        assert account.bank_id == bank.id
        
        txns = session.exec(select(Transaction).where(Transaction.account_id == account.id)).all()
        assert len(txns) == 2
        
        debit = next(t for t in txns if t.reference == "REF101")
        assert debit.amount == -50.00
        assert debit.name == "Grocery Store"
