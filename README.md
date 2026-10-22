# AI Business Analyst Assistant

A portfolio-ready Data Analyst project that lets a business user ask questions in plain English.

Example:

> Why did revenue drop in March?

The application:
1. Understands the business question using an LLM.
2. Generates safe SQLite SQL.
3. Runs the SQL against a sales database.
4. Displays the query result.
5. Creates an automatic visualization.
6. Generates business-focused AI insights.
7. Lets the user download the analysis as CSV.
8. Can be extended into a Power BI dashboard.

## Architecture

Streamlit UI
↓
LangChain + LLM
↓
SQL generation
↓
SQLite business database
↓
Pandas
↓
Plotly visualization
↓
AI business insight

## Technologies

- Python
- SQL / SQLite
- Pandas / NumPy
- LangChain
- OpenAI-compatible LLM API
- Plotly
- Streamlit
- Power BI

## VS Code setup

### 1. Open the project
VS Code → File → Open Folder → `AI_Business_Analyst_Assistant`

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Install packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure AI

Copy `.env.example` to `.env`.

Then add:

```text
OPENAI_API_KEY=your_real_key
OPENAI_MODEL=your_available_model_name
```

Never upload `.env` to GitHub.

### 5. Create the database

```powershell
python setup_database.py
```

### 6. Run

```powershell
streamlit run app.py
```

### 7. Test

Try:
- Why did revenue drop in March?
- Show monthly revenue and orders.
- Which category generated the most revenue?
- Who are the top 10 customers by revenue?
- What is the average order value by customer segment?
- Which region has the highest return rate?

## Resume bullets

**AI Business Analyst Assistant | Python, SQL, SQLite, LangChain, LLM API, Pandas, Plotly, Streamlit**

- Built a natural-language analytics assistant that converts business questions into safe SQL queries and executes them on a SQLite sales database.
- Developed Python/Pandas workflows for automated analysis and Plotly visualizations, with CSV export for downstream reporting.
- Added LLM-powered business insight generation to explain revenue, customer, product and regional trends in business-friendly language.
- Implemented SQL validation to restrict execution to read-only SELECT/WITH statements and prevent data modification.

## GitHub checklist

Upload:
- `app.py`
- `setup_database.py`
- `src/`
- `data/sales_data.csv`
- `powerbi/`
- `requirements.txt`
- `README.md`
- `.env.example`

Do NOT upload:
- `.env`
- `.venv/`
- `data/business.db` (optional; it can be regenerated)

## Portfolio upgrades

After the basic version works:
- PostgreSQL instead of SQLite
- Power BI dashboard screenshots
- Query history
- Authentication
- Human approval before executing generated SQL
- Multiple business tables
- Docker deployment
- Unit tests
