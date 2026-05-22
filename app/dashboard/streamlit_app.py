import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

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

# =====================================================
# KPIs
# =====================================================

total_transactions = len(
    transactions_df
)

total_volume = (
    transactions_df["amount"].sum()
)

avg_transaction = (
    transactions_df["amount"].mean()
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Transactions",
    f"{total_transactions:,}"
)

col2.metric(
    "Total Transaction Volume",
    f"${total_volume:,.2f}"
)

col3.metric(
    "Average Transaction",
    f"${avg_transaction:,.2f}"
)

# =====================================================
# TRANSACTION CATEGORY DISTRIBUTION
# =====================================================

category_counts = (
    transactions_df["category"]
    .value_counts()
    .reset_index()
)

category_counts.columns = [
    "category",
    "count"
]

fig1 = px.pie(
    category_counts,
    names="category",
    values="count",
    title="Transaction Categories"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================================
# TOP ENTITIES
# =====================================================

entity_volume = (
    transactions_df.groupby(
        "source_entity"
    )["amount"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    entity_volume.sort_values(
        by="amount",
        ascending=False
    ).head(10),
    x="source_entity",
    y="amount",
    title="Top Entity Transaction Volume"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================================
# DAILY TRANSACTION TREND
# =====================================================

transactions_df["timestamp"] = (
    pd.to_datetime(
        transactions_df["timestamp"]
    )
)

daily_trend = (
    transactions_df.groupby(
        transactions_df["timestamp"].dt.date
    )["amount"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    daily_trend,
    x="timestamp",
    y="amount",
    title="Daily Transaction Trend"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =====================================================
# RAW DATA VIEW
# =====================================================

st.subheader("Transaction Investigation Console")

st.dataframe(
    transactions_df.head(1000),
    use_container_width=True
)