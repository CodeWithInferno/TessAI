from core.runner import extract_run_command, run_in_terminal
import os
import platform
import sqlite3
import requests
from pathlib import Path
from uuid import uuid4

# Constants

SERVER_URL = "https://selections-minority-nightlife-safer.trycloudflare.com"
UPLOAD_ENDPOINT = f"{SERVER_URL}/upload-files"
CHAT_ENDPOINT = f"{SERVER_URL}/chat"
IS_WINDOWS = platform.system() == "Windows"
HOME_PATH = str(Path.home())
DB_FILE = os.path.join(HOME_PATH, "TessAI", "File_Dir.db")
DEVICE_ID_FILE = os.path.join(HOME_PATH, "TessAI", "device_id.txt")

# Generate or Load Device ID
def get_device_id():
    if os.path.exists(DEVICE_ID_FILE):
        with open(DEVICE_ID_FILE, "r") as f:
            return f.read().strip()
    else:
        device_id = f"{platform.system()}_{platform.node()}_{uuid4().hex[:8]}"
        with open(DEVICE_ID_FILE, "w") as f:
            f.write(device_id)
        return device_id

DEVICE_ID = get_device_id()

# === TEMPORARILY DISABLED ===
def upload_file_data():
    print("📦 Uploading file data to server...")
    return True
    """
    if not os.path.exists(DB_FILE):
        print(f"❌ Local file DB not found at {DB_FILE}")
        return False

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT path, name, is_dir, extension, size FROM files")
    rows = cursor.fetchall()
    conn.close()

    payload = [
        {
            "device_id": DEVICE_ID,
            "path": row[0],
            "name": row[1],
            "is_dir": bool(row[2]),
            "extension": row[3],
            "size": row[4],
        }
        for row in rows
    ]

    try:
        print(f"📡 Uploading {len(payload)} entries from {DEVICE_ID}...")
        res = requests.post(UPLOAD_ENDPOINT, json=payload)
        res.raise_for_status()
        print("✅ Upload complete.")
        return True
    except Exception as e:
        print("❌ Upload failed:", e)
        return False
    """

def chat_loop():
    print("💬 Enter your message (type 'exit' to quit):")
    while True:
        msg = input("You: ").strip()
        if msg.lower() == "exit":
            print("👋 Exiting.")
            break

        try:
            res = requests.post(CHAT_ENDPOINT, json={"query": msg, "device_id": DEVICE_ID})
            if res.status_code == 200:
                raw = res.json().get("response", "")
                cmd = extract_run_command(raw)

                if cmd:
                    print(f"⚙️ Running command: {cmd}")
                    run_in_terminal(cmd)
                else:
                    print("Tess:", raw.strip())
            else:
                print("❌ Error:", res.status_code, res.text)

        except Exception as e:
            print("❌ Connection failed:", e)

if __name__ == "__main__":
    print("🧠 Tess Terminal Client Starting...")
    uploaded = upload_file_data()
    if uploaded:
        print("🚀 Connected to Tess AI. Starting chat...")
        chat_loop()
    else:
        print("⚠️ Skipping file upload. Starting chat anyway...")
        chat_loop()





