import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.memory import vectorstore

docs = vectorstore.get()["documents"]
print("\n📂 Current Stored Memory:\n")
for i, doc in enumerate(docs, 1):
    print(f"{i}. {doc}")
