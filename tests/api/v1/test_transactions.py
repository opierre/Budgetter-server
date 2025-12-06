from fastapi.testclient import TestClient
from sqlmodel import Session, select

from budgetter_server.models.sql_models import Transaction, Mean, TransactionType, AccountType, Status


class TestTransactions:
    """
    Test suite for transactions API endpoints.
    """

    def test_create_transaction(self, client: TestClient, session: Session) -> None:
        """
        Test creating a new transaction.
        
        Verifies:
            - Response status code is 200.
            - Database actually contains the new transaction.
        """
        # Create an account first (dependency)
        client.post(
            "/api/v1/accounts/",
            json={
                "name": "Test Account",
                "account_id": "ACC123",
                "account_type": AccountType.CREDIT_CARD,
                "status": Status.ACTIVE,
                "amount": 100.0,
                "color": "red",
                "last_update": "2023-01-01"
            }
        )
        
        # Create transaction
        response = client.post(
            "/api/v1/transactions/",
            json={
                "name": "Groceries",
                "amount": 50.25,
                "date": "2023-11-15",
                "comment": "Weekly shopping",
                "mean": Mean.CARD,
                "transaction_type": TransactionType.EXPENSES,
                "reference": "REF123456",
                "account_id": 1
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Groceries"
        assert data["amount"] == "50.25"
        
        # Verify DB update directly via session
        statement = select(Transaction).where(Transaction.reference == "REF123456")
        transaction_in_db = session.exec(statement).first()
        assert transaction_in_db is not None
        assert transaction_in_db.name == "Groceries"
        assert transaction_in_db.amount == 50.25

    def test_read_transactions(self, client: TestClient) -> None:
        """
        Test reading transactions list.
        """
        response = client.get("/api/v1/transactions/")
        assert response.status_code == 200        
        assert isinstance(response.json(), list)
