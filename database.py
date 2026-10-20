import sqlite3

connection = sqlite3.connect("automobile.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    vehicle TEXT NOT NULL,
    service TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

connection.commit()
connection.close()

print("Database created successfully!")
