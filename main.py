from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.command_handlers import start, help_command, history, proceed, reset
from handlers.message_handlers import handle_message
from database.db import init_db
from config import TELEGRAM_BOT_TOKEN

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
init_db()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
# app.add_handler(CommandHandler("history", history))
app.add_handler(CommandHandler("proceed", proceed))
app.add_handler(CommandHandler("reset", reset))

# ✅ This is important — prevents commands from overwriting session
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND | filters.VOICE | filters.PHOTO,
    handle_message
))

if __name__ == "__main__":
    print("🤖 MediBot started")
    app.run_polling()
