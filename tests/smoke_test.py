"""Run from the repository root: python tests/smoke_test.py"""
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from dashboard_utils import (  # noqa: E402
    country_revenue, filter_sales, kpis, load_sales_data, monthly_revenue,
    product_revenue,
)


def main():
    df = load_sales_data(BASE_DIR / "sales_dashboard.csv.gz")
    full = kpis(df)
    assert len(df) == 524_878, len(df)
    assert full["orders"] == 19_960, full
    assert full["customers"] == 4_338, full
    assert abs(full["revenue"] - 10_642_110.804) < 0.01, full
    assert abs(full["aov"] - 533.17) < 0.01, full
    assert df["InvoiceNo"].dropna().str.fullmatch(r"[0-9a-f]{32}").all()
    assert df["CustomerID"].dropna().str.fullmatch(r"[0-9a-f]{32}").all()

    subset = filter_sales(df, ["Germany"], df.InvoiceDate.min().date(), df.InvoiceDate.max().date())
    assert not subset.empty
    assert set(subset["Country"]) == {"Germany"}
    assert kpis(subset)["revenue"] < full["revenue"]

    months = monthly_revenue(df)
    assert abs(months["TotalPrice"].sum() - full["revenue"]) < 0.01
    assert len(country_revenue(df)) == 10
    products = product_revenue(df)
    assert len(products) == 10
    assert "REGENCY CAKESTAND 3 TIER" in products["Product"].values
    assert len(filter_sales(df, [], df.InvoiceDate.min().date(), df.InvoiceDate.max().date())) == len(df)
    assert filter_sales(df, [], df.InvoiceDate.max().date(), df.InvoiceDate.min().date()).empty
    print("PASS: dataset, privacy checks, KPIs, filters, charts and aggregations")
    print(f"Revenue £{full['revenue']:,.2f}; {full['orders']:,} orders; {full['customers']:,} customers")


if __name__ == "__main__":
    main()
