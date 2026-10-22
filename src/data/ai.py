import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()


def get_llm():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key or api_key == "your_gemini_api_key_here":
        return None

    return genai.Client(api_key=api_key)


def clean_sql(text: str) -> str:
    text = text.strip()

    match = re.search(
        r"```(?:sql)?\s*(.*?)```",
        text,
        flags=re.I | re.S
    )

    if match:
        text = match.group(1).strip()

    text = re.sub(
        r"^(SQL\s*:|Query\s*:)",
        "",
        text,
        flags=re.I
    ).strip()

    return text.rstrip(";").strip()


def validate_sql(sql: str) -> None:
    normalized = re.sub(r"\s+", " ", sql.strip()).lower()

    if not (
        normalized.startswith("select ")
        or normalized.startswith("with ")
    ):
        raise ValueError("Only SELECT/WITH queries are allowed.")

    blocked = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "create ",
        "replace ",
        "truncate ",
        "attach ",
        "detach ",
        "pragma ",
    ]

    for keyword in blocked:
        if keyword in normalized:
            raise ValueError(
                f"Blocked SQL operation detected: {keyword.strip()}"
            )

    if ";" in sql:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )


def generate_sql(question: str, schema: str) -> str:
    client = get_llm()

    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    prompt = f"""
You are a senior data analyst who writes safe SQLite SQL.

Rules:
1. Return ONLY one SQL query.
2. Use only the table and columns in the schema.
3. Only SELECT or WITH queries are allowed.
4. Never modify data.
5. Prefer clear aliases.
6. For monthly trends, use strftime('%Y-%m', order_date).
7. Revenue means SUM(revenue).
8. AOV means SUM(revenue) / COUNT(DISTINCT order_id).
9. If comparing categories, group by category.
10. If the question asks why revenue changed, break the result
    into useful dimensions such as category, customer, region,
    and order status.

Schema:
{schema}

Business question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    sql = clean_sql(response.text)
    validate_sql(sql)

    return sql


def generate_insight(
    question: str,
    sql: str,
    result_csv: str
) -> str:

    client = get_llm()

    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    prompt = f"""
You are a business analyst.
Explain data findings to a non-technical manager.

Use only the supplied query result.
Do not invent facts.

Return:
- 2 to 4 concise findings
- 1 business implication
- 1 recommended next action

Business question:
{question}

SQL:
{sql}

Query result:
{result_csv[:12000]}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text.strip()