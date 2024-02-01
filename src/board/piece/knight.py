from . import Piece, Color, Move
import numpy as np

class Knight(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color)

    def get_possible_moves(self, board: np.array) -> [Move]:
        possible_moves = []
        possible_movements = np.array(np.meshgrid([-2,-1,1,2], [-2,-1,1,2])).T.reshape(-1, 2)
        # The knight always moves 3 squares in total (either 2 up and 1 right/left, 2 right and 1 up/down, etc.)
        possible_movements = possible_movements[np.abs(possible_movements).sum(axis=1) == 3]
        for movement in possible_movements:
            resulting_square = self.square + tuple(movement)
            if self.can_move_to(board, resulting_square):
                possible_moves.append(Move(self.square, resulting_square))

        return possible_moves

    
    def fen_symbol(self):
        if self.color == Color.White:
            return "N"
        return "n"