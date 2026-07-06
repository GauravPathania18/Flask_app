from flask import Flask
import random

app = Flask(__name__)

# List of motivational quotes
motivational_quotes = [
    "Start where you are. You don't have to be great to start, but you must start to be great.",
    "Embrace your failures. Every mistake is simply a stepping stone and a lesson learned, not a stop sign.",
    "Control what you can. Stop stressing over the things you cannot change and pour your energy into your own actions.",
    "Consistency beats intensity. Small, daily habits yield massive, life-changing results over time.",
    "Protect your focus. Say no to distractions and say yes to the things that move you closer to your goals.",
    "Embrace the challenge. Great things never come from comfort zones. If it challenges you, it changes you.",
    "Choose progress over perfection. Keep moving forward. A step in the right direction, no matter how small, is a victory.",
    "Trust the process. Patience and persistence are an unbeatable combination for achieving any long-term success.",
    "Believe in yourself. You hold the power to shape your destiny. The only person you are destined to become is the one you decide to be.",
    "Keep going. Even on tough days, remember why you started and keep pushing forward."
]


@app.route('/')
def home():
    quote = random.choice(motivational_quotes)  # Pick a random quote
    return f"<h1>Motivational Quote of the Day</h1><p>{quote}</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)