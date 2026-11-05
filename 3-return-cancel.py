import pandas as pd
from tkinter import Tk, filedialog

# Select dataset
root = Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select Online Retail Dataset",
    filetypes=[("Excel Files", "*.xlsx")]
)

if file_path:

    df = pd.read_excel(file_path)

    # Identify cancelled transactions
    cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

    # Identify negative quantities
    returns = df["Quantity"] < 0

    print("\n===== RETURN AND CANCELLATION ANALYSIS =====")

    print("\n1. Total records:", len(df))

    print("\n2. Negative quantity records:", returns.sum())

    print("\n3. Cancelled transaction records:", cancelled.sum())

    print("\n4. Negative quantity AND cancelled records:",
          (returns & cancelled).sum())

    print("\n5. Negative quantity with normal invoice numbers:",
          (returns & ~cancelled).sum())

    print("\n6. Unique cancelled invoice numbers:",
          df.loc[cancelled, "InvoiceNo"].nunique())

    print("\n7. Sample return records:")
    print(df.loc[returns].head(10))

    print("\n8. Sample cancelled records:")
    print(df.loc[cancelled].head(10))

    print("\n===== ANALYSIS COMPLETED =====")

else:
    print("No file selected.")

root.destroy()