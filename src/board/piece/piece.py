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
        self.controlled_squares = []

    def move(self, move: Move):
        self.nr_moves += 1
        self.square = move.to_square

    def undo(self, move: Move):
        self.nr_moves -= 1
        self.square = move.from_square

    def calculate_controlled_squares(self, board: np.array):
        """ Finds the squares the piece controls in the given position
        and stores them in self.controlled_squares
        """
        pass

    def get_controlled_squares(self) -> [Move]:
        """ Returns the possible moves for this piece in the given position.
        """
        return self.controlled_squares

    def is_on_board(self, square: np.array):
        if square[0] < 0 or square[0] >= 8:
            return False
        if square[1] < 0 or square[1] >= 8:
            return False
        return True
    
    def has_piece(self, board: np.array, square: np.array):
        if board[tuple(square)] is None:
            return False
        return True
    
    def find_linear_squares(self, board: np.array, direction: tuple) -> [Move]:
        """ Finds squares linearly following the specified direction until
        out of board or blocked by another piece that cannot be captured.
        """
        squares = []
        (nr_ranks, _) = board.shape
        for i in range(1, nr_ranks+1):
            # Move i steps to current direction
            movement = (direction[0]*i, direction[1]*i)
            resulting_square = self.square + movement
            if not self.is_on_board(resulting_square):
                break
            if self.has_piece(board, resulting_square):
                # Still controls the square, but doesn't see further
                squares.append(resulting_square)
                break
            squares.append(resulting_square)

        return squares

    def __repr__(self):
        color_str = "(W)"
        if self.color == Color.Black:
            color_str = "(B)"
        return type(self).__name__[:4] + color_str
    
    def fen_symbol(self):
        pass

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        
        if self.color != other.color:
            return False
        
        # Position doesn't matter
        return True