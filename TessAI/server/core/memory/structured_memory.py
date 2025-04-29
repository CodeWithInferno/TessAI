import sqlite3
import os

DB_PATH = "server_data/file_memory.db"

def create_structured_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS structured_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            detail TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_fact(category, detail):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO structured_memory (category, detail) VALUES (?, ?)', (category, detail))
    conn.commit()
    conn.close()

def get_all_facts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT category, detail FROM structured_memory')
    facts = c.fetchall()
    conn.close()
    return facts
