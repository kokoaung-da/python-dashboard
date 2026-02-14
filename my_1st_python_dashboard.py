import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG (ALWAYS FIRST)
# ==================================================
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    initial_sidebar_state= "expanded"
)

# ==================================================
# LOAD DATA (SIMULATED FACT TABLE)
# ==================================================
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Date": pd.date_range("2024-01-01", periods=30),
        "Category": ["Electronics", "Accessories"] * 15,
        "Product": ["Laptop", "Mouse", "Keyboard", "Monitor", "Mouse"] * 6,
        "Sales": [1200, 50, 80, 300, 60] * 6
    })

df = load_data()

# ==================================================
# SIDEBAR = POWER BI SLICERS
# ==================================================
with st.sidebar:
    st.header("🔍 Filters")

    category = st.multiselect(
        "Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    date_range = st.date_input(
        "Date Range",
        value=(df["Date"].min(), df["Date"].max())
    )

# Safe filtering
df_sel = df.copy()

if category:
    df_sel = df_sel[df_sel["Category"].isin(category)]

df_sel = df_sel[
    (df_sel["Date"] >= pd.to_datetime(date_range[0])) &
    (df_sel["Date"] <= pd.to_datetime(date_range[1]))
]

# ==================================================
# TITLE
# ==================================================
st.title("📊 Sales Performance Dashboard")
st.markdown("---")

# ==================================================
# KPI CALCULATIONS (MEASURES)
# ==================================================
total_sales = df_sel["Sales"].sum()
avg_sales = df_sel["Sales"].mean()
max_sales = df_sel["Sales"].max()
transactions = len(df_sel)

# ==================================================
# ROW 1 → PRIMARY KPIs
# ==================================================
with st.container():
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Total Sales", f"US $ {total_sales:,}")
    k2.metric("Average Sale", f"US $ {avg_sales:,.2f}")
    k3.metric("Max Sale", f"US $ {max_sales:,}")
    k4.metric("Transactions", transactions)

# ==================================================
# ROW 2 → VISUALS
# ==================================================
sales_by_category = (
    df_sel.groupby("Category", as_index=False)["Sales"].sum()
)

sales_by_product = (
    df_sel.groupby("Product", as_index=False)["Sales"].sum()
)

fig_category = px.pie(
    sales_by_category,
    values="Sales",
    names="Category",
    title="Sales by Category"
)

fig_product = px.bar(
    sales_by_product,
    x="Sales",
    y="Product",
    orientation="h",
    title="Sales by Product",
    template="plotly_white"
)

c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(fig_category, use_container_width=True)

with c2:
    st.plotly_chart(fig_product, use_container_width=True)

# ==================================================
# ROW 3 → TABLE (POWER BI STYLE)
# ==================================================
st.markdown("---")
st.subheader("📋 Sales Summary")

summary_table = (
    df_sel
    .groupby(["Category", "Product"], as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Avg_Sales=("Sales", "mean"),
        Transactions=("Sales", "count")
    )
)

st.dataframe(
    summary_table.style.format({
        "Total_Sales": "US $ {:,.0f}",
        "Avg_Sales": "US $ {:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ==================================================
# RAW DATA (OPTIONAL)
# ==================================================
with st.expander("📄 View Raw Data"):
    st.dataframe(df_sel, use_container_width=True, hide_index=True)