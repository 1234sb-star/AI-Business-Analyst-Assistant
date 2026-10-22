from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "business.db"
CSV_PATH = DATA_DIR / "sales_data.csv"

SCHEMA_DESCRIPTION = """
Table: sales
Columns:
  order_id INTEGER - unique order identifier
  order_date TEXT - ISO date YYYY-MM-DD
  customer_id TEXT - customer identifier
  customer_segment TEXT - Consumer, Corporate, Small Business
  category TEXT - product category
  product TEXT - product name
  quantity INTEGER - units ordered
  unit_price REAL - price per unit
  revenue REAL - realized revenue after returns/cancellations
  payment_method TEXT - UPI, Credit Card, Debit Card, Cash on Delivery
  order_status TEXT - Completed, Returned, Cancelled
  region TEXT - West, North, South, East

Business metrics:
  revenue = SUM(revenue)
  orders = COUNT(DISTINCT order_id)
  units = SUM(quantity)
  average_order_value = SUM(revenue) / COUNT(DISTINCT order_id)
  return_rate = returned_orders / total_orders
"""

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    DATA_DIR.mkdir(exist_ok=True)
    conn = get_connection()
    try:
        exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='sales'"
        ).fetchone()
        if exists is None:
            df = pd.read_csv(CSV_PATH)
            df.to_sql("sales", conn, if_exists="replace", index=False)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_category ON sales(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id)")
            conn.commit()
    finally:
        conn.close()

def run_query(sql: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()
