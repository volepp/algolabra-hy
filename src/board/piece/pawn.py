from . import Piece, Color, Move
import numpy as np

class Pawn(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color)

    def calculate_controlled_squares(self, board: np.array):
        # TODO think this through because technically the pawn doesn't
        # control the squares in front of it
        self.controlled_squares = self.get_advances(board)
        self.controlled_squares.extend(self.get_captures(board))    

    def get_advances(self, board: np.array) -> [Move]:
        possible_squares = []
        # If white, move up the board, down otherwise
        direction = 1 if self.color == Color.White else -1

        sqr_1 = np.copy(self.square)
        sqr_1[0] += direction # Move 1 square
        move_1_possible = self.is_on_board(sqr_1) and board[tuple(sqr_1)] is None
        if not move_1_possible:
            return possible_squares # moving 2 squares cannot be possible either in this case
        possible_squares.append(sqr_1)

        if self.nr_moves > 0:
            return possible_squares
        
        sqr_2 = np.copy(self.square)
        sqr_2[0] += 2*direction # Move 2 squares
        if self.is_on_board(sqr_2) and board[tuple(sqr_2)] is None:
            possible_squares.append(sqr_2)

        return possible_squares
    
    def get_captures(self, board: np.array) -> [Move]:
        possible_squares = []
        # If white, move up the board, down otherwise
        direction = 1 if self.color == Color.White else -1

        capture_1 = np.copy(self.square)
        capture_1 += (direction, 1)
        if self.is_on_board(capture_1) and \
            board[tuple(capture_1)] is not None and \
            board[tuple(capture_1)].color != self.color:
            possible_squares.append(capture_1)

        capture_2 = np.copy(self.square)
        capture_2 += (direction, -1)
        if self.is_on_board(capture_2) and \
            board[tuple(capture_2)] is not None and \
            board[tuple(capture_2)].color != self.color:
            possible_squares.append(capture_2)

        return possible_squares
    
    def fen_symbol(self):
        if self.color == Color.White:
            return "P"
        return "p"