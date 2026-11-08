import csv
import os
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

from chatbot import Chatbot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_MESSAGE_LENGTH = 300
UNANSWERED_LOG = os.path.join(BASE_DIR, "logs", "unanswered.csv")

app = Flask(__name__)
bot = Chatbot(os.path.join(BASE_DIR, "intents.json"))


def log_unanswered(message: str, confidence: float) -> None:
    """Save questions the bot could not answer so intents.json can be improved."""
    os.makedirs(os.path.dirname(UNANSWERED_LOG), exist_ok=True)
    new_file = not os.path.exists(UNANSWERED_LOG)
    with open(UNANSWERED_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["time_utc", "message", "confidence"])
        writer.writerow([datetime.now(timezone.utc).isoformat(timespec="seconds"), message, confidence])


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify(error="Message is empty."), 400
    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify(error=f"Message is too long (max {MAX_MESSAGE_LENGTH} characters)."), 400

    result = bot.reply(message)
    if result["tag"] == "fallback":
        log_unanswered(message, result["confidence"])
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
