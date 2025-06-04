from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)
from database import add_user, get_username

GET_USERNAME = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = get_username(chat_id)
    
    if username:
        await update.message.reply_text(f"You are already linked with username: {username}")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please enter a unique alphanumeric username:")
        return GET_USERNAME

async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.message.text.strip()
    
    if not username.isalnum():
        await update.message.reply_text("Username must be alphanumeric. Please try again:")
        return GET_USERNAME
    
    if add_user(username, chat_id):
        await update.message.reply_text("✅ Account linked successfully!")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Username already taken. Please try again:")
        return GET_USERNAME

async def myusername(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = get_username(update.effective_chat.id)
    if username:
        await update.message.reply_text(f"Your username: {username}")
    else:
        await update.message.reply_text("No username linked. Send /start to begin.")

def setup_bot(application):
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={GET_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username)]},
        fallbacks=[]
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("myusername", myusername))
