import streamlit as st
import sqlite3
import pandas as pd
from pdf_invoice import generate_pdf

# Page Configuration
st.set_page_config(
    page_title="Grocery Store Management System",
    page_icon="🛒",
    layout="wide"
)

def get_products():
    connection = sqlite3.connect("database/grocery.db")
    query = "SELECT * FROM products"
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

def add_product_db(product_name, category, brand, price, quantity, supplier, expiry_date):
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products
        (product_name, category, brand, price, quantity, supplier, expiry_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (product_name, category, brand, price, quantity, supplier, expiry_date))

    connection.commit()
    connection.close()

def search_product_db(product_name):
    connection = sqlite3.connect("database/grocery.db")

    query = """
        SELECT *
        FROM products
        WHERE product_name LIKE ?
    """

    df = pd.read_sql_query(
        query,
        connection,
        params=(f"%{product_name}%",)
    )

    connection.close()

    return df


def update_product_db(product_id, new_price, new_quantity):
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE products
        SET price = ?, quantity = ?
        WHERE product_id = ?
        """,
        (new_price, new_quantity, product_id)
    )

    connection.commit()
    connection.close()

def delete_product_db(product_id):
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    cursor.execute(
    "DELETE FROM products WHERE product_id=?",
    (product_id,)
)

    connection.commit()
    connection.close()

def get_product(product_name):
    connection = sqlite3.connect("database/grocery.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE product_name=?",
        (product_name,)
    )

    product = cursor.fetchone()

    connection.close()

    return product

def complete_sale(product, quantity):
    connection = sqlite3.connect("database/grocery.db")
    cursor = connection.cursor()

    product_id = product[0]
    product_name = product[1]
    price = product[4]
    current_stock = product[5]

    total = quantity * price
    remaining_stock = current_stock - quantity

    # Update product stock
    cursor.execute(
        """
        UPDATE products
        SET quantity = ?
        WHERE product_id = ?
        """,
        (remaining_stock, product_id)
    )

    # Save sale
    cursor.execute(
        """
        INSERT INTO sales
        (product_name, price, quantity, total)
        VALUES (?, ?, ?, ?)
        """,
        (product_name, price, quantity, total)
    )

    connection.commit()
    connection.close()

    return total, remaining_stock

def get_sales():
    connection = sqlite3.connect("database/grocery.db")
    query = """
        SELECT
            sale_id,
            product_name,
            price,
            quantity,
            total,
            sale_date
        FROM sales
        ORDER BY sale_id DESC
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df

