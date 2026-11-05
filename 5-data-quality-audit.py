import pandas as pd
from tkinter import Tk, filedialog

# =====================================
# 1. SELECT DATASET
# =====================================

root = Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select Online Retail Dataset",
    filetypes=[("Excel Files", "*.xlsx")]
)

if file_path:

    df = pd.read_excel(file_path)

    print("\n===== DATA QUALITY AUDIT =====")

    # =====================================
    # 2. DATASET OVERVIEW
    # =====================================

    print("\n1. DATASET OVERVIEW")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    # =====================================
    # 3. MISSING VALUES
    # =====================================

    print("\n2. MISSING VALUES")
    print(df.isnull().sum())
    print("Total missing cells:", df.isnull().sum().sum())

    # =====================================
    # 4. DUPLICATE RECORDS
    # =====================================

    print("\n3. DUPLICATE RECORDS")

    print("Extra duplicate rows:", df.duplicated().sum())

    print(
        "All rows in duplicate groups:",
        df.duplicated(keep=False).sum()
    )

    # =====================================
    # 5. DATA TYPES
    # =====================================

    print("\n4. DATA TYPES")
    print(df.dtypes)

    # =====================================
    # 6. QUANTITY INVESTIGATION
    # =====================================

    print("\n5. QUANTITY CHECK")
    print("Zero quantities:", (df["Quantity"] == 0).sum())
    print("Negative quantities:", (df["Quantity"] < 0).sum())

    # =====================================
    # 7. PRICE INVESTIGATION
    # =====================================

    print("\n6. PRICE CHECK")
    print("Zero prices:", (df["UnitPrice"] == 0).sum())
    print("Negative prices:", (df["UnitPrice"] < 0).sum())

    # =====================================
    # 8. DATE INVESTIGATION
    # =====================================

    print("\n7. DATE CHECK")
    print("Earliest date:", df["InvoiceDate"].min())
    print("Latest date:", df["InvoiceDate"].max())
    print("Missing dates:", df["InvoiceDate"].isnull().sum())

    # =====================================
    # 9. DUPLICATE INVESTIGATION
    # =====================================

    print("\n8. DUPLICATE INVESTIGATION")

    duplicates = df[df.duplicated()]

    print("\nFirst 15 duplicate records:")

    if not duplicates.empty:
        print(duplicates.head(15).to_string(index=False))
    else:
        print("No duplicate records found.")

    print("\nTop 10 invoices containing duplicate rows:")

    print(
        duplicates["InvoiceNo"].value_counts().head(10)
    )

    print("\n===== AUDIT COMPLETED =====")

else:
    print("No file selected.")

root.destroy()