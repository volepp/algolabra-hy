from . import Piece, Color, Move
import numpy as np

class Knight(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color, 3)

    def calculate_controlled_squares(self, position: np.array):
        self.controlled_squares = np.empty((0,2), dtype=int)
        possible_movements = np.array(np.meshgrid([-2,-1,1,2], [-2,-1,1,2])).T.reshape(-1, 2)
        # The knight always moves 3 squares in total (either 2 up and 1 right/left, 2 right and 1 up/down, etc.)
        possible_movements = possible_movements[np.abs(possible_movements).sum(axis=1) == 3]
        for movement in possible_movements:
            resulting_square = self.square + tuple(movement)
            if not self.is_on_board(resulting_square):
                continue
            self.controlled_squares = np.vstack((self.controlled_squares, resulting_square))

            piece_on_square = position[tuple(resulting_square)]
            if piece_on_square is not None and piece_on_square.color != self.color:
                piece_on_square.attacked_by.append(self)
    
    def fen_symbol(self):
        if self.color == Color.White:
            return "N"
        return "n"