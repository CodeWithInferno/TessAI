import os

def find_folder(target_name, start_path=os.path.expanduser("~"), depth=3):
    """
    Recursively search for a folder up to a max depth.
    Returns the path to the folder if found.
    """
    for root, dirs, files in os.walk(start_path):
        current_depth = root[len(start_path):].count(os.sep)
        if current_depth > depth:
            continue
        for dir in dirs:
            if target_name.lower() in dir.lower():
                return os.path.join(root, dir)
    return None

def trace_find_folder(target_name):
    path = os.path.expanduser("~")
    print(f"🌍 Starting at {path}")
    for root, dirs, _ in os.walk(path):
        print(f"🔍 Checking: {root}")
        for d in dirs:
            if target_name.lower() in d.lower():
                found_path = os.path.join(root, d)
                print(f"✅ Found '{target_name}' at {found_path}")
                return found_path
    print("❌ Folder not found.")
    return None
def smart_find_folder(target_name: str, search_roots: list[str], depth=3):
    for root_path in search_roots:
        if not os.path.exists(root_path):
            continue
        for root, dirs, _ in os.walk(root_path):
            if root[len(root_path):].count(os.sep) > depth:
                continue
            for d in dirs:
                if target_name.lower() in d.lower():
                    return os.path.join(root, d)
    return None
