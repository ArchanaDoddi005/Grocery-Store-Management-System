import sqlite3

# Connect to the database
connection = sqlite3.connect("database/grocery.db")

# Create a cursor
cursor = connection.cursor()

# Create the Products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    brand TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    supplier TEXT,
    expiry_date TEXT
)
""")
cursor.execute("DROP TABLE IF EXISTS sales")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    total REAL NOT NULL,
    sale_date TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Save changes
connection.commit()

# Close the connection
connection.close()

print("Database and Products table created successfully!")