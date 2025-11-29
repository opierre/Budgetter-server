<br />
<div align="center">
  <h1 align="center">Budgetter-server</h1>
  <p align="center">
    🧾 Budgetter is a personal finance management software such as <a href="https://en.wikipedia.org/wiki/Microsoft_Money">Money</a>.
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

- **OFX Import**: Easily import transaction files from your bank.
- **AI Categorization**: Automatically categorizes transactions using a local AI model (DistilBART).
  - **Privacy First**: The AI runs entirely on your machine. No data leaves your server.
  - **Zero-Shot**: No training required. It understands categories like "Groceries" or "Transport" out of the box.
- **Rule-Based Engine**: Define custom rules for exact matches (highest priority).
- **Dashboard**: Visualize your spending with charts and graphs.

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/opierre/Budgetter.git
   cd Budgetter/budgetter_server
   ```

2. **Install dependencies**
   ```bash
   pip install .
   # Or for development (editable mode):
   # pip install -e .
   ```
   *Note: This will install `transformers` and `torch` for the AI features (~2GB).*

3. **Apply migrations**
   ```bash
   python manage.py makemigrations
   ```
   ```bash
   python manage.py migrate
   ```

## 🏃 Usage

1. **Start the server**
   ```bash
   python manage.py runserver
   ```
   *On first launch, the AI model (~300MB) will be downloaded and cached automatically.*

2. **Access the app**
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## 🧪 Testing

Run the comprehensive test suite to verify functionality:

```bash
# Run tests
python manage.py test dashboard.tests_coverage

# Run with coverage report
coverage run --source='dashboard,utils' manage.py test dashboard.tests_coverage
coverage report
```