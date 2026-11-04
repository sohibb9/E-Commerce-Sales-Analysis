"""Interactive portfolio dashboard for the cleaned Online Retail transactions.

Run from repository root: python -m streamlit run app.py
"""

from html import escape
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from dashboard_utils import (
    country_revenue,
    filter_sales,
    kpis,
    load_sales_data,
    monthly_revenue,
    product_revenue,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sales_dashboard.csv.gz"
CHART_HEIGHT = 345
ACCENT = "#10b981"

st.set_page_config(
    page_title="E-Commerce | Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container { max-width: 1450px; padding-top: 1.6rem; padding-bottom: 2rem; }
.product-rank-table { width: 100%; border-collapse: collapse; font-size: .85rem; table-layout: fixed; }
.product-rank-table th { color: #94a3b8; font-size: .78rem; font-weight: 650;
    border-bottom: 1px solid rgba(148,163,184,.35); padding: 10px 8px; text-align: left; }
.product-rank-table td { border-bottom: 1px solid rgba(148,163,184,.16);
    padding: 10px 8px; height: 39px; vertical-align: middle; }
.product-rank-table .product-name { overflow: hidden; text-overflow: ellipsis;
    white-space: nowrap; display: block; max-width: 100%; }
.product-rank-table td:last-child, .product-rank-table th:last-child { text-align: right; white-space: nowrap; }
.product-rank-table th:first-child { width: 65%; }
.product-rank-table th:last-child { width: 35%; }
</style>
""", unsafe_allow_html=True)

st.title("📊 E-Commerce Analytics Dashboard")
st.caption("ONLINE RETAIL · Dec 2010–Dec 2011 · GBP · Sales-only (not profit)")
st.write("Explore revenue, orders, customers, markets and products with interactive filters.")


@st.cache_data(show_spinner="Loading transaction data…")
def get_data() -> pd.DataFrame:
    return load_sales_data(DATA_FILE)


try:
    full_df = get_data()
except (FileNotFoundError, ValueError, OSError, pd.errors.ParserError) as exc:
    st.error(f"Unable to load dashboard dataset: {exc}")
    st.info("This app needs sales_dashboard.csv.gz beside app.py. See README.md for setup.")
    st.stop()

st.sidebar.header("🔎 Filters")
st.sidebar.caption("Leave the country filter empty to include all countries.")
selected_countries = st.sidebar.multiselect(
    "Countries", sorted(full_df["Country"].dropna().unique().tolist()),
    placeholder="All countries",
)
minimum = full_df["InvoiceDate"].min().date()
maximum = full_df["InvoiceDate"].max().date()
date_range = st.sidebar.date_input(
    "Date range", value=(minimum, maximum), min_value=minimum, max_value=maximum,
)
if len(date_range) != 2:
    st.info("Select both a start date and an end date to see the dashboard.")
    st.stop()

start_date, end_date = date_range
sales = filter_sales(full_df, selected_countries, start_date, end_date)
if sales.empty:
    st.warning("No transactions match the selected filters. Try a wider date range or other countries.")
    st.stop()

metrics = kpis(sales)

st.subheader("Sales overview")
a, b, c, d = st.columns(4, gap="medium")
a.metric("Revenue", f"£{metrics['revenue']:,.2f}")
b.metric("Orders", f"{metrics['orders']:,}")
c.metric("Known customers", f"{metrics['customers']:,}")
d.metric("Average order value", f"£{metrics['aov']:,.2f}")
st.caption("AOV = revenue ÷ distinct orders. Known customers excludes transactions with a missing customer ID.")

st.divider()
st.subheader("Sales performance")
left, right = st.columns(2, gap="large")

monthly = monthly_revenue(sales)
monthly_chart = (
    alt.Chart(monthly)
    .mark_line(point=alt.OverlayMarkDef(size=68), strokeWidth=3, color=ACCENT)
    .encode(
        x=alt.X("Month:N", sort=None, title="Month", axis=alt.Axis(labelAngle=-40)),
        y=alt.Y("TotalPrice:Q", title="Revenue (£)", axis=alt.Axis(format="~s")),
        tooltip=[alt.Tooltip("Month:N", title="Month"),
                 alt.Tooltip("TotalPrice:Q", title="Revenue (£)", format=",.2f")],
    )
    .properties(height=CHART_HEIGHT)
)

countries = country_revenue(sales)
country_chart = (
    alt.Chart(countries)
    .mark_bar(color=ACCENT, cornerRadiusEnd=3)
    .encode(
        y=alt.Y("Country:N", sort="-x", title=None,
                axis=alt.Axis(labelLimit=150)),
        x=alt.X("TotalPrice:Q", title="Revenue (£)", axis=alt.Axis(format="~s")),
        tooltip=[alt.Tooltip("Country:N", title="Country"),
                 alt.Tooltip("TotalPrice:Q", title="Revenue (£)", format=",.2f")],
    )
    .properties(height=CHART_HEIGHT)
)

with left:
    with st.container(border=True):
        st.markdown("**Monthly revenue trend**")
        st.altair_chart(monthly_chart, width="stretch")
with right:
    with st.container(border=True):
        st.markdown("**Top 10 countries by revenue**")
        st.altair_chart(country_chart, width="stretch")

st.caption("December 2011 is incomplete. Compare partial months with caution.")
st.divider()
st.subheader("Top 10 products by revenue")

products = product_revenue(sales)
rank_col, chart_col = st.columns([1.15, 1.85], gap="large")

with rank_col:
    with st.container(border=True):
        st.markdown("**Product rankings**")
        # A static, compact table means the mouse wheel scrolls the PAGE,
        # rather than scrolling or zooming a nested interactive grid.
        if products.empty:
            st.info("No product records for these filters.")
        else:
            rows = []
            for pos, row in enumerate(products.itertuples(index=False), start=1):
                full_name = str(row.Product)
                label = escape(full_name)
                revenue = float(row.Revenue)
                rows.append(
                    f'<tr><td><span class="product-name" title="{label}">'
                    f'{pos}. {label}</span></td><td>£{revenue:,.2f}</td></tr>'
                )
            table_html = (
                '<table class="product-rank-table"><thead><tr>'
                '<th>Product</th><th>Revenue</th></tr></thead><tbody>'
                + "".join(rows) + '</tbody></table>'
            )
            st.markdown(table_html, unsafe_allow_html=True)

with chart_col:
    with st.container(border=True):
        st.markdown("**Product revenue chart**")
        if products.empty:
            st.info("No product records for these filters.")
        else:
            product_chart = (
                alt.Chart(products)
                .mark_bar(color=ACCENT, cornerRadiusEnd=3)
                .encode(
                    y=alt.Y("Product:N", sort="-x", title=None,
                            axis=alt.Axis(labelLimit=185, labelFontSize=11)),
                    x=alt.X("Revenue:Q", title="Revenue (£)", axis=alt.Axis(format="~s")),
                    tooltip=[alt.Tooltip("Product:N", title="Product"),
                             alt.Tooltip("Revenue:Q", title="Revenue (£)", format=",.2f")],
                )
                .properties(height=395)
            )
            st.altair_chart(product_chart, width="stretch")

st.divider()
with st.expander("🔍 Dataset preview & methodology", expanded=False):
    st.write(f"**Filtered rows:** {len(sales):,}  |  **Columns:** {sales.shape[1]}")
    st.write("Transactions are filtered to positive-price, positive-quantity sales, with exact duplicate rows removed in the notebook. Special codes DOT, POST and M are excluded from product rankings only.")
    st.write("The shared extract replaces invoice and customer IDs with random pseudonyms, but is not guaranteed anonymous.")
    preview = sales.drop(columns=["CustomerID", "InvoiceNo"], errors="ignore")
    st.dataframe(preview.head(8), hide_index=True, width="stretch")

st.caption("Source: UCI Online Retail (CC BY 4.0) · Descriptive revenue analysis · Built with Pandas, Altair and Streamlit")
