from engine import Engine
from board import Board
from board.piece import Move
import random

# Only used for initial UI testing
class RandomEngine(Engine):

    def __init__(self):
        # self.cheat_board = chess.Board()
        pass

    def make_move(self, board: Board) -> Move:
        """ Returns the next move.
        """
        return self.select_random_move(board)

    def select_random_move(self, board: Board) -> Move:
        legal_moves = board.get_legal_moves(board.next_move_color()) # self.cheat_board.legal_moves
        print("legal:", legal_moves)
        return random.choice(legal_moves)