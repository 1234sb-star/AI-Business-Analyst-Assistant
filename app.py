import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

from src.database import initialize_database, run_query, SCHEMA_DESCRIPTION
from src.ai import generate_sql, generate_insight

st.set_page_config(
    page_title="AI Business Analyst Assistant",
    page_icon="📊",
    layout="wide"
)

initialize_database()

st.title("📊 AI Business Analyst Assistant")
st.caption(
    "Business question → AI SQL → database → Python analysis → visualization → AI insight"
)

with st.sidebar:
    st.header("Try these questions")
    examples = [
        "Why did revenue drop in March?",
        "Show monthly revenue and orders.",
        "Which product categories generated the most revenue?",
        "Who are the top 10 customers by revenue?",
        "What is the average order value by customer segment?",
        "Which region has the highest return rate?",
        "Compare revenue by payment method.",
    ]
    selected = st.selectbox("Example question", ["Choose..."] + examples)

    st.divider()
    st.subheader("Project stack")
    st.write("Python • SQL • SQLite • LangChain • LLM API • Pandas • Plotly • Streamlit")

if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input(
    "Ask a business question",
    value="" if selected == "Choose..." else selected,
    placeholder="Example: Why did revenue drop in March?"
)

if st.button("🔎 Analyze", type="primary"):
    if not question.strip():
        st.warning("Please enter a business question.")
        st.stop()

    try:
        with st.spinner("Generating SQL..."):
            sql = generate_sql(question, SCHEMA_DESCRIPTION)

        with st.expander("1️⃣ Generated SQL", expanded=True):
            st.code(sql, language="sql")

        with st.spinner("Running SQL on the business database..."):
            result = run_query(sql)

        if result.empty:
            st.info("The query returned no rows.")
            st.stop()

        st.subheader("2️⃣ Query Result")
        st.dataframe(result, use_container_width=True)

        st.download_button(
            "⬇️ Download result as CSV",
            result.to_csv(index=False).encode("utf-8"),
            file_name="analysis_result.csv",
            mime="text/csv"
        )

        st.subheader("3️⃣ Visualization")
        numeric_cols = result.select_dtypes(include="number").columns.tolist()
        date_like = [
            c for c in result.columns
            if "date" in c.lower() or "month" in c.lower()
        ]
        text_cols = [c for c in result.columns if c not in numeric_cols]

        fig = None
        if date_like and numeric_cols:
            fig = px.line(
                result,
                x=date_like[0],
                y=numeric_cols[0],
                markers=True,
                title=f"{numeric_cols[0]} over {date_like[0]}"
            )
        elif text_cols and numeric_cols:
            fig = px.bar(
                result.head(15),
                x=text_cols[0],
                y=numeric_cols[0],
                title=f"{numeric_cols[0]} by {text_cols[0]}"
            )
        elif len(numeric_cols) >= 2:
            fig = px.scatter(
                result,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title=f"{numeric_cols[1]} vs {numeric_cols[0]}"
            )

        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("The result is best viewed as a table.")

        with st.spinner("Generating business insights..."):
            insight = generate_insight(
                question,
                sql,
                result.head(50).to_csv(index=False)
            )

        st.subheader("4️⃣ AI-Powered Business Insights")
        st.markdown(insight)

        st.session_state.history.append({
            "question": question,
            "rows": len(result)
        })

    except Exception as exc:
        st.error(f"Analysis failed: {exc}")
        st.info(
            "Check your .env API key, model name, internet connection, "
            "and the terminal error."
        )

if st.session_state.history:
    st.divider()
    st.subheader("Recent questions")
    for item in reversed(st.session_state.history[-5:]):
        st.write(f"• {item['question']} — {item['rows']} rows returned")
