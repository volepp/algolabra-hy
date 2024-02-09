from . import Piece, Color, Move
import numpy as np

class Queen(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color, 9)

    def calculate_controlled_squares(self, board: np.array):
        self.controlled_squares = np.empty((0,2), dtype=int)
        possible_directions = np.array(np.meshgrid([-1,0,1], [-1,0,1])).T.reshape(-1, 2)
        for [d_rank, d_file] in possible_directions:
            if d_rank == 0 and d_file == 0:
                continue
            self.controlled_squares = np.vstack((self.controlled_squares, self.calculate_linear_squares(board, (d_rank, d_file))))
    
    def fen_symbol(self):
        if self.color == Color.White:
            return "Q"
        return "q"