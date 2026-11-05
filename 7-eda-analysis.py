# ============================================================
# RETAIL SALES INTELLIGENCE & BUSINESS ANALYSIS
# STAGE 5: EXPLORATORY DATA ANALYSIS (EDA)
# Business Questions 1-17
# ============================================================

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. FILE PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Online_Retail_Cleaned.xlsx"
)

REPORT_DIR = PROJECT_DIR / "reports" / "eda_analysis"
CHART_DIR = REPORT_DIR / "charts"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("RETAIL SALES INTELLIGENCE - EDA ANALYSIS")
print("=" * 60)


# ============================================================
# 2. LOAD DATA
# ============================================================

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Cleaned dataset not found: {DATA_FILE}"
    )

df = pd.read_excel(
    DATA_FILE,
    sheet_name="Cleaned_Data"
)

required_columns = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

df = df[required_columns].copy()

df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()
df["StockCode"] = df["StockCode"].astype("string").str.strip()
df["Description"] = df["Description"].astype("string").str.strip()
df["Country"] = df["Country"].astype("string").str.strip()

df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

df["IsCancelled"] = (
    df["InvoiceNo"].str.upper().str.startswith("C", na=False)
)

df["LineValue"] = df["Quantity"] * df["UnitPrice"]


# ============================================================
# 3. DATASET UNDERSTANDING - Q1 TO Q3
# ============================================================

total_rows = len(df)
total_columns = len(df.columns)

column_types = df.dtypes.astype(str)

unique_invoices = df["InvoiceNo"].nunique()
unique_products = df["StockCode"].nunique()
unique_customers = df["CustomerID"].nunique()
unique_countries = df["Country"].nunique()

first_date = df["InvoiceDate"].min()
last_date = df["InvoiceDate"].max()


# ============================================================
# 4. DATA QUALITY - Q4 TO Q8
# ============================================================

missing_values = df.isna().sum()

duplicate_rows = int(df.duplicated().sum())

zero_quantity = int((df["Quantity"] == 0).sum())
negative_quantity = int((df["Quantity"] < 0).sum())

zero_price = int((df["UnitPrice"] == 0).sum())
negative_price = int((df["UnitPrice"] < 0).sum())

cancelled_rows = int(df["IsCancelled"].sum())

cancelled_invoices = int(
    df.loc[df["IsCancelled"], "InvoiceNo"].nunique()
)

return_mask = (
    (df["Quantity"] < 0)
    & (~df["IsCancelled"])
)

return_rows = int(return_mask.sum())

return_invoices = int(
    df.loc[return_mask, "InvoiceNo"].nunique()
)

quality_summary = pd.DataFrame({
    "Check": [
        "Missing Description",
        "Missing CustomerID",
        "Duplicate Rows",
        "Zero Quantity",
        "Negative Quantity",
        "Zero UnitPrice",
        "Negative UnitPrice",
        "Cancelled Transaction Rows",
        "Unique Cancelled Invoices",
        "Negative Quantity on Non-Cancelled Invoices"
    ],
    "Count": [
        int(df["Description"].isna().sum()),
        int(df["CustomerID"].isna().sum()),
        duplicate_rows,
        zero_quantity,
        negative_quantity,
        zero_price,
        negative_price,
        cancelled_rows,
        cancelled_invoices,
        return_rows
    ]
})


# ============================================================
# 5. SALES DATA PREPARATION
# ============================================================

sales_mask = (
    (~df["IsCancelled"])
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
    & (df["InvoiceDate"].notna())
)

sales = df.loc[sales_mask].copy()

if sales.empty:
    raise ValueError("No valid sales transactions found.")

sales["SalesValue"] = (
    sales["Quantity"] * sales["UnitPrice"]
)

sales["Month"] = (
    sales["InvoiceDate"].dt.to_period("M").astype(str)
)


# ============================================================
# 6. SALES ANALYSIS - Q9 TO Q12
# ============================================================

total_sales = float(sales["SalesValue"].sum())

total_sales_invoices = int(
    sales["InvoiceNo"].nunique()
)

identifiable_sales_customers = int(
    sales["CustomerID"].nunique()
)

average_order_value = (
    total_sales / total_sales_invoices
    if total_sales_invoices > 0
    else 0
)

monthly_sales = (
    sales.groupby("Month", as_index=False)
    .agg(
        Total_Sales=("SalesValue", "sum"),
        Total_Orders=("InvoiceNo", "nunique"),
        Units_Sold=("Quantity", "sum")
    )
    .sort_values("Month")
)


# ============================================================
# 7. PRODUCT ANALYSIS - Q13 AND Q14
# ============================================================

