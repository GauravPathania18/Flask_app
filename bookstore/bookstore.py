from flask import Flask, jsonify
import sqlite3
app = Flask(__name__)


connection = sqlite3.connect("books.db")  # creates database file if it doesn’t exist
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

connection.commit()
connection.close()
print("✅ Database and 'books' table created successfully!")

@app.route("/", methods =['GET'])
def home():
    return jsonify({"message": "Welcome to the Online Bookstore API!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)