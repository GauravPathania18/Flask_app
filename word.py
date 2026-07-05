from flask import Flask, jsonify

app = Flask(__name__)

# 1. Home route with instructions
@app.route('/')
def home():
    return """
    <h1>Welcome to the Reverse Word API!</h1>
    <p>To use this API, enter a word in the URL like this: 
    <code>/reverse/your_word_here</code></p>
    """

# 2. API route to reverse the word and return JSON
@app.route('/reverse/<word>')
def reverse_word(word):
    # Reverse the string using Python slicing
    reversed_str = word[::-1]
    
    # Return both original and reversed word in JSON format
    return jsonify({
        "original": word,
        "reversed": reversed_str
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)