import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-fact', methods=['POST'])
def generate_fact():
    data = request.get_json()
    topic = data.get('topic')

    prompt = f"Tell me one interesting fun fact about {topic}. Keep it short."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"

    response = requests.post(url, json={
        "contents": [{"parts": [{"text": prompt}]}]
    })

    result = response.json()

    if "candidates" not in result:
        return jsonify({"fact": f"API error: {result}"})

    fact = result["candidates"][0]["content"]["parts"][0]["text"]
    return jsonify({"fact": fact})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)