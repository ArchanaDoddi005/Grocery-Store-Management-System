import sqlite3
from pdf_invoice import generate_pdf

def generate_bill():
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    print("\n========== BILLING ==========")

    product_name = input("Enter Product Name: ")

    cursor.execute(
        "SELECT * FROM products WHERE product_name = ?",
        (product_name,)
    )

    product = cursor.fetchone()

    if product is None:
        print("\n❌ Product not found.")
        connection.close()
        return

    print(f"\nProduct : {product[1]}")
    print(f"Price   : ₹{product[4]}")
    print(f"Stock   : {product[5]}")

    try:
        quantity = int(input("\nEnter Quantity: "))
    except ValueError:
        print("\n❌ Quantity must be a number.")
        connection.close()
        return

    if quantity <= 0:
        print("\n❌ Quantity must be greater than zero.")
        connection.close()
        return

    if quantity > product[5]:
        print("\n❌ Insufficient stock available.")
        connection.close()
        return

    total = quantity * product[4]

    print("\n========== BILL ==========")
    print(f"Product  : {product[1]}")
    print(f"Price    : ₹{product[4]}")
    print(f"Quantity : {quantity}")
    print(f"Total    : ₹{total}")

    remaining_stock = product[5] - quantity

    cursor.execute("""
    UPDATE products
    SET quantity = ?
    WHERE product_id = ?
    """, (remaining_stock, product[0]))

    cursor.execute("""
    INSERT INTO sales (product_name, price, quantity, total)
    VALUES (?, ?, ?, ?)
    """, (
        product[1],
        product[4],
        quantity,
        total
))

    connection.commit()
   
    print(f"\nRemaining Stock : {remaining_stock}")
    print("\n✅ Stock updated successfully!")
    generate_pdf(product[1], product[4], quantity, total)

    connection.close()