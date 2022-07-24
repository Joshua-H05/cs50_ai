"""
Tic Tac Toe Player
"""
import copy
import math
import pysnooper

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_moves_made = 0
    o_moves_made = 0
    for row in range(3):
        for cell in range(3):
            if board[row][cell] == X:
                x_moves_made += 1
            if board[row][cell] == O:
                o_moves_made += 1

    if x_moves_made == o_moves_made + 1:
        return O
    if x_moves_made == o_moves_made:
        return X
    else:
        return "Someone has made 2 moves in a row! "


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for row in range(3):
        for cell in range(3):
            if board[row][cell] == EMPTY:
                possible_moves.add((row, cell))
    if len(possible_moves) == 0:
        return None
    elif winner(board):
        return None
    else:
        return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    """if action not in actions(board):
        raise Exception("You cannot play there! ")"""
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    victor = None
    for coordinate in range(3):
        if board[coordinate][0] == board[coordinate][1] == board[coordinate][2]:
            victor = board[coordinate][0]
        if board[0][coordinate] == board[1][coordinate] == board[2][coordinate]:
            victor = board[0][coordinate]
    if board[0][0] == board[1][1] == board[2][2]:
        victor = board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        victor = board[0][2]
    return victor


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty_cells = 0
    for row in range(3):
        for cell in range(3):
            if board[row][cell] == EMPTY:
                empty_cells += 1
    if empty_cells == 0:
        return True
    if winner(board):
        return True
    if empty_cells > 0:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    board_value = None
    if winner(board) == X:
        board_value = 1
    if winner(board) == O:
        board_value = -1
    return board_value


def max_value(board):
    possible_moves = []
    v = float("-inf")
    if terminal(board):
        info = (utility(board), None)
        return info
    else:
        for move in actions(board):
            print(type(max(min_value(result(board, move))[0], v)))
            v = max(min_value(result(board, move))[0], v)
            if v is None:
                print("Max")
                break
            possible_moves.append((v, move))
    for move in possible_moves:
        v = float("-inf")
        if move[0] > v:
            v = move[0]
    return v, move[1]


def min_value(board):
    possible_moves = []
    v = float("inf")
    if terminal(board):
        info = (utility(board), None)
        return info
    else:
        for move in actions(board):
            v = min(max_value(result(board, move))[0], v)
            print(type(max_value(result(board, move))[0]))
            if v is None:
                print("min")
                break
            possible_moves.append((v, move))
    for move in possible_moves:
        v = float("inf")
        if move[0] < v:
            v = move[0]
    return v, move[1]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    current_player = player(board)
    if current_player == X:
        optimal_move = max_value(board)[1]
    else:
        optimal_move = min_value(board)[1]
    return optimal_move
