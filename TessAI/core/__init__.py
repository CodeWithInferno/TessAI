# from .llm import llm
# from .memory import rag_chain, summarize_and_store_if_needed
# from .search import search_and_summarize
# from .automation.terminal import run_in_new_terminal
# from .automation.command_planner import extract_commands
# from .automation.explorer import smart_find_folder
# from .automation.locator import guess_search_locations
# from tests import test_boot
# import time, os
# from tqdm import tqdm
# from .automation.query_parser import extract_folder_name


# class TessCore:
#     def run_boot_diagnostics(self):
#         print("🚀 Running system checks...\n")
#         checks = [
#             # Removed broken test_llm_response
#             ("Testing memory quality...", test_boot.test_memory_summary_filter),
#         ]

#         for i, (desc, func) in enumerate(checks):
#             time.sleep(0.4)
#             tqdm.write(f"[{'#' * ((i+1)*3)}{'-' * (10 - (i+1)*3)}] {int((i+1)/len(checks)*100)}% {desc}", end=' ')
#             passed = func()
#             tqdm.write("✔ PASS" if passed else "❌ FAIL")

#         print("\n✅ All tests passed.\n")
#         print("(Launching Tess in 2 seconds...)")
#         time.sleep(2)
#         os.system("clear")

#     rag_chain = rag_chain
#     summarize_and_store_if_needed = summarize_and_store_if_needed
#     search_and_summarize = staticmethod(search_and_summarize)
#     extract_commands = staticmethod(extract_commands)
#     run_in_new_terminal = staticmethod(run_in_new_terminal)
#     guess_search_locations = staticmethod(guess_search_locations)
#     smart_find_folder = staticmethod(smart_find_folder)
#     extract_folder_name = staticmethod(extract_folder_name)


# Tess = TessCore()








from .llm import llm
from .memory import rag_chain, summarize_and_store_if_needed
from .search import search_and_summarize
from .automation.terminal import run_in_new_terminal
from .automation.command_planner import extract_commands
from .automation.explorer import smart_find_folder
from .automation.locator import guess_search_locations
from .automation.query_parser import extract_folder_name
from .automation.terminal import run_in_shared_terminal
from .automation.file_resolver import resolve_file_path
from .automation.executor import run_with_retry_and_reflection




class TessCore:
    def run_boot_diagnostics(self):
        print("🧠 Skipping system tests. Starting immediately...\n")

    rag_chain = rag_chain
    @staticmethod
    def summarize_and_store_if_needed(message: str):
        return summarize_and_store_if_needed(message)
    search_and_summarize = staticmethod(search_and_summarize)
    extract_commands = staticmethod(extract_commands)
    run_in_terminal = staticmethod(run_in_shared_terminal)  # ✅ fixed here
    guess_search_locations = staticmethod(guess_search_locations)
    smart_find_folder = staticmethod(smart_find_folder)
    extract_folder_name = staticmethod(extract_folder_name)
    resolve_file_path = staticmethod(resolve_file_path)
    run_with_retry = staticmethod(run_with_retry_and_reflection)


Tess = TessCore()
