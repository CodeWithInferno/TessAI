import time
import json
import os
from pynput import keyboard

signature = {
    "key_down_times": {},
    "key_intervals": []
}

capture_text = "the quick brown fox jumps over the lazy dog"
print(f"✍️ Please type this exactly:\n\n\"{capture_text}\"\n\nTyping starts now...")

key_down = {}
prev_key_time = None

def on_press(key):
    try:
        k = key.char
    except AttributeError:
        k = str(key)

    if k not in key_down:
        key_down[k] = time.time()

def on_release(key):
    global prev_key_time

    try:
        k = key.char
    except AttributeError:
        k = str(key)

    down_time = key_down.get(k)
    if down_time:
        duration = time.time() - down_time
        signature["key_down_times"][k] = round(duration, 5)

    now = time.time()
    if prev_key_time:
        interval = now - prev_key_time
        signature["key_intervals"].append(round(interval, 5))
    prev_key_time = now

    if key == keyboard.Key.enter:
        return False

print("⌨️ Press Enter after you're done typing.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Save to file
output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(output_dir, exist_ok=True)
save_path = os.path.join(output_dir, "typing_signature.json")

with open(save_path, "w") as f:
    json.dump(signature, f, indent=2)

print(f"\n✅ Typing signature saved at: {save_path}")
