import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import pandas as pd
import plotly.express as px
import streamlit as st

from sqlalchemy import text

from app.database.db import get_engine

from app.analytics.workflow_manager import (
    update_anomaly_status
)

engine = get_engine()

st.set_page_config(
    page_title="ThemisFin AI Dashboard",
    layout="wide"
)

st.title(
    "ThemisFin AI — Enterprise Audit Platform"
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

avg_severity = (
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
    "Average Severity",
    f"{avg_severity:.2f}"
)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header(
    "Investigation Filters"
)

selected_types = (
    st.sidebar.multiselect(
        "Anomaly Types",
        anomalies_df["anomaly_type"]
        .unique(),
        default=list(
            anomalies_df["anomaly_type"]
            .unique()
        )
    )
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
    (
        anomalies_df["anomaly_type"]
        .isin(selected_types)
    )
    &
    (
        anomalies_df["severity_score"]
        >= selected_severity
    )
]

# =====================================================
# ANOMALY DISTRIBUTION
# =====================================================

st.subheader(
    "Anomaly Distribution"
)

anomaly_counts = (
    filtered_df["anomaly_type"]
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
    values="count"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================================
# ENTITY RISK HEATMAP
# =====================================================

st.subheader(
    "Entity Risk Summary"
)

entity_risk_df = pd.read_sql(
    """
    SELECT *
    FROM entity_risk_summary
    ORDER BY anomaly_count DESC
    LIMIT 20;
    """,
    engine
)

fig2 = px.density_heatmap(
    entity_risk_df,
    x="source_entity",
    y="avg_severity",
    z="anomaly_count"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================================
# INVESTIGATION CONSOLE
# =====================================================

st.subheader(
    "Investigation Console"
)

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =====================================================
# WORKFLOW MANAGEMENT
# =====================================================

st.subheader(
    "Workflow Management"
)

anomaly_ids = (
    filtered_df["anomaly_id"]
    .tolist()
)

selected_anomaly = st.selectbox(
    "Select Anomaly ID",
    anomaly_ids
)

reviewer = st.text_input(
    "Reviewer Name"
)

new_status = st.selectbox(
    "Update Status",
    [
        "Open",
        "Under Review",
        "Escalated",
        "Resolved",
        "False Positive"
    ]
)

notes = st.text_area(
    "Investigation Notes"
)

if st.button("Update Workflow"):

    update_anomaly_status(
        selected_anomaly,
        new_status,
        reviewer,
        notes
    )

    st.success(
        "Workflow updated successfully."
    )

# =====================================================
# AI AUDIT REPORTS
# =====================================================

st.subheader(
    "AI Audit Findings"
)

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

    for _, row in ai_reports_df.iterrows():

        with st.expander(
            f"{row['anomaly_type']} "
            f"- {row['transaction_id']}"
        ):

            st.write(
                row["generated_report"]
            )

except Exception:

    st.warning(
        "AI reports unavailable."
    )

# =====================================================
# AUDIT LOGS
# =====================================================

st.subheader(
    "Audit Logs"
)

try:

    logs_df = pd.read_sql(
        """
        SELECT *
        FROM audit_logs
        ORDER BY action_timestamp DESC
        LIMIT 20;
        """,
        engine
    )

    st.dataframe(
        logs_df,
        use_container_width=True
    )

except Exception:

    st.warning(
        "Audit logs unavailable."
    )