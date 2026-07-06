from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Create Employee Database
def create_database():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Create employees table 
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

def update_db():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Check if table is empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]

    # Sample data to insert into the employees table
    employees_data = [
            ('Alice Smith', 'HR', 65000.0),
            ('Bob Jones', 'Engineering', 85000.0),
            ('Charlie Brown', 'Marketing', 55000.0),
            ('Diana Prince', 'Legal', 95000.0),
            ('Evan Wright', 'Finance', 72000.0)
        ]
    if count == 0:
        cursor.executemany('''
                INSERT INTO employees (name, department, salary) 
                VALUES (?, ?, ?)
            ''', employees_data)

    conn.commit()
    conn.close()
    print("Database updated with new employee records.")

#call the function
update_db()

# Home route
@app.route('/')
def home():
    return "Employee Database created successfully!"

#Route to get data in database ( GET METHOD )
@app.route('/employees', methods = ['GET'])
def get_employees():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()

    employee_list = [
        {
            "id": row[0],
            "name": row[1],
            "department": row[2],
            "salary": row[3]
        }
        for row in employees
    ]

    return jsonify(employee_list), 200


@app.route('/employees/<int:employee_id>', methods=['GET']) 
def get_employee_by_id(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
    employee = cursor.fetchone()

    if employee:
        employee_data = {
            "id": employee[0],
            "name": employee[1],
            "department": employee[2],
            "salary": employee[3]
        }
        return jsonify(employee_data), 200
    else:
        return jsonify({"error": "Employee not found"}), 404


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)