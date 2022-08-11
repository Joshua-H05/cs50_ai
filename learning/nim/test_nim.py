import unittest
from nim import NimAI


class TestNim(unittest.TestCase):
    def setUp(self) -> None:
        self.AI = NimAI(alpha=0.5, epsilon=0.1)
        self.original_state = [1, 3, 5, 7]

    def test_get_q_value(self):
        self.AI.q = {((1, 3, 5, 7), (1, 1)): 1}
        result = self.AI.get_q_value((1, 3, 5, 7), (1, 1))
        self.assertEqual(result, 1)

    def test_get_q_value_unmapped(self):
        self.AI.q = {((1, 3, 5, 7), (1, 1)): None}
        result = self.AI.get_q_value((1, 3, 5, 7), (1, 1))
        self.assertEqual(result, 0)

    def test_choose_action(self):
        print(self.AI.q.keys())
        self.AI.choose_action(self.original_state)


