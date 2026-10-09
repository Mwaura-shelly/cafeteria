import sqlite3

connection = sqlite3.connect("cafeteria.db")
cursor = connection.cursor()

# Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT NOT NULL,
    items TEXT NOT NULL,
    total REAL NOT NULL,
    status TEXT DEFAULT 'Pending'
)
""")

connection.commit()
connection.close()

print("Orders table created successfully!")