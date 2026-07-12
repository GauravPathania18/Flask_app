from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods =['GET'])
def home():
    return jsonify({"message": "Welcome to the Online Bookstore API!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)