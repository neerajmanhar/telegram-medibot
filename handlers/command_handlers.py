from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import get_last_symptom
from core.session_storage import get_user_session, clear_user_session, append_to_memory, get_user_memory
from agents.doctor_gpt import ask_doctor_with_memory
from core.text_to_speech import generate_speech
import asyncio

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to MediBot!  आपका स्वागत है MediBot में!\n\n"
        "🩺 I can give you some home remedies and medical advice according to your symptoms.\n"
        "🩺 मैं आपकी स्वास्थ्य समस्याओं को समझकर घरेलू उपाय और दवाइयों की सलाह देती हूँ।\n\n"
        "🔘 Choose an action (कोई एक विकल्प चुनें):\n\n"
        "/proceed – Get medical advice (स्वास्थ्य सलाह लें)\n"
        "/reset – Clear previous inputs (पिछला इनपुट हटाएं)\n"
        # "/history – Show your last submitted symptom (आखिरी लक्षण देखें)\n"
        "/help – Get help (मदद प्राप्त करें)\n\n"
        "🎤 YOU CAN NOW START TALKING TO ME IN VOICE OR TEXT, AND I WILL TRY TO HELP YOU.\n"
        "🎤 अब आप मुझसे वॉइस या टेक्स्ट में बात कर सकते हैं, और मैं आपकी मदद करने की कोशिश करूंगी।",
        reply_markup=ReplyKeyboardMarkup(
            [['/proceed', '/reset'], ['/help']],
            resize_keyboard=True
        )
    )

# --- Help Command ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🩺 Please describe your symptoms in voice or text. I will try to help you.\n"
        "🩺 कृपया अपने लक्षण वॉइस या टेक्स्ट में बताएं। मैं आपकी मदद करूंगी।"
    )

# --- History Command ---
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    symptom = get_last_symptom(telegram_id)
    if symptom:
        await update.message.reply_text(f"📌 Last symptom you shared: {symptom}")
    else:
        await update.message.reply_text("❗ अभी तक कोई लक्षण नहीं मिला है।\n❗ No symptom found yet.")

# --- Proceed Command ---
async def proceed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    query = session.get("text")
    image_path = session.get("image_path")

    if not query:
        await update.message.reply_text(
            "❗ You have not sent any information yet. Please describe your symptoms in voice or text and then tap on /proceed.\n"
            "❗ आपने अभी तक कोई जानकारी नहीं भेजी है। कृपया अपने लक्षण वॉइस या टेक्स्ट में बताएं और फिर /proceed दबाएं।"
        )
        return

    memory = get_user_memory(user_id)

    # Send animated loading message
    loading_msg = await update.message.reply_text("⏳ Processing.💬")
    await asyncio.sleep(0.5)
    await loading_msg.edit_text("⏳ Processing..🩺")
    await asyncio.sleep(0.5)
    await loading_msg.edit_text("⏳ Processing...🤖")

    # Get LLM response
    if image_path:
        reply = ask_doctor_with_memory(query=query, image_path=image_path, memory=memory)
    else:
        reply = ask_doctor_with_memory(query=query, memory=memory)

    append_to_memory(user_id, query, reply)

    # Send reply text
    await loading_msg.edit_text(reply)

    # Notify about audio generation
    voice_loading_msg = await update.message.reply_text("🔈 Generating voice response, please wait...")

    # Generate speech in background thread
    audio_path = await asyncio.to_thread(generate_speech, reply)

    # Send voice message
    await update.message.reply_voice(voice=open(audio_path, "rb"))

    # Remove loading message for audio
    await voice_loading_msg.delete()

    # Clear session
    session.pop("text", None)
    session.pop("image_path", None)

    print("🚀 /proceed session debug:", session)


# --- Reset Command ---
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    clear_user_session(user_id)
    await update.message.reply_text("🧹 Memory has been cleared. You can start again.\n🧹 मेमोरी साफ़ कर दी गई है। अब आप फिर से शुरू कर सकते हैं।")
