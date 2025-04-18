import unittest
from core.memory import summarize_and_store_if_needed
from core.memory import vectorstore

class TestMemory(unittest.TestCase):
    def test_summary_saved(self):
        test_input = "My name is Pratham and I study at Gannon University"
        summarize_and_store_if_needed(test_input)

        results = vectorstore.similarity_search("Pratham", k=1)
        self.assertTrue(any("Pratham" in r.page_content for r in results))
