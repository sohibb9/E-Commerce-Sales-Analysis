# E-Commerce Sales Analysis & Interactive Dashboard

**Python · Pandas · Seaborn · Altair · Streamlit**

A portfolio project that cleans a real Online Retail transactional dataset, documents analytical assumptions, calculates business KPIs, and presents a filterable dashboard. The Jupyter notebook shows the analysis; the Streamlit app presents the results to nontechnical users.

**Sources:** [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online-retail) ([DOI: 10.24432/C5BW33](https://doi.org/10.24432/C5BW33)) · [Kaggle mirror](https://www.kaggle.com/datasets/carrie1/ecommerce-data)  
**Covered period:** December 2010–December 2011 (**December 2011 is incomplete**)  
**Dashboard:** Add your `https://<your-app>.streamlit.app` link here after deployment.

## KPI summary (all countries, full date range)

| Metric | Value |
| --- | ---: |
| Total sales revenue | **£10,642,110.80** |
| Distinct orders | **19,960** |
| Known customers | **4,338** |
| Unique stock codes (including service codes) | **3,922** |
| Average order value (AOV) | **£533.17** |
| Final sales rows after removing exact duplicates | **524,878** |

The KPIs are based on a **filtered, deduplicated, sales-only** scenario; they are *not* profits or all net transactions. Known customers exclude records without `CustomerID`. AOV is total sales revenue divided by distinct invoices, not the mean of line items.

## Dashboard features

- Country and inclusive date filters that update every KPI and chart.
- Revenue, distinct orders, known customers and AOV.
- Monthly revenue trend and top countries, with same-height chart panels.
- Product ranking table **on the left**, horizontal product chart **on the right**, with a static table to avoid mouse-wheel scrolling inside it.
- Collapsed dataset preview and explanation of filtering assumptions.

Charts are rendered with Altair **without scroll-wheel zoom**. This is intentionally a single-page dashboard.

## Cleaning decisions and limitations

1. Exclude cancellation invoice IDs beginning with `C`, nonpositive quantities and nonpositive prices.
2. Compute `TotalPrice = Quantity × UnitPrice` in GBP.
3. Remove 5,226 exact duplicate copies as a documented analytical assumption (not all identical lines are necessarily errors). This changes pre-deduplication sales-only revenue by **£24,573.74** (about **0.23%**).
4. Keep missing customer IDs in revenue/order KPIs; there are **132,186** such rows after deduplication. Exclude them only from distinct-customer analysis.
5. Exclude `DOT`, `POST` and `M` from **product rankings**, but retain them in total revenue. Other non-product codes may exist.
6. Treat December 2011 as a *partial month*. No costs are available to calculate profit.

**Highlights:** The UK is the leading revenue market. November 2011 is the highest-revenue complete month in the dataset. Product rankings by revenue and by quantity answer different questions. Customer-spending rankings differ from order-frequency rankings.

## Run the dashboard locally

Use Python 3.11+ and run commands from the repository directory. Windows CMD example:

```bat
cd /d "E:\05-Projects\Data Analysis\E-Commerce-Sales-Analysis"
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL shown by Streamlit (usually `http://localhost:8501`). The dashboard works with the **included** `sales_dashboard.csv.gz` file; you do not need raw `data.csv` just to view the app.

To test without opening a browser:

```bat
python tests\smoke_test.py
```

## Reproduce the Jupyter analysis and figures

1. Download the original `data.csv` from the [Kaggle mirror](https://www.kaggle.com/datasets/carrie1/ecommerce-data) (or UCI original, converting XLSX to CSV with the equivalent schema as needed).
2. Place `data.csv` in the **repository root** beside the notebook. The file is intentionally excluded from GitHub with `.gitignore`.
3. Open `ecommerce_sales_analysis_final.ipynb` in VS Code/Jupyter **with the repository as working directory** and run all cells.
4. The notebook reproduces revenue/customer/order calculations, saves six PNG figures to `figures/`, and at the end exports and verifies a new `sales_dashboard.csv.gz` extract. The export creates fresh random pseudonyms every time, so the binary file changes even when business KPIs do not.
5. Run `python tests/smoke_test.py` before publishing changes.

## Repository structure

```text
E-Commerce-Sales-Analysis/
├── app.py                            # Streamlit UI
├── dashboard_utils.py                # reusable calculations & data validation
├── sales_dashboard.csv.gz            # compressed, pseudonymized extract for the app
├── ecommerce_sales_analysis_final.ipynb
├── figures/                          # six saved analysis charts
├── tests/
│   └── smoke_test.py
├── README.md
├── requirements.txt
└── .gitignore
```

The original local-only `data.csv`, `sales_cleaned.csv`, `Backup/`, `.venv/` and `.git/` are **not distributed in the public-ready ZIP**. Never replace the `.git` folder of your existing repository.

## Deploy on Streamlit Community Cloud

1. Copy the updated files into your **existing** local Git repository (do not delete its `.git/` folder).
2. Verify `git status` does not include raw customer files or a local virtual environment. Then:

   ```bat
   git add app.py dashboard_utils.py ecommerce_sales_analysis_final.ipynb README.md requirements.txt .gitignore figures tests sales_dashboard.csv.gz
   git commit -m "Polish analysis and deploy-ready Streamlit dashboard"
   git push
   ```

3. Open [Streamlit Community Cloud](https://share.streamlit.io/), choose **Create app**, select your GitHub repository `sohibb9/E-Commerce-Sales-Analysis`, `main` branch and `app.py` as the entrypoint. Deploy and check that the four KPIs match the table above.
4. Add the deployed URL to the top of this README and to your portfolio. Deployment is **not automatic** until you connect your GitHub repository to Streamlit Cloud.

## Dataset attribution and privacy

Original dataset: **Chen, D. (2015), Online Retail, UCI Machine Learning Repository**, [DOI: 10.24432/C5BW33](https://doi.org/10.24432/C5BW33). UCI lists the dataset under **Creative Commons Attribution 4.0 (CC BY 4.0)**; credit is required when sharing derived data. The Kaggle mirror's license field is listed as unknown, so attribution here relies on the documented UCI origin. The dashboard extract was cleaned, deduplicated and transformed from the original; it replaces the original invoice and customer IDs with random pseudonyms, but **is not fully anonymized** (transaction details may still be linked to the public source). The compressed extract is shared only for the dashboard demonstration. Do not publish private client datasets in this manner.


## Dataset Attribution

Dataset: Online Retail
Creator: Daqing Chen (2015)
Source: UCI Machine Learning Repository
DOI: https://doi.org/10.24432/C5BW33
License: CC BY 4.0

The dashboard uses a cleaned, compressed version
with pseudonymized invoice and customer identifiers.