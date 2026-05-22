import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import pandas as pd
import plotly.express as px
import streamlit as st

from app.database.db import get_engine

engine = get_engine()

st.set_page_config(
    page_title="ThemisFin AI Dashboard",
    layout="wide"
)

st.title(
    "ThemisFin AI — Audit & Compliance Dashboard"
)

# =====================================================
# LOAD DATA
# =====================================================

transactions_df = pd.read_sql(
    "SELECT * FROM transactions",
    engine
)

anomalies_df = pd.read_sql(
    "SELECT * FROM anomaly_flags",
    engine
)

# =====================================================
# KPIs
# =====================================================

total_transactions = len(
    transactions_df
)

total_anomalies = len(
    anomalies_df
)

avg_risk_score = (
    anomalies_df["severity_score"].mean()
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Transactions",
    f"{total_transactions:,}"
)

col2.metric(
    "Detected Anomalies",
    f"{total_anomalies:,}"
)

col3.metric(
    "Average Severity Score",
    f"{avg_risk_score:.2f}"
)

# =====================================================
# ANOMALY DISTRIBUTION
# =====================================================

anomaly_counts = (
    anomalies_df["anomaly_type"]
    .value_counts()
    .reset_index()
)

anomaly_counts.columns = [
    "anomaly_type",
    "count"
]

fig1 = px.pie(
    anomaly_counts,
    names="anomaly_type",
    values="count",
    title="Anomaly Distribution"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================================
# TOP RISK ENTITIES
# =====================================================

risk_query = """
    SELECT
        t.source_entity,
        COUNT(*) AS anomaly_count
    FROM anomaly_flags af
    JOIN transactions t
    ON af.transaction_id = t.transaction_id
    GROUP BY t.source_entity
    ORDER BY anomaly_count DESC
    LIMIT 10;
"""

risk_df = pd.read_sql(
    risk_query,
    engine
)

fig2 = px.bar(
    risk_df,
    x="source_entity",
    y="anomaly_count",
    title="Top Risky Entities"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================================
# SEVERITY FILTER
# =====================================================

st.sidebar.header(
    "Investigation Filters"
)

selected_severity = (
    st.sidebar.slider(
        "Minimum Severity",
        0,
        100,
        50
    )
)

filtered_df = anomalies_df[
    anomalies_df["severity_score"]
    >= selected_severity
]

# =====================================================
# ANOMALY TABLE
# =====================================================

st.subheader(
    "Anomaly Investigation Console"
)

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =====================================================
# AI REPORTS
# =====================================================

try:

    ai_reports_df = pd.read_sql(
        """
        SELECT *
        FROM ai_audit_reports
        ORDER BY created_at DESC
        LIMIT 10;
        """,
        engine
    )

    st.subheader(
        "AI-Generated Audit Findings"
    )

    for _, row in ai_reports_df.iterrows():

        with st.expander(
            f"{row['anomaly_type']} — "
            f"{row['transaction_id']}"
        ):

            st.write(
                row["generated_report"]
            )

except Exception:

    st.warning(
        "AI reports not generated yet."
    )