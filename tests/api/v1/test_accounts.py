from fastapi.testclient import TestClient
from sqlmodel import Session

from budgetter_server.schemas.account import AccountCreate
from budgetter_server.models.sql_models import AccountType, Status


class TestAccounts:
    """
    Test suite for accounts API endpoints.
    """

    def test_create_account(self, client: TestClient) -> None:
        """
        Test creating a new account via API.
        
        Verifies:
            - Response status code is 200.
            - Response JSON contains expected fields.
        """
        response = client.post(
            "/api/v1/accounts/",
            json={
                "name": "Test Savings",
                "account_id": "SAV001",
                "account_type": AccountType.CREDIT_CARD,
                "amount": 1000.50,
                "color": "blue",
                "last_update": "2023-10-01",
                "status": Status.ACTIVE
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Savings"
        assert data["account_id"] == "SAV001"
        assert data["amount"] == 1000.50
        assert "id" in data

    def test_read_accounts(self, client: TestClient) -> None:
        """
        Test reading accounts list.
        
        Verifies:
            - Response status code is 200.
            - Returns a list of accounts.
        """
        # Create an account first
        client.post(
            "/api/v1/accounts/",
            json={
                "name": "Test Checking",
                "account_id": "CHK001",
                "account_type": AccountType.CREDIT_CARD,
                "amount": 500.0,
                "color": "green",
                "last_update": "2023-10-01",
                "status": Status.ACTIVE
            }
        )
        
        response = client.get("/api/v1/accounts/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == "Test Checking"
