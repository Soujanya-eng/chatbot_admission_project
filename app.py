from flask import Flask, render_template, request, jsonify
import json
import random
import difflib

app = Flask(__name__)

with open("intents.json") as file:
    data = json.load(file)

def chatbot_response(user_input):

    user_input = user_input.lower()

    best_match = None
    highest_score = 0

    for intent in data["intents"]:
        for pattern in intent["patterns"]:

            score = difflib.SequenceMatcher(None, user_input, pattern.lower()).ratio()

            if score > highest_score:
                highest_score = score
                best_match = intent

    if highest_score > 0.5:
        return random.choice(best_match["responses"])

    return "Sorry, I didn't understand. Please ask about admissions, departments, placements or contact details."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def chatbot():
    user_message = request.json.get("message")
    response = chatbot_response(user_message)
    return jsonify({"reply": response})


if __name__ == "__main__":
    app.run(debug=True)