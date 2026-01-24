<br />
<div align="center">
  <h1 align="center">Budgetter-server</h1>
  <p align="center">
    🧾 Budgetter is a modern personal finance manager API.
    <br />
    <br />
    <a href="https://github.com/opierre/Budgetter/issues">Report Bug</a>
    ·
    <a href="https://github.com/opierre/Budgetter/issues">Request Feature</a>
    <br />
    <br />
    <a style="text-decoration:none" href="https://sonarcloud.io/summary/new_code?id=opierre_Budgetter" target="_blank">
      <img src="https://sonarcloud.io/api/project_badges/measure?project=opierre_Budgetter-server&metric=alert_status">
    </a>
    <a style="text-decoration:none" href="https://sonarcloud.io/summary/new_code?id=opierre_Budgetter" target="_blank">
      <img src="https://sonarcloud.io/api/project_badges/measure?project=opierre_Budgetter-server&metric=vulnerabilities">
    </a>
    <a style="text-decoration:none" href="https://sonarcloud.io/summary/new_code?id=opierre_Budgetter" target="_blank">
      <img src="https://sonarcloud.io/api/project_badges/measure?project=opierre_Budgetter-server&metric=bugs">
    </a>
    <a style="text-decoration:none" href="https://sonarcloud.io/summary/new_code?id=opierre_Budgetter" target="_blank">
      <img src="https://sonarcloud.io/api/project_badges/measure?project=opierre_Budgetter-server&metric=security_rating">
    </a>
    <a style="text-decoration:none" href="https://sonarcloud.io/summary/new_code?id=opierre_Budgetter" target="_blank">
      <img src="https://sonarcloud.io/api/project_badges/measure?project=opierre_Budgetter-server&metric=sqale_rating">
    </a>
    <a style="text-decoration:none" href="https://sonarcloud.io/summary/new_code?id=opierre_Budgetter" target="_blank">
      <img src="https://sonarcloud.io/api/project_badges/measure?project=opierre_Budgetter-server&metric=reliability_rating">
    </a>
  </p>
</div>

---

## 🚀 Features

- **FastAPI**: built on top of modern Python type hints.
- **OFX Import**: Easily import transaction files from your bank via the API.
- **REST API**: Comprehensive endpoints for Banks, Accounts, and Transactions.
- **Categorization Rules**: Database models to support custom categorization rules.
- **SQLModel**: Interaction with PostgreSQL using modern ORM.

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/opierre/Budgetter.git
   cd Budgetter-server
   ```

2. **Install dependencies**
   Using `uv` (recommended):
   ```bash
   uv sync
   ```
   
   Or standard `pip`:
   ```bash
   pip install -e .
   ```

3. **Database Configuration**
   Ensure you have a PostgreSQL database running and a `.env` file at the root:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```
   *The application creates tables automatically on startup.*

## 🏃 Usage

1. **Start the server**
   ```bash
   uvicorn budgetter_server.main:app --reload
   ```

2. **Access the Documentation**
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to explore the Swagger UI and test endpoints.

## 🧪 Testing

Run the test suite using `pytest`:

```bash
uv run pytest
# or
pytest
```