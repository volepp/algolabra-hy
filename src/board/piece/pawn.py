from numpy.core.multiarray import array as array
from . import Piece, Color, Move
import numpy as np

class Pawn(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color, 1)
        self.movable_squares = []

        # Has to have moved if not on the 2nd or 7th rank
        if square is not None and square[0] != 1 and square[0] != 6:
            self.nr_moves = 1

    def get_movable_squares(self) -> np.array:
        return self.movable_squares

    def calculate_controlled_squares(self, board: np.array, dry_run=False):
        self.controlled_squares = self.get_capture_squares(board)
        self.movable_squares = np.vstack(\
            (self.get_advances(board), self.get_possible_captures(board, self.controlled_squares, dry_run=dry_run)))

    def get_advances(self, board: np.array) -> np.array:
        possible_squares = np.empty((0,2), dtype=int)
        # If white, move up the board, down otherwise
        direction = 1 if self.color == Color.White else -1

        sqr_1 = np.copy(self.square)
        sqr_1[0] += direction # Move 1 square
        move_1_possible = self.is_on_board(sqr_1) and board[tuple(sqr_1)] is None
        if not move_1_possible:
            return possible_squares # moving 2 squares cannot be possible either in this case
        possible_squares = np.vstack((possible_squares, sqr_1))

        if self.nr_moves > 0:
            return possible_squares
        
        sqr_2 = np.copy(self.square)
        sqr_2[0] += 2*direction # Move 2 squares
        if self.is_on_board(sqr_2) and board[tuple(sqr_2)] is None:
            possible_squares = np.vstack((possible_squares, sqr_2))

        return possible_squares
    
    def get_capture_squares(self, board: np.array) -> np.array:
        capture_squares = np.empty((0,2), dtype=int)
        # If white, move up the board, down otherwise
        direction = 1 if self.color == Color.White else -1

        capture_1 = np.copy(self.square)
        capture_1 += (direction, 1)
        if self.is_on_board(capture_1):
            capture_squares = np.vstack((capture_squares, capture_1))

        capture_2 = np.copy(self.square)
        capture_2 += (direction, -1)
        if self.is_on_board(capture_2):
            capture_squares = np.vstack((capture_squares, capture_2))

        return capture_squares
    
    def get_possible_captures(self, board: np.array, capture_squares: np.array, dry_run=False) -> np.array:
        possible_captures = np.empty((0,2), dtype=int)
        for sqr in capture_squares:
            piece_to_capture = board[tuple(sqr)]
            if piece_to_capture is not None and\
                piece_to_capture.color != self.color:

                possible_captures = np.vstack((possible_captures, sqr))
                if not dry_run:
                    piece_to_capture.attacked_by.append(self)            

        return possible_captures


    def fen_symbol(self):
        if self.color == Color.White:
            return "P"
        return "p"