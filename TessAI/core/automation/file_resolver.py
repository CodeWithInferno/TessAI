import os
import sqlite3
from pathlib import Path

DB_PATH = os.path.join(Path(__file__).parent.parent.parent, "File_Dir.db")

COMMON_SEARCH_DIRS = [
    "~/Documents", "~/Downloads", "~/Desktop", "~/Pictures"
]

def search_file_by_name(name):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT path FROM files WHERE name LIKE ? ORDER BY size DESC LIMIT 5", (f"%{name}%",))
        results = cursor.fetchall()
        conn.close()
        return [r[0] for r in results]
    except Exception:
        return []

def fallback_search(name):
    for base in COMMON_SEARCH_DIRS:
        for root, _, files in os.walk(os.path.expanduser(base)):
            if name in files:
                return os.path.join(root, name)
    return None

def resolve_file_path(name):
    # 1. Check cached DB
    db_results = search_file_by_name(name)
    if db_results:
        return db_results[0]

    # 2. Real-time fallback search
    return fallback_search(name)

