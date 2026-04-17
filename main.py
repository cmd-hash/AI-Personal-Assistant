from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from mistralai import Mistral 

# Load environment variables
load_dotenv()

app = Flask(__name__)

# API setup
api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)


# Home route
@app.route("/")
def home():
    return render_template("index.html")


#  Ask Anything
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("question")

    if not user_input:
        return jsonify({"response": "Please enter a question"})

    response = client.chat.complete(
        model="mistral-medium-latest",
        messages=[
            {"role": "system", "content": "Act like a helpful personal assistant"},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=300
    )

    answer = response.choices[0].message.content.strip()
    return jsonify({"response": answer})


#  Summarize Email
@app.route("/summarize", methods=["POST"])
def summarize():
    
    email_text = request.form.get("Email")

    if not email_text:
        return jsonify({"summary": "Please enter email text"})

    response = client.chat.complete(
        model="mistral-medium-latest",
        messages=[
            {"role": "system", "content": "Summarize emails in 2-3 sentences"},
            {"role": "user", "content": f"Summarize this:\n\n{email_text}"}
        ],
        temperature=0.3,
        max_tokens=300
    )

    summary = response.choices[0].message.content.strip()
    return jsonify({"summary": summary})


if __name__ == "__main__":
    app.run(debug=True)