product_sales = (
    sales.groupby(
        ["StockCode", "Description"],
        dropna=False,
        as_index=False
    )
    .agg(
        Total_Sales=("SalesValue", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Total_Orders=("InvoiceNo", "nunique")
    )
)

top_products_by_sales = (
    product_sales
    .sort_values("Total_Sales", ascending=False)
    .head(10)
)

top_products_by_quantity = (
    product_sales
    .sort_values("Total_Quantity", ascending=False)
    .head(10)
)


# ============================================================
# 8. COUNTRY ANALYSIS - Q15
# ============================================================

country_sales = (
    sales.groupby("Country", as_index=False)
    .agg(
        Total_Sales=("SalesValue", "sum"),
        Total_Orders=("InvoiceNo", "nunique"),
        Total_Quantity=("Quantity", "sum"),
        Unique_Customers=("CustomerID", "nunique")
    )
    .sort_values("Total_Sales", ascending=False)
)


# ============================================================
# 9. CUSTOMER ANALYSIS - Q16 AND Q17
# ============================================================

identified_sales = sales.loc[
    sales["CustomerID"].notna()
].copy()

customer_frequency = (
    identified_sales
    .groupby("CustomerID", as_index=False)
    .agg(
        Purchase_Frequency=("InvoiceNo", "nunique"),
        Total_Sales=("SalesValue", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
)

customer_frequency["Customer_Type"] = np.where(
    customer_frequency["Purchase_Frequency"] > 1,
    "Repeat Customer",
    "One-time Customer"
)

repeat_customers = customer_frequency.loc[
    customer_frequency["Purchase_Frequency"] > 1
].copy()

one_time_customers = customer_frequency.loc[
    customer_frequency["Purchase_Frequency"] == 1
].copy()

top_customers = (
    customer_frequency
    .sort_values("Total_Sales", ascending=False)
    .head(10)
)

repeat_customer_count = len(repeat_customers)
one_time_customer_count = len(one_time_customers)

repeat_customer_rate = (
    repeat_customer_count / len(customer_frequency) * 100
    if len(customer_frequency) > 0
    else 0
)


# ============================================================
# 10. SAVE ANALYSIS TABLES
# ============================================================

missing_values.rename("Missing_Count").to_csv(
    REPORT_DIR / "missing_values.csv",
    header=True
)

quality_summary.to_csv(
    REPORT_DIR / "data_quality_summary.csv",
    index=False
)

monthly_sales.to_csv(
    REPORT_DIR / "monthly_sales_trend.csv",
    index=False
)

top_products_by_sales.to_csv(
    REPORT_DIR / "top_products_by_sales.csv",
    index=False
)

top_products_by_quantity.to_csv(
    REPORT_DIR / "top_products_by_quantity.csv",
    index=False
)

country_sales.to_csv(
    REPORT_DIR / "country_sales.csv",
    index=False
)

customer_frequency.to_csv(
    REPORT_DIR / "customer_purchase_frequency.csv",
    index=False
)

top_customers.to_csv(
    REPORT_DIR / "top_10_customers.csv",
    index=False
)


# ============================================================
# 11. CREATE CHARTS
# ============================================================

# Monthly sales trend

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["Month"],
    monthly_sales["Total_Sales"],
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales Value")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "monthly_sales_trend.png",
    dpi=150
)

plt.close()


# Top products by sales

chart_products = (
    top_products_by_sales
    .sort_values("Total_Sales")
)

plt.figure(figsize=(12, 7))

plt.barh(
    chart_products["Description"].fillna("Unknown").astype(str),
    chart_products["Total_Sales"]
)

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales Value")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_products_by_sales.png",
    dpi=150
)

plt.close()


# Top countries by sales

chart_countries = (
    country_sales.head(10)
    .sort_values("Total_Sales")
)

plt.figure(figsize=(10, 6))

plt.barh(
    chart_countries["Country"].astype(str),
    chart_countries["Total_Sales"]
)

plt.title("Top 10 Countries by Sales")
plt.xlabel("Sales Value")
plt.ylabel("Country")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_countries_by_sales.png",
    dpi=150
)

plt.close()


# ============================================================
# 12. GENERATE BUSINESS QUESTIONS REPORT
# ============================================================

def money(value):
    return f"{value:,.2f}"


report = []

report.append("# Retail Sales Intelligence & Business Analysis")
report.append("## Stage 5: Exploratory Data Analysis")
report.append("")

report.append("## A. Dataset Understanding")

report.append(
    f"Q1. Dataset size: {total_rows:,} rows and "
    f"{total_columns} columns."
)

report.append("")
report.append("Q2. Column names and data types:")

for column in required_columns:
    report.append(
        f"- {column}: {column_types[column]}"
    )

report.append("")

