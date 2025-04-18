import unittest
from core.llm import llm

class TestLLMCoreBehavior(unittest.TestCase):

    def test_basic_response(self):
        result = llm.invoke("Say hello in one word")
        self.assertIn("hello", result.lower())

    def test_paragraph_understanding(self):
        prompt = (
            "I'm going to tell you a little story: "
            "Alice went to the market to buy apples. "
            "She saw Bob, who told her oranges were cheaper. "
            "She still bought apples. What did Alice buy?"
        )
        result = llm.invoke(prompt)
        self.assertIn("apple", result.lower())

    def test_does_not_repeat(self):
        prompt = "Say the word banana only once"
        result = llm.invoke(prompt.lower())
        banana_count = result.lower().count("banana")
        self.assertEqual(banana_count, 1)

    def test_logical_reasoning(self):
        prompt = "If A is taller than B, and B is taller than C, who is the tallest?"
        result = llm.invoke(prompt)
        self.assertIn("A", result)

    def test_json_output_structure(self):
        prompt = "Respond with a JSON object: name is Pratham, age is 21"
        result = llm.invoke(prompt)
        self.assertTrue("{" in result and "}" in result and "name" in result)

    def test_gibberish_input(self):
        prompt = "asdkjh#@%$^&*()_+!!"
        result = llm.invoke(prompt)
        self.assertTrue(len(result.strip()) > 0)  # At least don’t crash

