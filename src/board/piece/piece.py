import numpy as np
from .color import Color
from .move import Move

class Piece:

    def __init__(self, square: np.array, color: Color):
        """ Initializes the piece on the given square.
        The square parameter is a np array in the format [file, rank] so that
        a=1, b=2, c=3, ..., h=8, meaning [1,3] => a3, [5, 1] => e1 etc.
        """
        self.square = square
        self.color = color
        self.nr_moves = 0

    def move(self, move: Move):
        self.nr_moves += 1
        self.square = move.to_square

    def undo(self, move: Move):
        self.nr_moves -= 1
        self.square = move.from_square

    def get_possible_moves(self, board: np.array) -> [Move]:
        """ Finds and returns the legal moves for this piece on the given board.
        """
        pass

    def is_on_board(self, square: np.array):
        if square[0] < 0 or square[0] >= 8:
            return False
        if square[1] < 0 or square[1] >= 8:
            return False
        return True
    
    def get_move(self, to_square: np.array) -> Move:
        return Move(self.square, to_square)
    
    def can_move_to(self, board: np.array, square: np.array):
        if not self.is_on_board(square):
            return False
        piece_on_sqr = board[tuple(square)]
        if piece_on_sqr is None or\
            piece_on_sqr.color != self.color:
            return True
        return False
    
    def find_linear_moves(self, board: np.array, direction: tuple) -> [Move]:
        """ Finds moves linearly following the specified direction until
        out of board or blocked by another piece that cannot be captured.
        """
        moves = []
        (nr_ranks, _) = board.shape
        for i in range(1, nr_ranks+1):
            # Move i steps to current direction
            movement = (direction[0]*i, direction[1]*i)
            resulting_square = self.square + movement
            if self.can_move_to(board, resulting_square):
                moves.append(Move(self.square, resulting_square))
            else:
                # Cannot move further if out of board or piece blocking the way
                break

        return moves

    def __repr__(self):
        color_str = "(W)"
        if self.color == Color.Black:
            color_str = "(B)"
        return type(self).__name__[:4] + color_str
    
    def fen_symbol(self):
        pass