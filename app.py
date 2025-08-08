from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Replace with your actual OpenRouter API key
OPENROUTER_API_KEY = "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"
MODEL = "openai/gpt-3.5-turbo"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rate', methods=['POST'])
def rate_joke():
    data = request.get_json()
    joke = data.get("joke", "").strip()

    if not joke:
        return jsonify({"error": "No joke provided"}), 400

    # 🧠 Brutal, clear, mic-drop-focused prompt

    prompt = f"""
You're the ultimate savage roast judge at a mic-drop battle.

Every joke is judged like it's on live TV. You don't hold back. You're ruthless, hilarious, and unfiltered. If it's weak, roast it so hard it gets PTSD. If it’s fire, HYPE it like a screaming crowd just fainted. Your goal is to make people *laugh out loud* at your feedback, not just read it.

Joke: \"{joke}\"

Respond ONLY in this format:

Burn Score: (1 to 10)  
Verdict: (1-line crowd reaction like "OHHHHHHHH!", "That joke committed murder!", etc.)  
Feedback: (Make this the FUNNIEST, most BRUTAL roast of the joke possible — like a stand-up comic destroying a heckler. Be savage, sarcastic, loud, and clever. No boring advice. No over-explaining. Just raw comedy. If the joke makes no sense, make fun of how confused you are. If it slaps, act like you just witnessed history max 109 charecters.)

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
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
