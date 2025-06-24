from openai import OpenAI
from config import OPENAI_API_KEY
import os
import json
from groq import Groq

client = OpenAI(api_key=OPENAI_API_KEY)

def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
            
        )
    return transcript.text
