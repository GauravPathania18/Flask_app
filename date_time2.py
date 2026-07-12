from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return (
        "<h1>Welcome to the Internet-Synced Date and Time API!</h1>"
        "<p>To get the accurate internet time, visit: <code>/time</code></p>"
    )

@app.route('/time', methods=['GET'])
def get_internet_time():
    try:
        # Fetch current time for UTC (or change to 'Asia/Kolkata', 'America/New_York', etc.)
        response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC", timeout=5)
        response_data = response.json()
        
        # WorldTimeAPI returns a 'datetime' string like "2026-07-06T15:00:23.123456+00:00"
        raw_datetime = response_data['datetime']
        
        # Format it cleanly to YYYY-MM-DD HH:MM:SS
        # Stripping the T separator and dropping the milliseconds/timezone offset
        formatted_time = raw_datetime.replace('T', ' ').split('.')[0]
        
        return jsonify({
            "source": "Internet (WorldTimeAPI)",
            "current_time": formatted_time
        }), 200

    except Exception as e:
        # Fallback mechanism in case the internet API is down or times out
        return jsonify({
            "error": "Failed to fetch time from internet",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)