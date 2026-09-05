import sqlite3
import matplotlib.pyplot as plt

def generate_sales_chart():
    # Connect to the database
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    # Fetch product names and quantities sold
    cursor.execute("""
        SELECT product_name, SUM(quantity)
        FROM sales
        GROUP BY product_name
    """)

    data = cursor.fetchall()

    connection.close()

    if not data:
        print("\n❌ No sales data available.")
        return

    # Separate product names and quantities
    products = [row[0] for row in data]
    quantities = [row[1] for row in data]

    # Create the chart
    plt.figure(figsize=(8, 5))
    plt.bar(products, quantities)

    plt.title("Sales Quantity by Product")
    plt.xlabel("Products")
    plt.ylabel("Quantity Sold")

    plt.tight_layout()

    # Save the chart
    plt.savefig("sales_chart.png")

    print("\n✅ Sales chart generated successfully!")
    print("📄 File Name: sales_chart.png")

    plt.show()