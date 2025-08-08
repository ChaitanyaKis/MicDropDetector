from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env (for local dev)
load_dotenv()

app = Flask(__name__)

# ✅ Read API key from environment
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "openai/gpt-oss-20b"

# ✅ Log the key status clearly (only for debugging)
if OPENROUTER_API_KEY:
    print("🔑 OPENROUTER_API_KEY loaded ✅")
else:
    print("❌ OPENROUTER_API_KEY NOT FOUND in env variables!")

# ✅ Fail early if key is missing
assert OPENROUTER_API_KEY, "❌ OPENROUTER_API_KEY is not set. Please add it to Railway Environment Variables."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rate', methods=['POST'])
def rate_joke():
    data = request.get_json()
    joke = data.get("joke", "").strip()

    if not joke:
        return jsonify({"error": "No joke provided"}), 400

    # 🧠 Savage rating prompt
    prompt = f"""
You're the ultimate savage roast judge at a mic-drop battle.

Every joke is judged like it's on live TV. You don't hold back. You're ruthless, hilarious, and unfiltered. If it's weak, roast it so hard it gets PTSD. If it’s fire, HYPE it like a screaming crowd just fainted. Your goal is to make people *laugh out loud* at your feedback, not just read it.

Joke: \"{joke}\"

Respond ONLY in this format:

Burn Score: (1 to 10)  
Verdict: (1-line crowd reaction like "OHHHHHHHH!", "That joke committed murder!", etc.)  
Feedback: (Make this the FUNNIEST, most BRUTAL roast of the joke possible — like a stand-up comic destroying a heckler. Be savage, sarcastic, loud, and clever. No boring advice. No over-explaining. Just raw comedy. If the joke makes no sense, make fun of how confused you are. If it slaps, act like you just witnessed history max 109 characters.)

You are a mix of Dave Chappelle, Kevin Hart, and a roast battle god. Never be polite. Always be hilarious.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "MicDropDetector.ai"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a roast rating assistant. Respond with Burn Score, Verdict, and Feedback."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    except Exception as e:
        print("❌ Error in OpenRouter request:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
