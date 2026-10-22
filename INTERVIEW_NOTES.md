# Interview Notes — AI Business Analyst Assistant

## 30-second explanation

I built an AI Business Analyst Assistant using Python, SQL, SQLite, LangChain, an LLM API, Pandas, Plotly and Streamlit. A user can ask a business question in plain English, such as "Why did revenue drop in March?" The system generates a read-only SQL query, runs it on the sales database, visualizes the result and produces business-focused insights.

## Why this is a Data Analyst project

The main value is not the chatbot. The core workflow is:

business question → metric definition → SQL → data validation → analysis → visualization → business recommendation.

## Your role

I designed the data model, prepared the sales dataset, created the SQLite database, built the natural-language-to-SQL workflow, validated SQL for read-only execution, generated visualizations using Python, and added AI-generated business insights.

## Important technical point

The LLM does not directly modify the database. The application only allows SELECT/WITH queries and blocks data-changing SQL keywords.

## Interview questions

**Why SQLite?**  
It is lightweight and reproducible locally. The architecture can be moved to PostgreSQL or a cloud warehouse.

**Why LangChain?**  
I used it to structure the LLM prompt and model integration. The analytical logic remains in Python and SQL.

**How did you prevent dangerous SQL?**  
I validate the generated query, allow only SELECT/WITH statements, block data-changing/schema-changing keywords, and reject multiple statements.

**Can an LLM make mistakes?**  
Yes. That is why the application validates SQL, shows the generated query, and should use read-only database credentials and human approval in production.

**How would you make it production-ready?**  
Use PostgreSQL/warehouse access with read-only credentials, authentication, query timeouts, row limits, parser-based SQL validation, logging, tests, monitoring, prompt versioning and approval for sensitive queries.

## Do not say

Avoid: "The AI magically analyzes the data."

Say:

"The LLM generates a candidate SQL query from the business question. The database performs the actual aggregation, Python visualizes the returned data, and the LLM summarizes the returned evidence into business language."
