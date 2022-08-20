import unittest
import questions


class TestQuestions(unittest.TestCase):
    def setUp(self) -> None:
        self.sentence = "Hey, hoW is it going?"

    def test_tokenize(self):
        result = questions.tokenize(self.sentence)
        self.assertEqual(result, ["hey", "going"])
