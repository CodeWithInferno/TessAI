# server/core/__init__.py

from .llm import llm
from .memory import rag_chain, summarize_and_store_if_needed
from .filesystem_manager import FileMemory


class TessCore:
    def run_boot_diagnostics(self):
        print("🧠 Tess server is ready.\n")

    rag_chain = rag_chain

    @staticmethod
    def summarize_and_store_if_needed(message: str):
        return summarize_and_store_if_needed(message)


Tess = TessCore()
