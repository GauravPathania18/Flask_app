from flask import Flask
import sqlite3

app = Flask(__name__)

# Create Employee Database
def create_database():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Create employees table if it does not already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary REAL NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

    print("Employee database and table created successfully!")

# Call the function
create_database()

# Home route
@app.route('/')
def home():
    return "Employee Database created successfully!"

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)