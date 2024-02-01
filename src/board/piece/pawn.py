from . import Piece, Color, Move
import numpy as np

class Pawn(Piece):

    def __init__(self, square: np.array, color: Color):
        super().__init__(square, color)

    def get_possible_moves(self, board: np.array) -> [Move]:
        possible_moves = self.get_advances(board)
        possible_moves.extend(self.get_captures(board))    

        return possible_moves
    
    def get_advances(self, board: np.array) -> [Move]:
        possible_moves = []
        # If white, move up the board, down otherwise
        direction = 1 if self.color == Color.White else -1

        move_1 = np.copy(self.square)
        move_1[0] += direction # Move 1 square
        if self.is_on_board(move_1) and board[tuple(move_1)] is None:
            possible_moves.append(self.get_move(move_1))

        if self.nr_moves > 0:
            return possible_moves
        
        move_2 = np.copy(self.square)
        move_2[0] += 2*direction # Move 2 squares
        if self.is_on_board(move_2) and board[tuple(move_2)] is None:
            possible_moves.append(self.get_move(move_2))

        return possible_moves
    
    def get_captures(self, board: np.array) -> [Move]:
        possible_moves = []
        # If white, move up the board, down otherwise
        direction = 1 if self.color == Color.White else -1

        capture_1 = np.copy(self.square)
        capture_1 += (direction, 1)
        if self.is_on_board(capture_1) and \
            board[tuple(capture_1)] is not None and \
            board[tuple(capture_1)].color != self.color:
            possible_moves.append(self.get_move(capture_1))

        capture_2 = np.copy(self.square)
        capture_2 += (direction, -1)
        if self.is_on_board(capture_2) and \
            board[tuple(capture_2)] is not None and \
            board[tuple(capture_2)].color != self.color:
            possible_moves.append(self.get_move(capture_2))

        return possible_moves
    
    def fen_symbol(self):
        if self.color == Color.White:
            return "P"
        return "p"