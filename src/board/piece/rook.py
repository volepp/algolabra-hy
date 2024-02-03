from . import Piece, Color, Move
import numpy as np

class Rook(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color)

    def calculate_controlled_squares(self, board: np.array):
        self.controlled_squares = []
        possible_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dir in possible_directions:
            self.controlled_squares.extend(self.find_linear_squares(board, dir))

    def fen_symbol(self):
        if self.color == Color.White:
            return "R"
        return "r"