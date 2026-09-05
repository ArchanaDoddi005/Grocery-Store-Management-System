import sqlite3
from openpyxl import Workbook


def export_sales_to_excel():
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Sales Report"

    sheet.append([
        "Sale ID",
        "Product Name",
        "Price",
        "Quantity",
        "Total",
        "Date"
    ])

    for sale in sales:
        sheet.append(sale)

    workbook.save("sales_report.xlsx")

    connection.close()

    print("\n✅ Sales report exported successfully!")
    print("📄 File Name: sales_report.xlsx")