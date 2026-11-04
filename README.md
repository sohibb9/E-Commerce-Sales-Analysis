# E-Commerce Sales Analysis

**Python · Pandas · Matplotlib · Seaborn**

An exploratory analysis of real online retail transactions to understand sales performance, top markets and products, monthly trends, and customer purchasing behavior.

**Dataset:** [Kaggle — E-Commerce Data (Online Retail)](https://www.kaggle.com/datasets/carrie1/ecommerce-data)  
**Period:** December 2010–December 2011 (December 2011 is incomplete)

## Project objectives

- Clean and validate transactional data for a consistent sales-only analysis.
- Measure revenue, order volume, customer count and average order value.
- Identify leading countries, stock codes, and customers.
- Visualize monthly revenue and order trends.
- Communicate assumptions and limitations clearly.

## Key performance indicators

| Metric | Result |
| --- | ---: |
| Total sales revenue | **£10,642,110.80** |
| Distinct orders (invoices) | **19,960** |
| Identified customers | **4,338** |
| Unique stock codes (including non-product codes) | **3,922** |
| Average order value (AOV) | **£533.17** |

These metrics were calculated for the **filtered, deduplicated sales-only dataset** (not net profit).

## Selected findings

- **United Kingdom** is the largest revenue market; the country comparison makes this concentration visible.
- The top stock codes vary depending on whether products are ranked by **units sold** or **sales revenue**.
- Revenue and order volume vary across months. **December 2011 is incomplete**, so its total should not be treated as a full-month decline.
- Customer analysis separately distinguishes **high-spending customers** from **frequent buyers**.

## Methodology

1. Inspect the raw dataset's schema, missing values and exact duplicates.
2. For sales-only reporting, exclude invoice numbers beginning with `C`, non-positive quantities and non-positive unit prices.
3. Derive `TotalPrice = Quantity × UnitPrice` and extract year and month from invoice dates.
4. Create a deduplicated analysis copy. Keep missing `CustomerID` values in overall sales analysis, but exclude them from customer-level analysis.
5. Exclude `DOT`, `POST` and `M` from **product rankings only**, because they represent postage/manual entries. Other non-product stock codes may remain.
6. Recalculate KPIs and generate country, product, monthly and customer visualizations from the final analysis copies.

### Data quality and limitations

- **Duplicate assumption:** 5,226 exact duplicate copies were excluded. Their recorded value was **£24,573.74** (approximately **0.23%** of pre-deduplication sales-only revenue). Identical transaction rows are *not necessarily incorrect*; this is a documented analytical choice.
- **Unknown customers:** 132,186 rows in the final dataset have missing `CustomerID`; these remain part of aggregate sales metrics but not identified-customer analyses.
- **Partial period:** December 2011 is only partially covered.
- **Revenue is not profit:** The dataset does not include cost information needed to calculate net profit.
- **Stock codes are not all products:** The unique stock-code count may contain service or special transaction codes.

## Visualizations

After running the notebook, charts are saved in the `figures/` folder:

| Chart | File |
| --- | --- |
| Top countries by revenue | `figures/top_countries_revenue.png` |
| Top stock codes by revenue | `figures/top_products_revenue.png` |
| Monthly revenue trend | `figures/monthly_revenue_trend.png` |
| Monthly order volume | `figures/monthly_order_volume.png` |
| Top customers by spending | `figures/top_customers_spending.png` |
| Top customers by purchase frequency | `figures/top_customers_frequency.png` |

## How to run

1. Download `data.csv` from the [Kaggle dataset](https://www.kaggle.com/datasets/carrie1/ecommerce-data). Place it next to the notebook, or change `possible_paths` in the data-loading cell.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Open `ecommerce_sales_analysis_final.ipynb` in VS Code or Jupyter Notebook.
4. Run **Restart & Run All**. The notebook calculates KPIs, runs quality checks, and saves six PNG charts in `figures/`.

The raw CSV file is **not included** in this repository; download it from Kaggle.

## Project files

```text
E-Commerce-Sales-Analysis/
├── ecommerce_sales_analysis_final.ipynb
├── README.md
├── requirements.txt
└── figures/                   # created/populated when notebook runs
```

## Conclusion

The project demonstrates an end-to-end exploratory sales analysis workflow: validating real transaction data, applying transparent cleaning decisions, calculating business KPIs and visualizing actionable sales patterns. Findings are descriptive and subject to the documented data-quality limitations.
