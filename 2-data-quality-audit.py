import pandas as pd
from tkinter import Tk, filedialog

# Select the original Excel dataset
root = Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select Online Retail Dataset",
    filetypes=[("Excel Files", "*.xlsx")]
)

if file_path:

    df = pd.read_excel(file_path)

    print("\n========== DATA QUALITY AUDIT ==========")

    print("\n1. DATASET SIZE")
    print(df.shape)

    print("\n2. MISSING VALUES")
    print(df.isnull().sum())

    print("\n3. DUPLICATE RECORDS")
    print("Total duplicates:", df.duplicated().sum())

    print("\n4. ZERO QUANTITY")
    print("Zero quantity:", (df["Quantity"] == 0).sum())

    print("\n5. NEGATIVE QUANTITY")
    print("Negative quantity:", (df["Quantity"] < 0).sum())

    print("\n6. ZERO UNIT PRICE")
    print("Zero price:", (df["UnitPrice"] == 0).sum())

    print("\n7. NEGATIVE UNIT PRICE")
    print("Negative price:", (df["UnitPrice"] < 0).sum())

    print("\n8. CANCELLED INVOICES")
    print("Cancelled invoices:",
          df["InvoiceNo"].astype(str).str.startswith("C").sum())

    print("\n========== AUDIT COMPLETED ==========")

else:
    print("No file selected.")

root.destroy()