import unittest
from core.llm import llm

class TestLLM(unittest.TestCase):

    def test_llm_basic_response(self):
        prompt = "Say hi in one word"
        result = llm.invoke(prompt)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result.strip()), 0)
        self.assertIn("hi", result.lower())

    def test_logical_reasoning(self):
        prompt = "If A is taller than B and B is taller than C, who is the tallest?"
        result = llm.invoke(prompt)
        self.assertIn("A", result)

    def test_json_format_output(self):
        prompt = "Respond with a JSON object with keys: name as 'Pratham' and age as 21"
        result = llm.invoke(prompt)
        self.assertIn("name", result.lower())
        self.assertIn("pratham", result.lower())
        self.assertIn("21", result)

    def test_question_answering(self):
        prompt = "Alice bought 3 apples and Bob bought 5. Who bought more apples?"
        result = llm.invoke(prompt)
        self.assertIn("bob", result.lower())

    def test_gibberish_handling(self):
        prompt = "@#$%*&^!()"
        result = llm.invoke(prompt)
        self.assertTrue(len(result.strip()) > 0)  # Should not crash or return empty

    def test_instruction_following(self):
        prompt = "Say the word banana exactly once."
        result = llm.invoke(prompt)
        self.assertEqual(result.lower().count("banana"), 1)
