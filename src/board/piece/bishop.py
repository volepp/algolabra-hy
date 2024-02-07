from . import Piece, Color, Move
import numpy as np

class Bishop(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color, 3)

    def calculate_controlled_squares(self, board: np.array):
        self.controlled_squares = []
        possible_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dir in possible_directions:
            self.controlled_squares.extend(self.find_linear_squares(board, dir))
    
    def fen_symbol(self):
        if self.color == Color.White:
            return "B"
        return "b"