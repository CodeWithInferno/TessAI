# setup_win.py
import os
import subprocess
import sys
from pathlib import Path

REQUIREMENTS_FILE = "requirements.txt"
DB_FOLDER = Path.home() / "TessAI"
DB_PATH = DB_FOLDER / "File_Dir.db"

def run(command):
    print(f"🔧 Running: {command}")
    subprocess.run(command, shell=True, check=True)

def ensure_python():
    try:
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Python already available.")
    except:
        print("❌ Python is not installed. Please install Python 3.10+ manually from https://www.python.org/downloads/")
        sys.exit(1)

def ensure_pip_packages():
    if not os.path.exists(REQUIREMENTS_FILE):
        print(f"❌ No {REQUIREMENTS_FILE} found.")
        return
    run("python -m pip install --upgrade pip")
    run(f"python -m pip install -r {REQUIREMENTS_FILE}")

def scan_files():
    from core.File_Dir import init_db, scan_and_store_files
    print(f"📁 Scanning and saving to DB at {DB_PATH}")
    conn = init_db()
    scan_and_store_files(str(Path.home()))
    conn.close()
    print("✅ Done scanning and storing file structure.")

if __name__ == "__main__":
    ensure_python()
    ensure_pip_packages()
    scan_files()
