import numpy as np
from .color import Color
from .move import Move

class Piece:

    def __init__(self, square: np.array, color: Color, value: int):
        """ Initializes the piece on the given square.
        The square parameter is a np array in the format [file, rank] so that
        a=1, b=2, c=3, ..., h=8, meaning [1,3] => a3, [5, 1] => e1 etc.
        """
        self.square = square
        self.color = color
        self.nr_moves = 0
        self.controlled_squares = []
        self.value = value
        self.is_pinned = False
        self.pinning = []
        self.attacked_by = []

    def move(self, move: Move):
        self.nr_moves += 1
        self.square = move.to_square

        for p in self.pinning:
            p.is_pinned = False
        self.pinning = []

    def undo(self, move: Move):
        self.nr_moves -= 1
        self.square = move.from_square

    def calculate_controlled_squares(self, board: np.array):
        """ Finds the squares the piece controls in the given position
        and stores them in self.controlled_squares
        """
        pass

    def get_controlled_squares(self) -> np.array:
        """ Returns the possible moves for this piece in the given position
        or None if no controlled squares
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

    def is_king(self):
        # Not pretty, but by default return False
        # King class overrides by returning True
        return False
    
    def reset(self):
        """ Resets the piece's is_pinned and attacked_by statuses.
        Should pretty much only be called before the whole board is 
        re-evaluated.
        """
        self.is_pinned = False
        self.pinning = []
        self.attacked_by = []

    def calculate_linear_squares(self, position: np.array, direction: tuple) -> np.array:
        """ Calculates controlled squares by linearly following the specified direction until
        out of board or blocked by another piece that cannot be captured.
        If x-rays the opponent king through an oppponent piece, marks the opponent
        piece as pinned by setting its .is_pinned to True. If is checking the king,
        sets the king's is_checked to True.
        """
        squares = np.empty((0,2), dtype=int)
        (nr_ranks, _) = position.shape
        attacked_piece = None # Piece that was 
        for i in range(1, nr_ranks+1):
            # Move i steps to current direction
            movement = (direction[0]*i, direction[1]*i)
            resulting_square = self.square + movement
            if not self.is_on_board(resulting_square):
                break
            if self.has_piece(position, resulting_square):
                piece = position[tuple(resulting_square)]
                if piece.color == self.color:
                    squares = np.vstack((squares, resulting_square))
                    break # Hit own piece, exit loop
                elif attacked_piece is None:
                    # Attacking the piece (instead of x-raying it)
                    squares = np.vstack((squares, resulting_square))
                    piece.attacked_by.append(self)
                    if piece.is_king():
                        # No need to continue and check for pins
                        # if attacking the opponent king
                        break
                    attacked_piece = piece
                    continue
                else:
                    # Already attacking some piece and currently checking for pins.
                    # i.e. exploring "x-rayed" pieces.
                    if piece.is_king():
                        # X-raying the king behind the attacked_piece
                        attacked_piece.is_pinned = True
                        self.pinning.append(attacked_piece)
                    break # No need to go further, cannot x-ray more than one piece.
                    
            if attacked_piece is None:
                # If attacked_piece is not None, would be checking x-rayed squares
                # which the piece doesn't actually control.
                squares = np.vstack((squares, resulting_square))

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