from src.ai import validate_sql

validate_sql("SELECT category, SUM(revenue) AS revenue FROM sales GROUP BY category")
validate_sql("WITH x AS (SELECT * FROM sales) SELECT COUNT(*) FROM x")

for bad_sql in [
    "DELETE FROM sales",
    "DROP TABLE sales",
    "UPDATE sales SET revenue = 0",
    "SELECT * FROM sales; DROP TABLE sales",
]:
    try:
        validate_sql(bad_sql)
        raise AssertionError(f"Unsafe SQL was accepted: {bad_sql}")
    except ValueError:
        pass

print("SQL safety tests passed.")
