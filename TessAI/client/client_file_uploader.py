import os
import platform
import sqlite3
import requests
from pathlib import Path
from uuid import getnode as get_mac

# Constants
SERVER_URL = "https://confused-fwd-rare-treasurer.trycloudflare.com/upload-files"  # Update if changed
IS_WINDOWS = platform.system() == "Windows"
HOME_PATH = str(Path.home())
DB_FILE = os.path.join(HOME_PATH, "TessAI", "File_Dir.db")

# Device identifier (you can customize this more)
DEVICE_ID = f"{platform.system()}_{platform.node()}_{hex(get_mac())[-4:]}"

# Send file metadata to server
def upload_file_data():
    if not os.path.exists(DB_FILE):
        print(f"❌ Local file DB not found at {DB_FILE}")
        return

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
        res = requests.post(SERVER_URL, json=payload)
        res.raise_for_status()
        print("✅ Upload complete.")
    except Exception as e:
        print("❌ Upload failed:", e)

if __name__ == "__main__":
    upload_file_data()
