import sqlite3

def insert_sample_books():
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()

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

if __name__ == "__main__":
    insert_sample_books()
