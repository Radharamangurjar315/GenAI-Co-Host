# cohost/tts.py
import pyttsx3, tempfile, os

def tts_save_wav_pyttsx3(text: str):
    if not text or not text.strip():
        return None
    engine = pyttsx3.init()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    engine.save_to_file(text, tmp.name)
    engine.runAndWait()
    return tmp.name
