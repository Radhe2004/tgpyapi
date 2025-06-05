import os
import threading
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram.ext import Application
from database import get_chat_id, create_tables
from bot import setup_bot

# Initialize DB
create_tables()

# Get Telegram bot token from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise Exception("TELEGRAM_TOKEN not set in environment variables")

# Set up the bot application
application = Application.builder().token(TELEGRAM_TOKEN).build()
setup_bot(application)

# Set up Flask app
app = Flask(__name__)
CORS(app)

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        username = data.get("username")
        message = data.get("message")

        if not username or not message:
            return jsonify({"error": "Missing username or message"}), 400

        chat_id = get_chat_id(username)
        if not chat_id:
            return jsonify({"error": "Username not found"}), 404

        # Send Telegram message using bot from application
        future = asyncio.run_coroutine_threadsafe(
            application.bot.send_message(chat_id=chat_id, text=message),
            application.loop
        )
        future.result(timeout=10)
        return jsonify({"status": "Message sent"})

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    application.run_polling()
