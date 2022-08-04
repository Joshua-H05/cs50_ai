import unittest
import generate
import crossword


class TestCrossWordCreator(unittest.TestCase):
    def setUp(self) -> None:
        self.crossword = crossword.Crossword("data/structure0.txt", "data/words0.txt")
        self.crossword_creator = generate.CrosswordCreator(self.crossword)

    def test_enforce_node_consistency(self):
        self.crossword_creator.enforce_node_consistency()