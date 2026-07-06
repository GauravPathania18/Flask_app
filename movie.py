from flask import Flask, jsonify
import random

app = Flask(__name__)

movies_list = [
    "The Shawshank Redemption",
    "The Dark Knight",
    "Inception",
    "Interstellar",
    "Pulp Fiction",
    "The Matrix",
    "Forrest Gump",
    "Spirited Away",
    "Gladiator",
    "Avatar"
]

@app.route('/')
def home():
    return (
        "<h1>Welcome to the Random Movie Suggestion API!</h1>"
        "<p>To get a random movie suggestion, visit: "
        "<code>/movie</code></p>"
    )

@app.route('/movie', methods=['GET'])
def get_random_movie():
    # Randomly select a movie from the list
    suggested_movie = random.choice(movies_list)
    
    # Return the recommendation in JSON format
    return jsonify({
        "suggestion": suggested_movie
    }), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)