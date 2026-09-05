import pandas as pd

df = pd.read_excel("sales_report.xlsx", engine="openpyxl")

print("\n========== SALES REPORT ==========\n")
print(df)