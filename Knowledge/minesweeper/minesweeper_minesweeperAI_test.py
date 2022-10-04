import unittest
from minesweeper import MinesweeperAI


class TestMineSweeperAI(unittest.TestCase):
    def setUp(self):
        self.msai = MinesweeperAI(height=8, width=8)

    def test_add_knowledge_moves_made(self):
        self.msai.add_knowledge(cell=(1, 1), count=1)
        self.assertEqual(self.msai.moves_made, {(1, 1)})

    def test_add_knowledge_add_safes(self):
        self.msai.add_knowledge(cell=(1, 1), count=1)
        self.assertEqual(self.msai.safes, {(1, 1)})

    def test_add_knowledge_unidentified_neighbors(self):
        self.msai.knowledge = []
        self.msai.add_knowledge(cell=(1, 1), count=3)
        self.assertEqual(self.msai.knowledge, [[{(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}, 3]])

    def test_add_knowledge_unidentified_neighbors_clean_sentence(self):
        self.msai.mines.add((1, 2))
        self.msai.mines.add((0, 0))
        self.msai.safes.add((2, 2))
        self.msai.add_knowledge(cell=(1, 1), count=3)
        self.assertEqual(self.msai.knowledge, [[{(0, 1), (0, 2), (1, 0), (2, 0), (2, 1)}, 1]])

    def test_add_knowledge_add_safes_inference(self):
        self.msai.safes.clear()
        self.msai.knowledge = [[{(0, 0), (1, 2)}, 0]]
        self.msai.add_knowledge(cell=(1, 1), count=1)
        self.assertEqual(self.msai.safes, {(0, 0), (1, 2), (1, 1)})

    def test_add_knowledge_add_mines(self):
        self.msai.knowledge = [[{(0, 0), (1, 2)}, 2]]
        self.msai.add_knowledge(cell=(1, 1), count=0)
        self.assertEqual(self.msai.mines, {(0, 0), (1, 2)})

    def test_add_knowledge_add_nothing_mines(self):
        self.msai.knowledge = [[{(0, 0), (1, 2)}, 1]]
        self.msai.add_knowledge(cell=(1, 1), count=0)
        self.assertEqual(self.msai.mines, set())

    def test_add_knowledge_make_inference(self):
        self.msai.knowledge.append(({(0, 0), (0, 1), (0, 2), (0, 3)}, 2))
        self.msai.knowledge.append(({(0, 0), (0, 1)}, 1))
        self.msai.add_knowledge(count=2, cell=(6, 6))
        self.assertIn([{(0, 2), (0, 3)}, 1], self.msai.knowledge)

    def test_make_safe_move_no_safe_move(self):
        self.msai.knowledge.append(({(0, 0), (1, 2)}, 1))
        safe_move = self.msai.make_safe_move()
        self.assertEqual(safe_move, None)

    def test_make_safe_move_safe_move_possible(self):
        self.msai.knowledge.append(({(0, 0), (1, 2)}, 0))
        self.msai.add_knowledge(cell=(1, 0), count=1)
        safe_move = self.msai.make_safe_move()
        self.assertIn(safe_move, [(0, 0), (1, 2)])

    def test_make_random_move(self):
        self.msai.moves_made.add((0, 0))
        self.msai.moves_made.add((1, 1))
        self.msai.mines.add((5, 1))
        self.msai.mines.add((6, 2))
        random_move = self.msai.make_random_move()
        self.assertNotIn(random_move, ((0, 0), (1, 1), (5, 1), (6, 2)))

    def test_cell_sentence_removed(self):
        self.msai.mines = {(1, 1)}
        result = self.msai.cell_sentence(cell=(1, 0), count=2)
        self.assertNotIn((1, 1), result)
        
    def test_cell_sentence_len(self):
        self.msai.mines = {(1, 1)}
        self.msai.safes = {(0, 0), (2, 0)}
        result = self.msai.cell_sentence(cell=(1, 0), count=2)
        self.assertEqual(len(result[0]), 2)

    def test_cell_sentence_count(self):
        self.msai.mines = {(1, 1)}
        result = self.msai.cell_sentence(cell=(1, 0), count=2)
        self.assertEqual(result[1], 1)


