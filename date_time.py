from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return (
        "<h1>Welcome to the Current Date and Time API!</h1>"
        "<p>To get the current date and time, visit: "
        "<code>/time</code></p>"
    )

@app.route('/time', methods=['GET'])
def get_current_time():
    # Fetch the current date and time from the system
    now = datetime.now()
    
    # Format it as YYYY-MM-DD HH:MM:SS
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Return the formatted string in JSON format
    return jsonify({
        "current_time": formatted_time
    }), 200

if __name__ == "__main__":
    # Standard Codespaces configuration running on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)