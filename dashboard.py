import json
from pathlib import Path

import pandas as pd
import streamlit as st

# Page Config
st.set_page_config(page_title="Invoice Dashboard", layout="wide")

st.title("Invoice System Dashboard")

# Data Loading
DATA_PATH = Path("data/invoices.json")


@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        return []

    with open(DATA_PATH) as f:
        data = json.load(f)

    # Convert dict of dicts to list of dicts
    invoices = list(data.values())
    return invoices


invoices = load_data()

if not invoices:
    st.warning("No data found.")
    st.stop()

# Process Data
df = pd.json_normalize(invoices)


# Calculate Totals
def calculate_total(items):
    total = 0.0
    for item in items:
        q = item.get("quantity", 0)
        p = float(item.get("unit_price", 0.0))
        total += q * p
    return total


df["total_amount"] = df["items"].apply(calculate_total)

# Sidebar filters
st.sidebar.header("Filters")
status_filter = st.sidebar.multiselect(
    "Status", options=df["status"].unique(), default=df["status"].unique()
)

filtered_df = df[df["status"].isin(status_filter)]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Invoices", len(filtered_df))
col2.metric(
    "Total Revenue (Draft+Sent)",
    f"${filtered_df[filtered_df['status'].isin(['draft', 'sent'])]['total_amount'].sum():,.2f}",
)
col3.metric("Average Invoice Value", f"${filtered_df['total_amount'].mean():,.2f}")

# Charts
st.subheader("Invoices by Status")
status_counts = filtered_df["status"].value_counts()
st.bar_chart(status_counts)

# Data Table
st.subheader("Recent Invoices")
st.dataframe(
    filtered_df[["id", "invoice_number", "customer_id", "status", "total_amount"]],
    use_container_width=True,
)

# Raw Data (Optional)
with st.expander("View Raw Data"):
    st.json(invoices)
