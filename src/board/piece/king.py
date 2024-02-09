from numpy.core.multiarray import array as array
from . import Piece, Color, Move
import numpy as np

class King(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color, 0)
        self.checked_by = []

    def move(self, move):
        super().move(move)

    def is_king(self):
        return True

    def calculate_controlled_squares(self, board: np.array):
        self.controlled_squares = np.empty((0,2), dtype=int)
        possible_directions = np.array(np.meshgrid([-1,0,1], [-1,0,1])).T.reshape(-1, 2)
        for [d_rank, d_file] in possible_directions:
            if d_rank == 0 and d_file == 0:
                continue
            resulting_square = self.square + (d_rank, d_file)
            if not self.is_on_board(resulting_square):
                continue
            self.controlled_squares = np.vstack((self.controlled_squares, resulting_square))

    def fen_symbol(self):
        if self.color == Color.White:
            return "K"
        return "k"