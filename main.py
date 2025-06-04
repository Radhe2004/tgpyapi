import os
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram import Bot
from database import create_tables, get_chat_id
from bot import setup_bot
from telegram.ext import Application

# Setup database tables if not exist
create_tables()

# Telegram Bot setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()
setup_bot(application)

# Flask app with CORS enabled
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data.get("username")
    message = data.get("message")

    print(f"[DEBUG] Received send-message request for username={username} message={message}")

    if not username or not message:
        return jsonify({"error": "Invalid request, missing username or message"}), 400

    chat_id = get_chat_id(username)
    print(f"[DEBUG] Resolved chat_id={chat_id} for username={username}")

    if chat_id:
        try:
            # Schedule the async send_message task in the bot's event loop
            application.create_task(bot.send_message(chat_id=chat_id, text=message))
            print("[DEBUG] Scheduled Telegram send_message coroutine")
            return jsonify({"status": "Message scheduled"})
        except Exception as e:
            print(f"[ERROR] Telegram send_message scheduling failed: {e}")
            return jsonify({"error": "Failed to schedule Telegram message", "details": str(e)}), 500
    else:
        print(f"[WARN] Username not found: {username}")
        return jsonify({"error": "Username not found"}), 404

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/favicon.ico")
def favicon():
    return "", 204  # Prevent favicon errors

@app.route("/debug-users")
def debug_users():
    from database import get_db_connection
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT username, chat_id FROM users")
            rows = cur.fetchall()
            return jsonify(rows)

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    application.run_polling()
