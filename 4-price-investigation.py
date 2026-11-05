import pandas as pd
from tkinter import Tk, filedialog

# Select original dataset
root = Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select Online Retail Dataset",
    filetypes=[("Excel Files", "*.xlsx")]
)

if file_path:

    df = pd.read_excel(file_path)

    # Identify unusual prices
    zero_price = df[df["UnitPrice"] == 0]
    negative_price = df[df["UnitPrice"] < 0]

    print("\n===== PRICE INVESTIGATION =====")

    print("\n1. Zero price records:")
    print(len(zero_price))

    print("\n2. Negative price records:")
    print(len(negative_price))

    print("\n3. Sample zero price records:")
    print(zero_price.head(10).to_string(index=False))

    print("\n4. Negative price records:")
    print(negative_price.to_string(index=False))

    print("\n5. Zero price by description:")
    print(zero_price["Description"].value_counts().head(10))

    print("\n===== INVESTIGATION COMPLETED =====")

else:
    print("No file selected.")

root.destroy()