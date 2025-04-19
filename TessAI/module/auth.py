from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import os
from time import sleep
from scipy.spatial.distance import cosine

BASE_PATH = Path(__file__).parent / ".." / "voice_profiles"
BASE_PATH.mkdir(exist_ok=True)

encoder = VoiceEncoder()


def record_sample(duration=4, fs=16000):
    print(f"🎤 Recording for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    return np.squeeze(audio)


def enroll_user(name: str):
    print(f"🔐 Enrolling voice profile for '{name}'...")
    audio = record_sample()
    wav_path = BASE_PATH / f"{name}.wav"
    wav.write(wav_path, 16000, audio.astype(np.float32))

    wav_data = preprocess_wav(wav_path)
    embed = encoder.embed_utterance(wav_data)
    np.save(BASE_PATH / f"{name}.npy", embed)
    print("✅ Enrollment complete.")


def verify_speaker(threshold=0.75):
    print("🧠 Verifying speaker...")
    recorded = record_sample()
    temp_path = BASE_PATH / "_temp.wav"
    wav.write(temp_path, 16000, recorded.astype(np.float32))

    wav_data = preprocess_wav(temp_path)
    new_embed = encoder.embed_utterance(wav_data)

    # Load all known voiceprints
    for file in BASE_PATH.glob("*.npy"):
        enrolled = np.load(file)
        similarity = 1 - cosine(new_embed, enrolled)
        print(f"🔍 Comparing to {file.stem} → Similarity: {similarity:.2f}")
        if similarity > threshold:
            print(f"✅ Speaker verified as {file.stem}")
            return True

    print("❌ Speaker not recognized.")
    return False


if __name__ == "__main__":
    print("1. Enroll new voice")
    print("2. Verify speaker")
    choice = input("Select option: ").strip()

    if choice == "1":
        name = input("Enter your name: ").strip()
        enroll_user(name)
    elif choice == "2":
        verify_speaker()