import sqlite3
from billing import generate_bill
from excel_export import export_sales_to_excel
from sales_chart import generate_sales_chart

def add_product():
    # Connect to the database
    connection = sqlite3.connect("database/grocery.db")

# Create a cursor
    cursor = connection.cursor()

# Get input from the user
    try:
        product_name = input("Enter Product Name: ")
        category = input("Enter Category: ")
        brand = input("Enter Brand: ")
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))
        supplier = input("Enter Supplier: ")
        expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")

    except ValueError:
        print("\n❌ Invalid input! Price must be a number and Quantity must be an integer.")
        connection.close()
        return
  
    # Insert data into the table
    cursor.execute("""
        INSERT INTO products
        (product_name, category, brand, price, quantity, supplier, expiry_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        product_name,
        category,
        brand,
        price,
        quantity,
        supplier,
        expiry_date
    ))

    # Save the changes
    connection.commit()

    # Close the connection
    connection.close()

    print("\n✅ Product added successfully!")

# Call the function
def view_products():
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    connection.close()

    if len(products) == 0:
        print("\nNo products found.")
    else:
        print("\n========== PRODUCT LIST ==========")

        print("\n" + "=" * 100)
        print("{:<5} {:<20} {:<15} {:<15} {:<10} {:<8} {:<20} {:<15}".format(
    "ID", "Product Name", "Category", "Brand", "Price",
    "Qty", "Supplier", "Expiry Date"))
        print("=" * 100)

        for product in products:
            print("{:<5} {:<20} {:<15} {:<15} {:<10} {:<8} {:<20} {:<15}".format(
        product[0],
        product[1],
        product[2],
        product[3],
        product[4],
        product[5],
        product[6],
        product[7]
    ))

print("=" * 100)
# 3. Search Product Function
def search_product():
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    product_name = input("Enter Product Name to Search: ")
    if product_name.strip() == "":
        print("\n❌ Product name cannot be empty.")
        connection.close()
        return
    cursor.execute(
        "SELECT * FROM products WHERE product_name = ?",
        (product_name,)
    )

    product = cursor.fetchone()

    connection.close()

    if product:
        print("\n===== PRODUCT FOUND =====")
        print(f"Product ID   : {product[0]}")
        print(f"Name         : {product[1]}")
        print(f"Category     : {product[2]}")
        print(f"Brand        : {product[3]}")
        print(f"Price        : ₹{product[4]}")
        print(f"Quantity     : {product[5]}")
        print(f"Supplier     : {product[6]}")
        print(f"Expiry Date  : {product[7]}")
    else:
        print("\n❌ Product not found.")


# 👇 Paste the new function here
def update_product():
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    try:
        product_id = int(input("Enter Product ID to Update: "))
    except ValueError:
        print("\n❌ Product ID must be a number.")
        connection.close()
        return

    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()

    if product:
        print("\nCurrent Product Details")
        print(f"Name     : {product[1]}")
        print(f"Price    : {product[4]}")
        print(f"Quantity : {product[5]}")

        try:
            new_price = float(input("Enter New Price: "))
            new_quantity = int(input("Enter New Quantity: "))
        except ValueError:
            print("\n❌ Price and Quantity must be numbers.")
            connection.close()
            return

        cursor.execute("""
            UPDATE products
            SET price = ?, quantity = ?
            WHERE product_id = ?
        """, (new_price, new_quantity, product_id))

        connection.commit()
        print("\n✅ Product updated successfully!")

    else:
        print("\n❌ Product ID not found.")

    connection.close()


# 👇 After all functions, the menu starts
def delete_product():
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    try:
        product_id = int(input("Enter Product ID to Delete: "))
    except ValueError:
        print("\n❌ Product ID must be a number.")
        connection.close()
        return


    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()

    if product:
        print("\nProduct Found")
        print(f"Name     : {product[1]}")
        print(f"Category : {product[2]}")
        print(f"Price    : {product[4]}")

        confirm = input("\nAre you sure you want to delete? (Y/N): ")

        if confirm.upper() == "Y":
            cursor.execute(
                "DELETE FROM products WHERE product_id = ?",
                (product_id,)
            )
            connection.commit()
            print("\n✅ Product deleted successfully!")
        else:
            print("\nDeletion cancelled.")

    else:
        print("\n❌ Product ID not found.")

    connection.close()

def view_sales():
    import sqlite3

    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()

    connection.close()

    if len(sales) == 0:
        print("\nNo sales found.")
    else:
        print("\n================ SALES HISTORY ================")
        print("{:<8} {:<15} {:<10} {:<10} {:<10} {:<20}".format(
            "Sale ID", "Product", "Price", "Qty", "Total", "Date"))
        print("=" * 80)

        for sale in sales:
            print("{:<8} {:<15} {:<10} {:<10} {:<10} {:<20}".format(
                sale[0],
                sale[1],
                sale[2],
                sale[3],
                sale[4],
                sale[5]
            ))

def low_stock():
    import sqlite3

    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE quantity < 10"
    )

    products = cursor.fetchall()

    connection.close()

    if len(products) == 0:
        print("\n✅ No low stock products.")
    else:
        print("\n========== LOW STOCK PRODUCTS ==========")

        print("{:<5} {:<20} {:<10}".format(
            "ID", "Product", "Quantity"
        ))

        print("=" * 40)

        for product in products:
            print("{:<5} {:<20} {:<10}".format(
                product[0],
                product[1],
                product[5]
            ))

def sales_report():
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_sales,
            SUM(quantity) AS total_items,
            SUM(total) AS total_revenue
        FROM sales
    """)

    report = cursor.fetchone()

    connection.close()

    total_sales = report[0] if report[0] else 0
    total_items = report[1] if report[1] else 0
    total_revenue = report[2] if report[2] else 0

    print("\n========== SALES REPORT ==========")
    print(f"Total Sales       : {total_sales}")
    print(f"Total Items Sold  : {total_items}")
    print(f"Total Revenue     : ₹{total_revenue}")
            
while True:
    
    print("\n===== Grocery Store Management =====")
    print("1. Add Product")
    print("2. View Products")
    print("3. Search Product")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Billing")
    print("7. Sales History")
    print("8. Low Stock Alert")
    print("9. Sales Report")
    print("10. Export Sales to Excel")
    print("11. Generate Sales Chart")
    print("12. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_product()

    elif choice == "2":
        view_products()

    elif choice == "3":
        search_product()

    elif choice == "4":
        update_product()

    elif choice == "5":
        delete_product()

    elif choice == "6":
        generate_bill()

    elif choice == "7":
        view_sales()

    elif choice == "8":
        low_stock()

    elif choice == "9":
        sales_report()

    elif choice == "10":
        export_sales_to_excel()

    elif choice == "11":
        generate_sales_chart()

    elif choice == "12":
        print("Thank you!")
        break

    else:
        print("Invalid choice. Try again.")
    