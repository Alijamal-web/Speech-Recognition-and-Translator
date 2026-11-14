import sounddevice as sd
import asyncio
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator


def trans_recording(lang):
    duration = 10  # секунды записи
    sample_rate = 44100
    
    print("Speak...")
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    wav.write("output.wav", sample_rate, recording)
    
    print("Record completed, now recognize...")
    recognizer = sr.Recognizer()
    
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio, language=lang)
    except sr.UnknownValueError:
        text = "Speech could not be recognized."
    except sr.RequestError as e:
        text = f"Ошибка сервиса: {e}"
    
    return text


async def translate(text, lang):
    translator = Translator()
    translated = await translator.translate(text, dest=lang)
    return translated.text



lang = input("Enter the language code for translation (e.g. 'ru' - Russian, 'es' - Spanish):")


recognized_text = trans_recording('en-EN')
print("recognized text:", recognized_text)

translated_text = asyncio.run(translate(recognized_text, lang))
print("Translation:", translated_text)
