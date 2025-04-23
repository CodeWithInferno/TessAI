import sqlite3
import os

# Absolute or relative from project root
DB_PATH = "server/server_data/rag_memory_ds/chroma.sqlite3"

# Ensure DB exists
if not os.path.exists(DB_PATH):
    print(f"❌ Vector memory DB not found at: {DB_PATH}")
    exit()

# Connect and fetch memory entries
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# List tables for verification
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("📂 Tables in DB:", [t[0] for t in tables])

# Check for expected structure
if "collections" not in [t[0] for t in tables] or "documents" not in [t[0] for t in tables]:
    print("❌ Required tables ('collections', 'documents') not found.")
    conn.close()
    exit()

# Fetch first 5 stored documents
print("\n🧠 First 5 memory entries:\n")
try:
    cursor.execute("""
        SELECT d.cmetadata, d.cdocument
        FROM documents d
        JOIN collections c ON d.collection_id = c.id
        LIMIT 5
    """)
    rows = cursor.fetchall()

    for i, (metadata, content) in enumerate(rows, 1):
        print(f"{i}. {content}")
        print(f"   Metadata: {metadata}")
        print("-" * 40)

except Exception as e:
    print("❌ Error reading memory:", str(e))

conn.close()
