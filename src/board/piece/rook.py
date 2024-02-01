from . import Piece, Color, Move
import numpy as np

class Rook(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color)

    def get_possible_moves(self, board: np.array) -> [Move]:
        possible_moves = []
        possible_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dir in possible_directions:
            possible_moves.extend(self.find_linear_moves(board, dir))

        return possible_moves

    
    def fen_symbol(self):
        if self.color == Color.White:
            return "R"
        return "r"