report.append(
    f"Q3. Date range: {first_date} to {last_date}. "
    f"Countries: {unique_countries:,}. "
    f"Products: {unique_products:,}. "
    f"Identifiable customers: {unique_customers:,}. "
    f"Invoices: {unique_invoices:,}."
)

report.append("")
report.append("## B. Data Quality")

report.append("Q4. Missing values:")

for column, count in missing_values.items():
    report.append(f"- {column}: {int(count):,}")

report.append("")

report.append(
    f"Q5. Duplicate rows remaining: {duplicate_rows:,}."
)

report.append("")

report.append(
    f"Q6. Zero quantities: {zero_quantity:,}; "
    f"negative quantities: {negative_quantity:,}; "
    f"zero prices: {zero_price:,}; "
    f"negative prices: {negative_price:,}."
)

report.append("")

report.append(
    f"Q7. Cancelled transaction rows: {cancelled_rows:,}; "
    f"cancelled invoices: {cancelled_invoices:,}; "
    f"negative-quantity rows on non-cancelled invoices: "
    f"{return_rows:,}; related invoices: {return_invoices:,}."
)

report.append("")

report.append(
    "Q8. Cleaning decisions: Exact duplicates and text/type "
    "standardization were handled during Stage 4. Missing customer "
    "IDs were preserved because customer identities cannot be "
    "reliably inferred. Unusual quantities, prices, returns, and "
    "cancellations were preserved for investigation. Sales analysis "
    "uses non-cancelled transactions with positive quantities, "
    "positive prices, and valid dates."
)

report.append("")
report.append("## C. Sales Analysis")

report.append(
    "Q9. Sales value is calculated as Quantity multiplied by UnitPrice."
)

report.append("")

report.append(
    f"Q10. Valid sales invoices: {total_sales_invoices:,}. "
    f"Identifiable sales customers: "
    f"{identifiable_sales_customers:,}."
)

report.append("")

report.append(
    f"Q11. Average Order Value: {money(average_order_value)}. "
    f"Total sales: {money(total_sales)}."
)

report.append("")

report.append(
    "Q12. Monthly sales results are available in "
    "monthly_sales_trend.csv and charts/monthly_sales_trend.png."
)

report.append("")
report.append("## D. Product and Country Analysis")

report.append(
    "Q13. Top products by sales are available in "
    "top_products_by_sales.csv."
)

report.append("")

report.append(
    "Q14. Top products by quantity are available in "
    "top_products_by_quantity.csv."
)

report.append("")

report.append(
    "Q15. Country sales results are available in country_sales.csv."
)

report.append("")
report.append("## E. Customer Analysis")

report.append(
    f"Q16. Identifiable customers: {len(customer_frequency):,}. "
    f"Repeat customers: {repeat_customer_count:,}. "
    f"One-time customers: {one_time_customer_count:,}. "
    f"Repeat customer rate: {repeat_customer_rate:.2f}%."
)

report.append("")

report.append(
    "Q17. Top customers by sales are available in "
    "top_10_customers.csv."
)

report.append("")
report.append("## Methodology and Limitations")

report.append(
    "Customer analysis excludes transactions without CustomerID. "
    "Sales value is a revenue proxy, not profit. The dataset does "
    "not provide profit margins, delivery times, marketing activity, "
    "or customer demographics. Questions 18-21 will be addressed "
    "in the later SQL, Power BI, and business recommendation stages."
)

report_path = (
    REPORT_DIR / "EDA_Business_Questions_Answers.md"
)

report_path.write_text(
    "\n".join(report),
    encoding="utf-8"
)


# ============================================================
# 13. FINAL RESULTS
# ============================================================

print("\nEDA ANALYSIS COMPLETED")

print("-" * 60)

print("Total rows:", f"{total_rows:,}")
print("Total columns:", total_columns)
print("Valid sales transactions:", f"{len(sales):,}")
print("Sales invoices:", f"{total_sales_invoices:,}")
print("Identifiable sales customers:", f"{identifiable_sales_customers:,}")

print("Total Sales:", money(total_sales))
print("Average Order Value:", money(average_order_value))

print("Repeat Customers:", f"{repeat_customer_count:,}")
print("Repeat Customer Rate:", f"{repeat_customer_rate:.2f}%")

print("\nTop 5 Countries by Sales:")

print(
    country_sales[
        ["Country", "Total_Sales"]
    ].head(5).to_string(index=False)
)

print("\nTop 5 Products by Sales:")

print(
    top_products_by_sales[
        ["StockCode", "Description", "Total_Sales"]
    ].head(5).to_string(index=False)
)

print("\nReports and charts saved in:")

print(REPORT_DIR)

print("\nNext stage: SQL verification.")

print("=" * 60)