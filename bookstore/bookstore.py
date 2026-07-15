from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Database setup (run once at startup)
def init_db():
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        price INTEGER,
        stock_quantity INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deleted_books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        price INTEGER,
        stock_quantity INTEGER
    )
    """)
    connection.commit()
    connection.close()
    print("✅ Database and 'books' table created successfully!")

# ----Helper functions----
def get_all_books():
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    connection.close()

    books = []
    for row in rows:
        books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "price": row[3],
            "stock_quantity": row[4]
        })
    return books

def get_book_by_id(book_id):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    row = cursor.fetchone()
    connection.close()

    if row:
        return {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "price": row[3],
            "stock_quantity": row[4]
        }
    return None

def insert_book(title, author, price, stock_quantity):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, price, stock_quantity)
        VALUES (?, ?, ?, ?)
    """, (title, author, price, stock_quantity))
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return new_id

def update_book(book_id, title, author, price, stock_quantity):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE books
        SET title=?, author=?, price=?, stock_quantity=?
        WHERE id=?
    """, (title, author, price, stock_quantity, book_id))
    connection.commit()
    updated_rows = cursor.rowcount #returns no. of rows affected : 1= success, 0= no rows updated
    connection.close()
    return updated_rows

def delete_book(book_id):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO deleted_books SELECT * FROM books WHERE id=?", (book_id,))
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    connection.commit()
    deleted_rows = cursor.rowcount
    connection.close()
    return deleted_rows

#--------------------
# ----Routes---------
#--------------------
@app.route("/", methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Online Bookstore API!"}), 200

@app.route("/books", methods=['GET'])
def fetch_books():
    return jsonify({"books": get_all_books()}), 200

# GET /books/<id>
@app.route("/books/<int:book_id>", methods=['GET'])
def fetch_book(book_id):
    book = get_book_by_id(book_id)
    if book:
        return jsonify(book), 200
    else:
        return jsonify({"error": "Book not found"}), 404

# POST route to add new books
@app.route("/books", methods=['POST'])
def add_book():
    data = request.get_json()
    #Validate input
    if not data or not all(k in data for k in ("title", "author", "price", "stock_quantity")):
        return jsonify({"error": "Invalid request. Provide title, author, price, and stock_quantity"}), 400
    #Insert into DB
    new_id = insert_book(data["title"], data["author"], data["price"], data["stock_quantity"])
    return jsonify({"message": "Book added successfully!", "id": new_id}), 201

#PUT /books/<id>
@app.route("/books/<int:book_id>", methods=['PUT'])
def update_book_details(book_id):
    data = request.get_json()

    # Validate input
    if not data or not all(k in data for k in ("title", "author", "price", "stock_quantity")):
        return jsonify({"error": "Invalid request. Provide title, author, price, and stock_quantity"}), 400

    # Check if book exists
    if not get_book_by_id(book_id):
        return jsonify({"error": "Book not found"}), 404

    # Update book
    updated = update_book(book_id, data["title"], data["author"], data["price"], data["stock_quantity"])
    if updated:
        return jsonify({"message": "Book updated successfully!"}), 200
    else:
        return jsonify({"error": "Update failed"}), 500

# DELETE /books/<id> → Delete book by ID
@app.route("/books/<int:book_id>", methods=['DELETE'])
def delete_book_by_id(book_id):
    if not get_book_by_id(book_id):
        return jsonify({"error": "Book not found"}), 404

    deleted = delete_book(book_id)
    if deleted:
        return jsonify({"message": f"Book with ID {book_id} deleted successfully!"}), 200
    else:
        return jsonify({"error": "Delete failed"}), 500
    
# RESTORE ENDPOINT(using archive table)
@app.route("/books/<int:book_id>/restore", methods=['POST'])
def restore_book(book_id):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()

    # Move book back from deleted_books to books
    cursor.execute("INSERT INTO books SELECT * FROM deleted_books WHERE id=?", (book_id,))
    cursor.execute("DELETE FROM deleted_books WHERE id=?", (book_id,))
    connection.commit()
    restored = cursor.rowcount
    connection.close()

    if restored:
        return jsonify({"message": f"Book with ID {book_id} restored successfully!"}), 200
    else:
        return jsonify({"error": "Book not found in archive"}), 404

# Run app
if __name__ == "__main__":
    init_db()  # ensure table exists before starting
    app.run(host="0.0.0.0", port=8080, debug=True)