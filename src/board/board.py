import numpy as np
from .piece import *

class Board:

    BOARD_SIZE = 8

    def __init__(self):
        self.setup_board()
        self.moves = []

    def setup_board(self):
        self.board = np.empty((self.BOARD_SIZE, self.BOARD_SIZE), dtype=Piece)

        # Board is defined so that row 0 will be the first rank and row 7 will be the 8th rank.
        # Column 0 -> a-file, column 7 -> h-file

        # Set kings
        self.board[0, 4] = King(np.array([0,4]), Color.White)
        self.board[7, 4] = King(np.array([7,4]), Color.Black)

        # Set queens
        self.board[0, 3] = Queen(np.array([0,3]), Color.White)
        self.board[7, 3] = Queen(np.array([7,3]), Color.Black)

        # Set rooks
        self.board[0, 0] = Rook(np.array([0,0]), Color.White)
        self.board[0, 7] = Rook(np.array([0,7]), Color.White)
        self.board[7, 0] = Rook(np.array([7,0]), Color.Black)
        self.board[7, 7] = Rook(np.array([7,7]), Color.Black)

        # Set bishops
        self.board[0, 2] = Bishop(np.array([0,2]), Color.White)
        self.board[0, 5] = Bishop(np.array([0,5]), Color.White)
        self.board[7, 2] = Bishop(np.array([7,2]), Color.Black)
        self.board[7, 5] = Bishop(np.array([7,5]), Color.Black)

        # Set knights
        self.board[0, 1] = Knight(np.array([0,1]), Color.White)
        self.board[0, 6] = Knight(np.array([0,6]), Color.White)
        self.board[7, 1] = Knight(np.array([7,1]), Color.Black)
        self.board[7, 6] = Knight(np.array([7,6]), Color.Black)

        # Set pawns
        for i in range(0, self.BOARD_SIZE):
            self.board[1, i] = Pawn(np.array([1,i]), Color.White)
            self.board[self.BOARD_SIZE-2, i] = Pawn(np.array([6,i]), Color.Black)

    def update_moves(self, movestr: str):
        """ Update multiple moves as a space separated string e.g. 'e2e4 e7e5'.
        Resets all moves if an empty string is given.
        """
        if len(movestr) == 0:
            self.moves = []
            return
        self.moves = movestr.strip().split(" ")

    def make_move(self, move: Move):
        """ Make a single move on the board.
        """
        self.moves.append(move)

        self.board[tuple(move.from_square)].move(move)
        self.board[tuple(move.to_square)] = self.board[tuple(move.from_square)]
        self.board[tuple(move.from_square)] = None

    def undo_last_move(self):
        last_move = self.moves[-1]
        
        self.board[tuple(last_move.to_square)].undo(last_move)
        self.board[tuple(last_move.from_square)] = self.board[tuple(last_move.to_square)]
        self.board[tuple(last_move.to_square)] = None

    def get_last_move(self):
        """ Returns the last move made or None if no moves have been made.
        """
        if len(self.moves) == 0:
            return None
        return self.moves[-1]
    
    def next_move_color(self):
        """ Returns which color has the next move
        """
        if len(self.moves) % 2 == 0:
            return Color.White
        return Color.Black
    
    def get_legal_moves(self, color: Color) -> [Move]:
        legal_moves = []
        for rank, file in np.ndindex(self.board.shape):
            piece = self.board[rank, file]
            if piece is None:
                continue
            if piece.color != color:
                continue
            possible_moves = piece.get_possible_moves(self.board)
            # Filter out illegal moves
            possible_moves = [move for move in possible_moves if self.is_legal(move)]
            legal_moves.extend(possible_moves)

        return legal_moves

    def is_legal(self, move: Move) -> bool:
        """ Checks if in the resulting position the player making the move
        would be in check (illegal)
        """
        # TODO

        return True

    def is_check(self) -> Color:
        """ Returns which color is in check or None if neither
        """
        # TODO

        return None

    def is_over(self):
        # TODO implement
        return False
    
    def get_result(self):
        # TODO implement
        return None
        
    def fen(self) -> str:
        fen = self.board_fen()
        if self.next_move_color() == Color.White:
            fen += " w"
        else:
            fen += " b"
        
        # For now say that never can castle
        fen += " -"

        # For now skip the possibility of an en passant 
        fen += " -"

        # Always set halfmove clock as 0
        fen += " 0"
        
        fen += f" {len(self.moves)}"

        return fen
    
    def board_fen(self) -> str:
        fen = ""
        for rank in reversed(range(self.board.shape[0])):
            counter = 0
            for file in range(self.board.shape[1]):
                piece = self.board[rank, file]
                if piece is None:
                    counter += 1
                    continue
                if counter > 0:
                    fen += str(counter)
                    counter = 0
                fen += piece.fen_symbol()
            if counter > 0:
                fen += str(counter)
            if rank > 0:
                # No slash on the last rank
                fen += "/"
            
        return fen
