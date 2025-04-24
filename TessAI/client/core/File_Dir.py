import os
import sqlite3
from pathlib import Path


EXCLUDED_DIRS = {
    "node_modules", ".next", ".cache", "__pycache__", ".git", ".venv", "venv", 
    "Library", "Applications", "System", "private", "Volumes", "usr", "bin", "opt", 
    "cores", "dev", "sbin", "etc", "tmp", "var", "Network", "Preboot", "Recovery", "home",
    "$Recycle.Bin", "Program Files", "Program Files (x86)", "Windows", "AppData"
}

USEFUL_EXTENSIONS = {
    ".txt", ".md", ".pdf", ".docx", ".xlsx", ".pptx", ".py", ".js", ".ts", ".json",
    ".html", ".css", ".cpp", ".c", ".java", ".swift", ".sh", ".sql", ".jpg", ".png"
}

HOME_PATH = str(Path.home())
DB_FILE = os.path.join(HOME_PATH, "TessAI", "File_Dir.db")

def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT,
            name TEXT,
            is_dir BOOLEAN,
            extension TEXT,
            size INTEGER
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_path ON files(path)')
    conn.commit()
    return conn

def should_skip_dir(dirname):
    return any(part in EXCLUDED_DIRS for part in Path(dirname).parts)

def scan_and_store_files(base_path=HOME_PATH):
    conn = init_db()
    cursor = conn.cursor()

    for root, dirs, files in os.walk(base_path, topdown=True):
        dirs[:] = [d for d in dirs if not should_skip_dir(os.path.join(root, d))]

        for name in files:
            full_path = os.path.join(root, name)
            try:
                stat = os.stat(full_path)
                ext = os.path.splitext(name)[1].lower()
                if ext in USEFUL_EXTENSIONS:
                    cursor.execute('''
                        INSERT INTO files (path, name, is_dir, extension, size)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (full_path, name, False, ext, stat.st_size))
            except Exception:
                continue

        for name in dirs:
            full_path = os.path.join(root, name)
            if not should_skip_dir(full_path):
                try:
                    cursor.execute('''
                        INSERT INTO files (path, name, is_dir, extension, size)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (full_path, name, True, "", 0))
                except Exception:
                    continue

    conn.commit()
    conn.close()
    print(f"✅ Done. Indexed files stored in {DB_FILE}")
