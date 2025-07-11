from flask import Flask, render_template, request, jsonify, session
import requests
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Ganti dengan string acak yang aman

TOGETHER_API_KEY = "tgp_v1_pRd7ya0V8UWwKlgyWmSU5Cm3JktDlEqNc2_JtZSArOU"

TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

@app.route("/")
def index():
    # Ambil histori dari session
    history = session.get("history", [])
    return render_template("index.html", history=history)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message")

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "Kamu adalah asisten AI yang membantu pengguna dengan jawaban yang jelas."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 512,
        "top_p": 0.7
    }

    response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        # Simpan histori ke session
        history = session.get("history", [])
        history.append({"role": "user", "message": user_message})
        history.append({"role": "bot", "message": reply})
        session["history"] = history

        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": "Terjadi error pada API Together AI."})

@app.route("/clear", methods=["POST"])
def clear_history():
    session.pop("history", None)
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
