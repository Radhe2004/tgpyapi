from flask import Flask, request, jsonify
from telegram import Bot
from database import get_chat_id, create_tables
import os

app = Flask(__name__)
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))

@app.before_first_request
def initialize():
    create_tables()
    if webhook_url := os.getenv('WEBHOOK_URL'):
        bot.set_webhook(url=f"{webhook_url}/telegram-webhook")

@app.route('/telegram-webhook', methods=['POST'])
def webhook():
    from bot import setup_bot
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()
    setup_bot(application)
    update = Update.de_json(request.get_json(), application.bot)
    application.update_queue.put(update)
    return jsonify({'status': 'ok'})

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or 'username' not in data or 'message' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    if chat_id := get_chat_id(data['username']):
        bot.send_message(chat_id=chat_id, text=data['message'])
        return jsonify({"status": "Message delivered"})
    return jsonify({"error": "Username not found"}), 404

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})