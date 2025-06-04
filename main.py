import os
import threading
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram import Bot
from telegram.ext import Application

# Dummy placeholder functions for your DB logic
def create_tables():
    pass

def get_chat_id(username):
    # Replace with your DB lookup for username -> chat_id
    dummy_users = {"alice": 123456789, "bob": 987654321}
    return dummy_users.get(username)

def setup_bot(app):
    # Add handlers to your Application here if needed
    pass

# Setup database tables if not exist
create_tables()

# Telegram Bot setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "YOUR_TELEGRAM_BOT_TOKEN"
bot = Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()
setup_bot(application)

# Flask app with CORS enabled
app = Flask(__name__)
CORS(app)

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data.get("username")
    message = data.get("message")

    if not username or not message:
        return jsonify({"error": "Invalid request, missing username or message"}), 400

    chat_id = get_chat_id(username)

    if chat_id:
        try:
            # Schedule coroutine thread-safe on bot's event loop
            future = asyncio.run_coroutine_threadsafe(
                bot.send_message(chat_id=chat_id, text=message),
                application.loop
            )
            # Wait for result to ensure sending succeeded
            future.result(timeout=10)
            return jsonify({"status": "Message sent"})
        except Exception as e:
            return jsonify({"error": "Failed to send Telegram message", "details": str(e)}), 500
    else:
        return jsonify({"error": "Username not found"}), 404

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    # Run Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Run Telegram bot polling (this blocks main thread)
    application.run_polling()
