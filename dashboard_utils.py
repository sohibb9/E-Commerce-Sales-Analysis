"""Data validation and aggregations for the E-Commerce Streamlit dashboard.

All monetary values are sales revenue in GBP, not profit. The dataset is
sales-only and uses the duplicate-removal assumptions documented in README.
"""

from pathlib import Path

import pandas as pd

SPECIAL_CODES = {"DOT", "POST", "M"}
REQUIRED_COLUMNS = {
    "InvoiceNo", "InvoiceDate", "Country", "CustomerID", "StockCode",
    "Description", "Quantity", "UnitPrice", "TotalPrice"
}


def load_sales_data(path: str | Path) -> pd.DataFrame:
    """Load the compressed public-dashboard extract with identifier-safe types."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Dashboard dataset not found: {path}")

    df = pd.read_csv(
        path,
        compression="gzip",
        parse_dates=["InvoiceDate"],
        dtype={"InvoiceNo": "string", "CustomerID": "string", "StockCode": "string"},
        low_memory=False,
    )
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing dashboard columns: {', '.join(sorted(missing))}")

    df["TotalPrice"] = pd.to_numeric(df["TotalPrice"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    if df[["InvoiceDate", "InvoiceNo", "TotalPrice", "Quantity", "UnitPrice"]].isna().any().any():
        raise ValueError("Dataset has invalid dates, sales values, or missing invoice IDs.")
    if (df["Quantity"] <= 0).any() or (df["UnitPrice"] <= 0).any():
        raise ValueError("The dashboard expects positive-quantity, positive-price sales.")
    if df.empty:
        raise ValueError("Dataset contains no sales.")
    return df


def filter_sales(df: pd.DataFrame, countries: list[str], start_date, end_date) -> pd.DataFrame:
    """Inclusive date filters, no country restriction when list is empty."""
    if start_date > end_date:
        return df.iloc[:0].copy()
    start = pd.Timestamp(start_date)
    end_exclusive = pd.Timestamp(end_date) + pd.Timedelta(days=1)
    mask = df["InvoiceDate"].ge(start) & df["InvoiceDate"].lt(end_exclusive)
    if countries:
        mask &= df["Country"].isin(countries)
    return df.loc[mask].copy()


def kpis(df: pd.DataFrame) -> dict:
    revenue = float(df["TotalPrice"].sum())
    orders = int(df["InvoiceNo"].nunique())
    customers = int(df["CustomerID"].nunique())  # excludes missing IDs
    return {"revenue": revenue, "orders": orders, "customers": customers,
            "aov": revenue / orders if orders else 0.0}


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (df.assign(Month=df["InvoiceDate"].dt.to_period("M").astype(str))
              .groupby("Month", as_index=False)["TotalPrice"].sum()
              .sort_values("Month"))


def country_revenue(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (df.groupby("Country", as_index=False)["TotalPrice"]
              .sum().nlargest(n, "TotalPrice"))


def product_revenue(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    items = df.loc[
        ~df["StockCode"].isin(SPECIAL_CODES) & df["Description"].notna()
    ]
    result = (items.groupby("Description", as_index=False)["TotalPrice"]
                   .sum().nlargest(n, "TotalPrice"))
    return result.rename(columns={"Description": "Product", "TotalPrice": "Revenue"})
