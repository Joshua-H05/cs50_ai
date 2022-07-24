import unittest
import tictactoe

X = "X"
O = "O"
EMPTY = None


class TicTacToeTest(unittest.TestCase):
    def setUp(self):
        self.empty_board = [[EMPTY, EMPTY, EMPTY],
                            [EMPTY, EMPTY, EMPTY],
                            [EMPTY, EMPTY, EMPTY]]
        self.o_turn = [[EMPTY, X, EMPTY],
                       [EMPTY, EMPTY, EMPTY],
                       [EMPTY, EMPTY, EMPTY]]
        self.error_board = [[X, X, EMPTY],
                            [EMPTY, EMPTY, EMPTY],
                            [EMPTY, EMPTY, EMPTY]]
        self.two_possible_actions = [[EMPTY, X, X],
                                     [O, O, X],
                                     [O, X, EMPTY]]
        self.draw = [[X, X, O],
                     [O, O, X],
                     [X, O, X]]
        self.action = (1, 1)
        self.x_wins = [[X, O, O],
                       [EMPTY, X, EMPTY],
                       [X, O, X]]
        self.o_wins = [[O, O, O],
                       [O, X, X],
                       [X, EMPTY, X]]

    """def test_player_x(self):
        player = tictactoe.player(self.empty_board)
        self.assertEqual(player, "X")

    def test_player_o(self):
        player = tictactoe.player(self.o_turn)
        self.assertEqual(player, "O")

    def test_player_error(self):
        player = tictactoe.player(self.error_board)
        self.assertEqual(player, "Someone has made 2 moves in a row! ")

    def test_actions(self):
        actions = tictactoe.actions(self.two_possible_actions)
        self.assertIn((2, 2), actions)
        self.assertIn((0, 0), actions)

    def test_no_more_actions(self):
        actions = tictactoe.actions(self.draw)
        self.assertEqual(actions, None)

    def test_action_x(self):
        result = tictactoe.result(self.empty_board, self.action)
        self.assertEqual(result, [[EMPTY, EMPTY, EMPTY],
                                  [EMPTY, X, EMPTY],
                                  [EMPTY, EMPTY, EMPTY]])

    def test_action_o(self):
        result = tictactoe.result(self.o_turn, self.action)
        self.assertEqual(result, [[EMPTY, X, EMPTY],
                                  [EMPTY, O, EMPTY],
                                  [EMPTY, EMPTY, EMPTY]])

    def test_winner_x(self):
        winner = tictactoe.winner(self.x_wins)
        self.assertEqual(winner, X)

    def test_winner_y(self):
        winner = tictactoe.winner(self.o_wins)
        self.assertEqual(winner, O)

    def test_winner_draw(self):
        winner = tictactoe.winner(self.draw)
        self.assertEqual(winner, None)

    def test_terminal_full_board(self):
        state = tictactoe.terminal(self.draw)
        self.assertEqual(state, True)

    def test_terminal_empty_board(self):
        state = tictactoe.terminal(self.empty_board)
        self.assertEqual(state, False)

    def test_utility_x_wins(self):
        value = tictactoe.utility(self.x_wins)
        self.assertEqual(value, 1)

    def test_utility_o_wins(self):
        value = tictactoe.utility(self.o_wins)
        self.assertEqual(value, -1)

    def test_utility_draw(self):
        value = tictactoe.utility(self.draw)
        self.assertEqual(value, None)"""

    def test_minimum_value(self):
        value = tictactoe.min_value(self.two_possible_actions)[0]
        self.assertEqual(value, -1)
        print(tictactoe.min_value(self.two_possible_actions))

    def test_maximum_value(self):
        value = tictactoe.max_value(self.two_possible_actions)[0]
        self.assertEqual(value, 1)
        print(f"{tictactoe.max_value(self.two_possible_actions)}")
"""
    def test_minimum_value_move(self):
        move = tictactoe.min_value(self.two_possible_actions)[1]
        self.assertEqual(move, (0, 0))

    def test_maximum_value_move(self):
        move = tictactoe.max_value(self.two_possible_actions)[1]
        self.assertEqual(move, (2, 2))

    def test_minimax(self):
        optimal_move = tictactoe.minimax(self.two_possible_actions)
        self.assertEqual(optimal_move, (0, 0))
        print(optimal_move)
"""

if __name__ == "__main__":
    unittest.main()
