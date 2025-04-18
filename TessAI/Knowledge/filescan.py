import os
import sqlite3
from pathlib import Path

# SQLite database file
DB_FILE = "/Users/pratham/Documents/Tess/TessAI/File_Dir.db"

# Exclude folders commonly known to be large or irrelevant
EXCLUDED_DIRS = {
    "node_modules", ".next", ".cache", "__pycache__", ".git", ".venv", "venv", 
    "Library", "Applications", "System", "private", "Volumes", "usr", "bin", "opt", 
    "cores", "dev", "sbin", "etc", "tmp", "var", "Network", "Preboot", "Recovery", "home"
}

# File extensions considered "useful"
USEFUL_EXTENSIONS = {
    ".txt", ".md", ".pdf", ".docx", ".xlsx", ".pptx", ".py", ".js", ".ts", ".json",
    ".html", ".css", ".cpp", ".c", ".java", ".swift", ".sh", ".sql", ".jpg", ".png"
}

# Initialize DB
def init_db():
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

# Decide whether to skip a directory based on its name
def should_skip_dir(dirname):
    return any(part in EXCLUDED_DIRS for part in Path(dirname).parts)

# Scan filesystem from user's home directory
def scan_and_store_files(base_path, conn):
    cursor = conn.cursor()
    for root, dirs, files in os.walk(base_path, topdown=True):
        # Remove excluded directories in-place to skip walking them
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
                continue  # ignore files we can't stat

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

# Run the scan
home_path = str(Path.home())
conn = init_db()
scan_and_store_files(home_path, conn)
conn.close()
