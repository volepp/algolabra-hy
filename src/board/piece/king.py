from . import Piece, Color, Move
import numpy as np

class King(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color)

    def get_possible_moves(self, board: np.array) -> [Move]:
        possible_moves = []
        possible_directions = np.array(np.meshgrid([-1,0,1], [-1,0,1])).T.reshape(-1, 2)
        for [d_rank, d_file] in possible_directions:
            if d_rank == 0 and d_file == 0:
                continue
            resulting_square = self.square + (d_rank, d_file)
            if self.can_move_to(board, resulting_square):
                possible_moves.append(Move(self.square, resulting_square))

        return possible_moves
    
    def fen_symbol(self):
        if self.color == Color.White:
            return "K"
        return "k"