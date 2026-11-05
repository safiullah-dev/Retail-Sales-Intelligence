from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. SET PROJECT AND DATASET PATHS
# --------------------------------------------------

project_root = Path(__file__).resolve().parents[1]

input_file = (
    project_root
    / "data"
    / "raw"
    / "online+retail"
    / "Online Retail.xlsx"
)

output_folder = project_root / "data" / "processed"
output_file = output_folder / "Online_Retail_Cleaned.xlsx"

# --------------------------------------------------
# 2. CHECK WHETHER THE ORIGINAL DATASET EXISTS
# --------------------------------------------------

if not input_file.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {input_file}"
    )

print("Dataset found successfully!")
print(f"Reading: {input_file}")

# --------------------------------------------------
# 3. LOAD ORIGINAL DATA
# --------------------------------------------------

df = pd.read_excel(input_file)

original_rows = len(df)

print("\nOriginal Dataset Information")
print("----------------------------")
print(f"Original records: {original_rows}")
print(f"Original columns: {len(df.columns)}")

# --------------------------------------------------
# 4. CHECK REQUIRED COLUMNS
# --------------------------------------------------

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
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns missing: {missing_columns}"
    )

# --------------------------------------------------
# 5. REMOVE EXACT DUPLICATE RECORDS
# --------------------------------------------------

duplicates_removed = int(df.duplicated().sum())

df = df.drop_duplicates().copy()

print("\nDuplicate Removal")
print("-----------------")
print(f"Duplicates removed: {duplicates_removed}")
print(f"Records remaining: {len(df)}")

# --------------------------------------------------
# 6. CLEAN TEXT COLUMNS
# --------------------------------------------------

text_columns = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Country"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Convert empty text values into missing values
df[text_columns] = df[text_columns].replace(
    r"^\s*$",
    pd.NA,
    regex=True
)

# --------------------------------------------------
# 7. CORRECT DATA TYPES
# --------------------------------------------------

df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
).astype("Int64")

df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"], errors="coerce"
)

df["CustomerID"] = pd.to_numeric(
    df["CustomerID"], errors="coerce"
).astype("Int64")

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)

# --------------------------------------------------
# 8. RECOVER SOME MISSING PRODUCT DESCRIPTIONS
# --------------------------------------------------

missing_description_before = int(
    df["Description"].isna().sum()
)

valid_descriptions = df.dropna(
    subset=["StockCode", "Description"]
)

description_counts = (
    valid_descriptions
    .groupby("StockCode")["Description"]
    .nunique()
)

unique_stock_codes = description_counts[
    description_counts == 1
].index

description_lookup = (
    valid_descriptions[
        valid_descriptions["StockCode"].isin(unique_stock_codes)
    ]
    .drop_duplicates(subset=["StockCode"])
    .set_index("StockCode")["Description"]
)

df["Description"] = df["Description"].fillna(
    df["StockCode"].map(description_lookup)
)

missing_description_after = int(
    df["Description"].isna().sum()
)

descriptions_recovered = (
    missing_description_before - missing_description_after
)

# --------------------------------------------------
# 9. CHECK REMAINING DATA QUALITY ISSUES
# --------------------------------------------------

remaining_duplicates = int(df.duplicated().sum())

missing_values = df.isna().sum()

negative_quantity = int((df["Quantity"] < 0).sum())
zero_quantity = int((df["Quantity"] == 0).sum())

negative_prices = int((df["UnitPrice"] < 0).sum())
zero_prices = int((df["UnitPrice"] == 0).sum())

cancelled_records = int(
    df["InvoiceNo"].str.startswith(
        "C", na=False
    ).sum()
)

missing_customer_ids = int(
    df["CustomerID"].isna().sum()
)

# --------------------------------------------------
# 10. CREATE CLEANING SUMMARY
# --------------------------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Original records",
        "Duplicates removed",
        "Final records",
        "Remaining duplicates",
        "Missing descriptions before recovery",
        "Descriptions recovered",
        "Missing descriptions after recovery",
        "Missing CustomerID records",
        "Negative quantity records",
        "Zero quantity records",
        "Negative price records",
        "Zero price records",
        "Cancellation records"
    ],
    "Value": [
        original_rows,
        duplicates_removed,
        len(df),
        remaining_duplicates,
        missing_description_before,
        descriptions_recovered,
        missing_description_after,
        missing_customer_ids,
        negative_quantity,
        zero_quantity,
        negative_prices,
        zero_prices,
        cancelled_records
    ]
})

missing_summary = missing_values.reset_index()
missing_summary.columns = [
    "Column",
    "Missing Values"
]

# --------------------------------------------------
# 11. SAVE CLEANED DATASET
# --------------------------------------------------

output_folder.mkdir(parents=True, exist_ok=True)

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Cleaned_Data",
        index=False
    )

    summary.to_excel(
        writer,
        sheet_name="Cleaning_Summary",
        index=False
    )

    missing_summary.to_excel(
        writer,
        sheet_name="Missing_Values",
        index=False
    )

# --------------------------------------------------
# 12. DISPLAY FINAL RESULTS
# --------------------------------------------------

print("\nCLEANING COMPLETED")
print("==================")

print(f"Original records: {original_rows}")
print(f"Duplicates removed: {duplicates_removed}")
print(f"Final records: {len(df)}")
print(f"Remaining duplicates: {remaining_duplicates}")

print("\nMissing Values:")
print(missing_summary.to_string(index=False))

print("\nDescription Recovery:")
print(f"Descriptions recovered: {descriptions_recovered}")
print(f"Descriptions still missing: {missing_description_after}")

print("\nUnusual Records Preserved:")
print(f"Negative quantities: {negative_quantity}")
print(f"Zero quantities: {zero_quantity}")
print(f"Negative prices: {negative_prices}")
print(f"Zero prices: {zero_prices}")
print(f"Cancellation records: {cancelled_records}")

print("\nOutput saved successfully:")
print(output_file)