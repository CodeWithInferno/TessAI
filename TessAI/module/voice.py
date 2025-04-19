import speech_recognition as sr
import pyttsx3
import platform
import argparse
import tempfile
import numpy as np
import scipy.io.wavfile as wavfile

# Toggle speaker verification
VOICE_AUTH_ENABLED = False  # set to True to require voice match

if VOICE_AUTH_ENABLED:
    from module.auth import verify_speaker

# Parse command-line flag (used by app.py)
parser = argparse.ArgumentParser()
parser.add_argument("--no-voice", action="store_true", help="Disable all voice features")
args, _ = parser.parse_known_args()
mute_mode = args.no_voice

# 🎙️ Setup TTS
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

# Try to set a female voice
for voice in engine.getProperty('voices'):
    if "female" in voice.name.lower() or "samantha" in voice.name.lower() or "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# 🔊 Speak (if not muted)
def speak(text):
    print(f"Tess: {text}")
    if not mute_mode:
        engine.say(text)
        engine.runAndWait()

# 🎤 Listen and optionally verify speaker
def listen():
    if mute_mode:
        return input("You (typed): ").strip()

    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 1.2

    while True:
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                audio = r.listen(source)

                if VOICE_AUTH_ENABLED:
                    print("🧠 Verifying speaker...")
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                    wavfile.write(temp_file.name, 16000, np.frombuffer(audio.get_raw_data(), dtype=np.int16))

                    if not verify_speaker(threshold=0.75):
                        print("❌ Unauthorized speaker.")
                        speak("Sorry, I don't recognize you.")
                        continue

                    print("✅ Authorized.")

                print("🧠 Transcribing...")
                return r.recognize_google(audio)

        except Exception as e:
            print(f"(STT failed: {e})")
            return input("You (typed): ").strip()
