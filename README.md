# 🤖 MediBot — AI-Powered Telegram Healthcare Assistant

**MediBot** is a multilingual multimodal AI Telegram bot designed to help users receive preliminary healthcare assistance via natural language, image, and voice inputs — all anonymously and privately within Telegram.

🔗 Try it live: [t.me/neerajmanhar_medibot](https://t.me/neerajmanhar_medibot)

---

## 🚀 Features

- 💬 **Natural language symptom checking**
- 🖼️ **Image-based analysis** (e.g., rashes, wounds)
- 🎤 **Voice message support** with transcription
- 🧠 **LLM-powered doctor agent** for AI-generated responses
- 🔐 **Anonymous & Secure**: No cloud-based user data storage
- 🗃️ **Local chat history** (optional for user session continuity)

---

## 🛠️ Tech Stack

- **Python**
- **Telegram Bot API** via `python-telegram-bot`
- **OpenAI GPT-4.1** for doctor agent
- **ElevenLabs / gTTS** for voice output
- **SQLite + SQLAlchemy** for session data
- **Pydub**, **SpeechRecognition**, **Tavily**, **Google Places API**
- **Hosted on AWS EC2**, deployed via GitHub Actions

---

## ⚙️ How to Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/neerajmanhar/telegram-medibot.git
cd telegram-medibot
````

### 2. Set Up Environment

Create a `.env` file in the root directory:

```dotenv
OPENAI_API_KEY=your_openai_key
TELEGRAM_BOT_TOKEN=your_bot_token
ELEVENLABS_API_KEY=your_elevenlabs_key
```

### 3. Install Dependencies

Make a virtual environment and install packages:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the Bot

```bash
python main.py
```

---

## 📁 Project Structure

```
telegram-medibot/
├── agents/                # LLM doctor agent
├── assets/                # Voice output files
├── core/                  # TTS, transcription, vision analysis
├── database/              # SQLite models and session DB
├── handlers/              # Telegram command and message handlers
├── main.py                # Bot entry point
├── .env                   # API keys (excluded from Git)
├── requirements.txt
└── .github/workflows/     # CI/CD workflow for auto-deploy
```

---

## 📦 Deployment (CI/CD)

This project includes a GitHub Actions workflow to:

* SSH into AWS EC2
* Pull latest code
* Install dependencies
* Restart the bot

🛠️ Deployment auto-triggers on push to `main`.

---

## 🧪 Demo / Sample Inputs

* Ask: "I have chest pain and breathlessness, what could it be?" (You can put **Hindi** or **Hinglish** message too!!.)
* Send voice: "Can you suggest some medicine for nausea?"
* Upload image: "Is this burn mark serious?"

---

## 🤝 Credits

Created by **[Neeraj Manhar](https://github.com/neerajmanhar)** as a real-world AI assistant project focused on accessibility and privacy.

- 🌐 [LinkedIn](https://www.linkedin.com/in/neerajmanhar/)
- 📧 nmanhar2002@gmail.com


## 🛡️ Disclaimer

MediBot is **not a substitute for professional medical advice**. Always consult a licensed healthcare provider for diagnosis and treatment.


