import os
from io import BytesIO
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY
from pydub import AudioSegment
from gtts import gTTS

# Initialize ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def split_text_into_chunks(text, max_chars=250):
    """Split long text into manageable sentence chunks."""
    import re
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_speech(text, output_path="assets/doctor_voice.mp3", voice_id="gHu9GtaHOXcSqFTK06ux", speedup_factor=1.1):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # --- ElevenLabs primary TTS ---
        chunks = split_text_into_chunks(text)
        request_ids = []
        audio_buffers = []

        for chunk in chunks:
            with client.text_to_speech.with_raw_response.convert(
                text=chunk,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                previous_request_ids=request_ids
            ) as response:
                request_id = response._response.headers.get("request-id")
                request_ids.append(request_id)
                request_ids = request_ids[-3:]  # ⬅️ now limit after appending

                audio_data = b''.join(part for part in response.data)
                audio_buffers.append(BytesIO(audio_data))



        combined_audio = BytesIO(b''.join(buf.getvalue() for buf in audio_buffers))

        # Export to file
        audio_segment = AudioSegment.from_file(combined_audio, format="mp3")
        audio_segment.export(output_path, format="mp3")
        return output_path

    except Exception as e:
        print(f"🔴 ElevenLabs TTS generation failed: {e}")
        print("⚠️ Falling back to gTTS...")

        # --- gTTS Fallback ---
        try:
            temp_path = "assets/temp_fallback.mp3"
            tts = gTTS(text=text, lang="hi", slow=False)
            tts.save(temp_path)

            audio = AudioSegment.from_file(temp_path)
            faster_audio = audio.speedup(playback_speed=speedup_factor)
            faster_audio.export(output_path, format="mp3")

            if os.path.exists(temp_path):
                os.remove(temp_path)

            print("✅ gTTS fallback succeeded")
            return output_path

        except Exception as fallback_error:
            print(f"❌ gTTS fallback also failed: {fallback_error}")
            return None
