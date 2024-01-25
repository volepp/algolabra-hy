import chess
from board import Board
import random

# Only used for initial UI testing
class RandomEngine:

    def __init__(self):
        self.cheat_board = chess.Board()

    def make_move(self, board):
        """Makes the next move and returns it in SAN format.
        """

        last_move = board.get_last_move()
        if last_move is not None:
            self.cheat_board.push_san(last_move)

        next_move = self.cheat_board.san(self.select_random_move())
        self.cheat_board.push_san(next_move)
        return next_move

    def select_random_move(self):
        legal_moves = self.cheat_board.legal_moves
        self.cheat_board.legal_moves
        rand_inx = random.randint(0, legal_moves.count()-1)

        for i, move in enumerate(legal_moves):
            if i == rand_inx:
                return move