import os
from telegram import Update
from telegram.ext import ContextTypes
from core.transcription import transcribe_audio
from agents.doctor_gpt import ask_doctor_with_memory
from database.db import store_symptom
from core.session_storage import store_user_input, get_user_session

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)  # 🔒 Always use str for session keys
    user_name = update.effective_user.first_name or "Unknown"
    msg = update.message

    confirmation = (
        "✅ Input received. When you're ready, type /proceed to consult the doctor.\n"
        "✅ इनपुट मिल गया है। जब तैयार हों, /proceed टाइप करें डॉक्टर से बात करने के लिए।"
    )

    # TEXT input
    if msg.text and not msg.text.startswith("/"):
        store_user_input(user_id, "text", msg.text)
        store_symptom(str(user_id), user_name, msg.text)

        session = get_user_session(str(user_id))  # Cast to str if needed

        if session.get("image_path"):
            await msg.reply_text(
                "📝 Symptom noted along with your uploaded photo.\n"
                "📝 आपके द्वारा भेजी गई फोटो के साथ लक्षण नोट कर लिए गए हैं।\n"
                + confirmation
            )
        else:
            await msg.reply_text(
                "📝 Symptom saved.\n(Optional: Send a medical photo if relevant.)\n"
                "📝 लक्षण save कर लिए गए हैं।\n(अगर जरूरी हो तो मेडिकल फोटो भेजें।)\n"
                + confirmation
            )

    # VOICE input
    elif msg.voice:
        voice_path = f"temp_voice_{user_id}.ogg"
        try:
            file = await msg.voice.get_file()
            await file.download_to_drive(voice_path)
            transcript = transcribe_audio(voice_path)
        except Exception as e:
            await msg.reply_text(
                "⚠️ Could not process your voice note. Please try again.\n"
                "⚠️ आपकी आवाज़ समझ नहीं पाई। कृपया फिर से भेजें।"
            )
            print(f"[ERROR] Transcription failed: {e}")
            return

        store_user_input(user_id, "text", transcript)
        store_symptom(str(user_id), user_name, transcript)

        session = get_user_session(user_id)  # 🔁 refresh session after storing
        if session.get("image_path"):
            await msg.reply_text(
                "🎤 Voice note saved with your photo.\n"
                "🎤 आपकी आवाज़ और फोटो दोनों save कर ली गई हैं।\n"
                + confirmation
            )
        else:
            await msg.reply_text(
                "🎤 Voice note saved.\n(Optional: Send a medical photo if relevant.)\n"
                "🎤 आवाज़ save कर ली गई है।\n(अगर जरूरी हो तो मेडिकल फोटो भेजें।)\n"
                + confirmation
            )

    # IMAGE input
    elif msg.photo:
        image_path = f"temp_image_{user_id}.jpg"
        try:
            file = await msg.photo[-1].get_file()
            await file.download_to_drive(image_path)
        except Exception as e:
            await msg.reply_text(
                "⚠️ Could not process the photo. Please try again.\n"
                "⚠️ फोटो समझ नहीं पाई। कृपया फिर से भेजें।"
            )
            print(f"[ERROR] Image download failed: {e}")
            return

        store_user_input(user_id, "image_path", image_path)

        session = get_user_session(user_id)  # 🔁 refresh session after storing
        if session.get("text"):
            await msg.reply_text(
                "🖼️ Photo saved and your symptoms are already noted.\n"
                "🖼️ फोटो save कर ली गई है और आपके लक्षण पहले से नोट हैं।\n"
                + confirmation
            )
        else:
            await msg.reply_text(
                "🖼️ Photo saved.\nPlease also describe your symptoms via voice or text.\nThen type /proceed.\n"
                "🖼️ फोटो save कर ली गई है। कृपया अपने लक्षण आवाज़ या टेक्स्ट में भी बताएं।\nफिर /proceed टाइप करें।"
            )

    else:
        await msg.reply_text(
            "❗ Please send either text, a voice note, or a medical photo describing your issue.\n"
            "❗ कृपया अपनी समस्या बताने के लिए टेक्स्ट, आवाज़ या मेडिकल फोटो भेजें।"
        )
        
    print("📥 handle_message session:", get_user_session(str(user_id)))
