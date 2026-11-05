import pandas as pd
from tkinter import Tk, filedialog

# Open a window to select the Excel file
root = Tk()
root.withdraw()

print("Please select your Online Retail.xlsx file...")

file_path = filedialog.askopenfilename(
    title="Select Online Retail Dataset",
    filetypes=[("Excel Files", "*.xlsx")]
)

if not file_path:
    print("No file selected. Please run the program again.")
else:
    print("\nLoading dataset...")

    df = pd.read_excel(file_path)

    print("\n===== DATASET SIZE =====")
    print("Rows and columns:", df.shape)

    print("\n===== FIRST 5 RECORDS =====")
    print(df.head())

    print("\n===== COLUMN INFORMATION =====")
    df.info()

    print("\n===== MISSING VALUES =====")
    print(df.isnull().sum())

    print("\n===== DUPLICATE RECORDS =====")
    print(df.duplicated().sum())

    print("\n===== NUMERICAL SUMMARY =====")
    print(df.describe())

    print("\n===== INSPECTION COMPLETED =====")

root.destroy()