def get_sales_report():

    connection = sqlite3.connect("database/grocery.db")

    query = """
        SELECT
            COUNT(*) AS total_sales,
            SUM(quantity) AS total_quantity,
            SUM(total) AS total_revenue
        FROM sales
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df

# Sidebar

st.sidebar.title("🛒 Grocery Store")

menu = st.sidebar.radio(
    "Select an Option",
    [
        "🏠 Home",
        "➕ Add Product",
        "📋 View Products",
        "🔍 Search Product",
        "✏️ Update Product",
        "❌ Delete Product",
        "🛒 Billing",
        "📜 Sales History",
        "📊 Sales Report",
        "📈 Sales Chart"
    ]
)

# Home Page

if menu == "🏠 Home":

    st.title("🛒 Grocery Store Management System")

    st.success("Welcome to the Grocery Store Dashboard!")

    st.write("### Features")

    st.write("✅ Product Management")
    st.write("✅ Billing System")
    st.write("✅ Sales History")
    st.write("✅ Sales Reports")
    st.write("✅ Excel Export")
    st.write("✅ PDF Invoice")
    st.write("✅ Sales Chart")

# Add Product

elif menu == "➕ Add Product":

    st.header("➕ Add Product")

    product_name = st.text_input("Product Name")

    category = st.text_input("Category")

    brand = st.text_input("Brand")

    price = st.number_input("Price",min_value=0.0,format="%.2f")

    quantity = st.number_input("Quantity",min_value=0,step=1)

    supplier = st.text_input("Supplier")

    expiry_date = st.date_input("Expiry Date")

    if st.button("Add Product"):

        add_product_db(
            product_name,
            category,
            brand,
            price,
            quantity,
            supplier,
            str(expiry_date)
        )

        st.success("✅ Product Added Successfully!")

# View Products

elif menu == "📋 View Products":

    st.header("📋 View Products")

    df = get_products()

    if df.empty:
        st.warning("No products found.")

    else:
        st.dataframe(
            df,
            use_container_width=True
        )


# Search Product

elif menu == "🔍 Search Product":

    st.header("🔍 Search Product")

    search = st.text_input("Enter Product Name")

    if st.button("Search"):

        df = search_product_db(search)

        if df.empty:
            st.error("❌ Product Not Found")

        else:
            st.success("✅ Product Found")
            st.dataframe(
                df,
                use_container_width=True
            )


# Update Product

elif menu == "✏️ Update Product":

    st.header("✏️ Update Product")

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        step=1
    )

    new_price = st.number_input(
        "New Price",
        min_value=0.0,
        format="%.2f"
    )

    new_quantity = st.number_input(
        "New Quantity",
        min_value=0,
        step=1
    )

    if st.button("Update Product"):

        update_product_db(
            product_id,
            new_price,
            new_quantity
        )

        st.success("✅ Product Updated Successfully!")


# Delete Product

elif menu == "❌ Delete Product":

    st.header("❌ Delete Product")

    product_id = st.number_input(
        "Enter Product ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Product"):

        delete_product_db(product_id)

        st.success("✅ Product Deleted Successfully!")


# Billing

elif menu == "🛒 Billing":

    st.header("🛒 Billing")

    product_name = st.text_input("Enter Product Name")

    quantity = st.number_input(
        "Enter Quantity",
        min_value=1,
        step=1
    )

    if st.button("Generate Bill"):

        product = get_product(product_name)

        if product is None:

            st.error("❌ Product not found.")

        elif quantity > product[5]:

            st.error("❌ Insufficient Stock!")

        else:

            total, remaining_stock = complete_sale(
                product,
                quantity
            )

            st.success("✅ Bill Generated Successfully!")

            st.write("### Bill Details")

            st.write(f"**Product:** {product[1]}")
            st.write(f"**Price:** ₹{product[4]}")
            st.write(f"**Quantity:** {quantity}")
            st.write(f"**Total:** ₹{total}")
            st.write(f"**Remaining Stock:** {remaining_stock}")

            generate_pdf(
                product[1],
                product[4],
                quantity,
                total
            )

            st.success("📄 PDF Invoice Generated Successfully!")

elif menu == "📜 Sales History":

    st.header("📜 Sales History")

    df = get_sales()

    if df.empty:
        st.warning("No sales found.")

    else:
        st.dataframe(
            df,
            use_container_width=True
        )

elif menu == "📊 Sales Report":

    st.header("📊 Sales Report")

    df = get_sales_report()

    if df.empty:
        st.warning("No sales data found.")

    else:

        total_sales = df["total_sales"].iloc[0]
        total_quantity = df["total_quantity"].iloc[0]
        total_revenue = df["total_revenue"].iloc[0]

        st.metric("🧾 Total Sales", total_sales)

        st.metric("📦 Total Quantity Sold", total_quantity)

        st.metric("💰 Total Revenue", f"₹{total_revenue:.2f}")

elif menu == "📈 Sales Chart":

    st.header("📈 Sales Chart")

    connection = sqlite3.connect("database/grocery.db")

    query = """
        SELECT product_name, SUM(total) AS total_sales
        FROM sales
        GROUP BY product_name
        ORDER BY total_sales DESC
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    if df.empty:
        st.warning("No sales data available.")

    else:
        st.subheader("Sales by Product")

        st.bar_chart(
            df.set_index("product_name")["total_sales"]
        )