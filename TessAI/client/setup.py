# setup.py
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

def ensure_homebrew():
    try:
        subprocess.run(["brew", "--version"], check=True, stdout=subprocess.DEVNULL)
        print("✅ Homebrew already installed.")
    except:
        print("📦 Installing Homebrew...")
        run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')

def ensure_python():
    try:
        subprocess.run(["python3", "--version"], check=True)
        print("✅ Python3 already available.")
    except:
        print("📦 Installing Python via Homebrew...")
        run("brew install python")

def ensure_pip_packages():
    if not os.path.exists(REQUIREMENTS_FILE):
        print(f"❌ No {REQUIREMENTS_FILE} found.")
        return
    run("python3 -m pip install --upgrade pip")
    run(f"python3 -m pip install -r {REQUIREMENTS_FILE}")

def scan_files():
    from core.File_Dir import init_db, scan_and_store_files
    print(f"📁 Scanning and saving to DB at {DB_PATH}")
    conn = init_db()
    scan_and_store_files(str(Path.home()))
    conn.close()
    print("✅ Done scanning and storing file structure.")

if __name__ == "__main__":
    ensure_homebrew()
    ensure_python()
    ensure_pip_packages()
    scan_files()
