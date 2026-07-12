import sqlite3

# Connect to the database
connection = sqlite3.connect("books.db")
cursor = connection.cursor()

# Insert sample book records
books = [
    ("The Great Gatsby", "F. Scott Fitzgerald", 300, 10),
    ("To Kill a Mockingbird", "Harper Lee", 250, 8),
    ("1984", "George Orwell", 200, 15),
    ("Pride and Prejudice", "Jane Austen", 350, 12),
    ("The Catcher in the Rye", "J.D. Salinger", 280, 5)
]

cursor.executemany("""
INSERT INTO books (title, author, price, stock_quantity)
VALUES (?, ?, ?, ?)
""", books)

connection.commit()
connection.close()

print("✅ Sample book records inserted successfully!")
