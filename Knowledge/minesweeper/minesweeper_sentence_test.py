import unittest
from minesweeper import Sentence


class TestSentence(unittest.TestCase):
    def setUp(self):
        pass

    def test_known_mines_certain(self):
        self.cells = {(1, 1), (2, 3), (6, 8)}
        self.count = 3
        mines = Sentence.known_mines(self)
        self.assertEqual(mines, {(1, 1), (2, 3), (6, 8)})

    def test_known_mines_uncertain(self):
        self.cells = {(1, 1), (2, 3), (6, 8)}
        self.count = 2
        mines = Sentence.known_mines(self)
        self.assertEqual(mines, None)

    def test_known_safes_certain(self):
        self.cells = {(1, 1), (2, 3), (6, 8)}
        self.count = 0
        safes = Sentence.known_safes(self)
        self.assertEqual(safes, {(1, 1), (2, 3), (6, 8)})

    def test_known_safes_uncertain(self):
        self.cells = {(1, 1), (2, 3), (6, 8)}
        self.count = 1
        safes = Sentence.known_safes(self)
        self.assertEqual(safes, None)

    cell = (1, 1)

    def test_mark_mine_cell_is_mine(self):
        pass

    def test_mark_mine_cell_is_not_mine(self):
        pass

    def test_mark_safe_cell_is_safe(self):
        pass

    def test_mark_safe_cell_is_not_safe(self):
        pass
