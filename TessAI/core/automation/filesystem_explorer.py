import os
import subprocess
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

CHROMA_DIR = "fs_memory"
embedding = OllamaEmbeddings(model="llama3.2")
vectorstore = Chroma(embedding_function=embedding, persist_directory=CHROMA_DIR)


def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return result.stdout.decode("utf-8").strip()
    except Exception as e:
        return f"ERROR: {e}"


def explore_path(path):
    """
    Explore a directory path using 'ls' and log its contents into ChromaDB.
    """
    if not os.path.exists(path):
        return f"❌ Path does not exist: {path}"

    contents = run_command(f"ls -a '{path}'")
    if contents.startswith("ERROR"):
        return contents

    # Format and store in vector memory
    content_list = contents.splitlines()
    filtered = [c for c in content_list if c not in ['.', '..']]
    formatted = f"Directory: {path}\nContents: {', '.join(filtered)}"
    
    # Avoid duplicates
    existing = vectorstore.similarity_search(formatted, k=1)
    if not existing or formatted not in [doc.page_content for doc in existing]:
        vectorstore.add_texts([formatted])

    return f"📁 Explored: {path}\n{formatted}"


def smart_explore(start_path="~"):
    """
    Walk down into folders using human-like reasoning.
    """
    abs_path = os.path.expanduser(start_path)
    stack = [abs_path]

    visited = set()

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        output = explore_path(current)
        print(output)

        try:
            items = os.listdir(current)
            for item in items:
                full = os.path.join(current, item)
                if os.path.isdir(full):
                    stack.append(full)
        except Exception:
            continue
