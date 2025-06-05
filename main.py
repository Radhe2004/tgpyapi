import os
import threading
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram.ext import Application
from database import get_chat_id, create_tables
from bot import setup_bot  # assuming your handlers are in bot.py

# Setup DB
create_tables()

# Telegram Application setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
application = Application.builder().token(TELEGRAM_TOKEN).build()
setup_bot(application)

# Flask app setup
app = Flask(__name__)
CORS(app)

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data.get("username")
    message = data.get("message")

    if not username or not message:
        return jsonify({"error": "Missing username or message"}), 400

    chat_id = get_chat_id(username)
    if not chat_id:
        return jsonify({"error": "Username not found"}), 404

    try:
        future = asyncio.run_coroutine_threadsafe(
            application.bot.send_message(chat_id=chat_id, text=message),
            application.loop
        )
        future.result(timeout=10)
        return jsonify({"status": "Message sent"})
    except Exception as e:
        return jsonify({"error": "Failed to send Telegram message", "details": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    # Run Flask app in separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Run Telegram bot
    application.run_polling()
