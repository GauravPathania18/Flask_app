from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return (
        "<h1>Welcome to the Calculator API!</h1>"
        "<p>To use the calculator, enter two numbers in the URL like this: "
        "<code>/calculate/num1/num2</code></p>"
    )

@app.route('/calculate/<int:num1>/<int:num2>', methods=['GET'])
def calculate(num1, num2):
    # Perform basic arithmetic operations
    addition = num1 + num2
    subtraction = num1 - num2
    multiplication = num1 * num2
    division = num1 / num2 if num2 != 0 else "undefined (division by zero)"

    # Return the results in JSON format
    return jsonify({
        "num1": num1,
        "num2": num2,
        "addition": addition,
        "subtraction": subtraction,
        "multiplication": multiplication,
        "division": division
    }), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)