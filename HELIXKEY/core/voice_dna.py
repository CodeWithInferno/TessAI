import os
import numpy as np
import sounddevice as sd
import librosa
import json

def record_voice(seconds=5, output_dir=None, sr=16000):
    print(f"🎙️ Recording {seconds} seconds of audio... Speak now.")
    print(f"🎙️ Please clearly say:\n\"The quick brown fox jumps over the lazy dog while whispering secrets in a robotic yet emotional tone.\"")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if output_dir is None:
        output_dir = os.path.join(base_dir, "../data/voice_dna")
    os.makedirs(output_dir, exist_ok=True)

    audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()

    wav_file = os.path.join(output_dir, "voice.wav")
    np.save(wav_file.replace(".wav", ".npy"), audio)

    mfcc = librosa.feature.mfcc(y=audio.flatten(), sr=sr, n_mfcc=13)
    mean_mfcc = np.mean(mfcc, axis=1)

    np.save(os.path.join(output_dir, "voice_embedding.npy"), mean_mfcc)
    with open(os.path.join(output_dir, "voice_embedding.txt"), 'w') as f:
        f.write(",".join(map(str, mean_mfcc)))

    print(f"✅ Voice signature saved to {output_dir}")

if __name__ == "__main__":
    record_voice()
