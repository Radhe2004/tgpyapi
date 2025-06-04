import os
import threading
from flask import Flask, request, jsonify
from telegram import Bot
from database import create_tables, get_chat_id
from bot import setup_bot
from telegram.ext import Application

# Setup database
create_tables()

# Setup Telegram Bot
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()
setup_bot(application)

# Flask App for OTP delivery
app = Flask(__name__)

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data.get("username")
    message = data.get("message")
    
    if not username or not message:
        return jsonify({"error": "Invalid request"}), 400
    
    chat_id = get_chat_id(username)
    if chat_id:
        bot.send_message(chat_id=chat_id, text=message)
        return jsonify({"status": "Message delivered"})
    else:
        return jsonify({"error": "Username not found"}), 404

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    application.run_polling()
