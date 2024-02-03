import numpy as np
from .piece import *

class Board:

    BOARD_SIZE = 8

    def __init__(self):
        self.setup_board()
        self._recalculate_controlled_squares()
        self.moves = []
        # Maps a move number to a captured piece
        self.captures = {}

    def setup_board(self):
        self.position = np.empty((self.BOARD_SIZE, self.BOARD_SIZE), dtype=Piece)

        # Board is defined so that row 0 will be the first rank and row 7 will be the 8th rank.
        # Column 0 -> a-file, column 7 -> h-file

        # Set kings
        self.white_king = King(np.array([0,4]), Color.White)
        self.black_king = King(np.array([7,4]), Color.Black)
        self.position[0, 4] = self.white_king
        self.position[7, 4] = self.black_king
        self.white_in_check = False
        self.black_in_check = False

        # Set queens
        self.position[0, 3] = Queen(np.array([0,3]), Color.White)
        self.position[7, 3] = Queen(np.array([7,3]), Color.Black)

        # Set rooks
        self.position[0, 0] = Rook(np.array([0,0]), Color.White)
        self.position[0, 7] = Rook(np.array([0,7]), Color.White)
        self.position[7, 0] = Rook(np.array([7,0]), Color.Black)
        self.position[7, 7] = Rook(np.array([7,7]), Color.Black)

        # Set bishops
        self.position[0, 2] = Bishop(np.array([0,2]), Color.White)
        self.position[0, 5] = Bishop(np.array([0,5]), Color.White)
        self.position[7, 2] = Bishop(np.array([7,2]), Color.Black)
        self.position[7, 5] = Bishop(np.array([7,5]), Color.Black)

        # Set knights
        self.position[0, 1] = Knight(np.array([0,1]), Color.White)
        self.position[0, 6] = Knight(np.array([0,6]), Color.White)
        self.position[7, 1] = Knight(np.array([7,1]), Color.Black)
        self.position[7, 6] = Knight(np.array([7,6]), Color.Black)

        # Set pawns
        for i in range(0, self.BOARD_SIZE):
            self.position[1, i] = Pawn(np.array([1,i]), Color.White)
            self.position[self.BOARD_SIZE-2, i] = Pawn(np.array([6,i]), Color.Black)

    def _recalculate_controlled_squares(self):
        for (_, _), piece in np.ndenumerate(self.position):
            if piece is None: continue
            piece.calculate_controlled_squares(self.position)

    def update_moves(self, movestr: str):
        """ Update multiple moves as a space separated string e.g. 'e2e4 e7e5'.
        Resets all moves if an empty string is given.
        """
        if len(movestr) == 0:
            self.moves = []
            return
        for mstr in movestr.strip().split(" "):
            self._make_move(Move.parse_uci(mstr))

    def play_move(self, move: Move):
        """ Makes the given move on the board. Raises an error if the move is illegal.
        """
        if not self.is_legal(move):
            raise ValueError(f"Illegal move attempted: {move}")
        
        self._make_move(move)
        self._recalculate_controlled_squares()
        
    def _make_move(self, move: Move):
        """ Makes the given move on the board without checking whether it's legal or not.
        """
        self.moves.append(move)

        captured_piece = self.position[tuple(move.to_square)]
        if captured_piece is not None:
            self.captures[len(self.moves)-1] = captured_piece

        self.position[tuple(move.from_square)].move(move)
        self.position[tuple(move.to_square)] = self.position[tuple(move.from_square)]
        self.position[tuple(move.from_square)] = None

    def get_pieces_for_color(self, color: Color) -> [Piece]:
        pieces = []
        for (_, _), piece in np.ndenumerate(self.position):
            if piece is not None and piece.color == color:
                pieces.append(piece)
        
        return pieces

    def undo_last_move(self):
        last_move = self.moves[-1]
        reverse_move = Move(last_move.to_square, last_move.from_square)
        self._make_move(reverse_move)
        # Remove the two previous moves (reverse and original move)
        self.moves = self.moves[:-2]
        removed_move_index = len(self.moves)
        if removed_move_index in self.captures:
            recovered_piece = self.captures.pop(removed_move_index)
            self.position[tuple(recovered_piece.square)] = recovered_piece
        self._recalculate_controlled_squares()

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
        for rank, file in np.ndindex(self.position.shape):
            piece = self.position[rank, file]
            if piece is None:
                continue
            if piece.color != color:
                continue
            
            controlled_squares = piece.get_controlled_squares()
            for csqr in controlled_squares:
                move = Move(piece.square, csqr)
                if self._is_move_legal(move):
                    legal_moves.append(move)

        return legal_moves

    def is_legal(self, move: Move) -> bool:
        """ Checks if the following conditions apply for the given move:
            - The starting square of the move has to contain a piece
            - The move has to be possible for the piece that is to be moved
            - The move cannot lead to the player being in check
        """
        # First check if the move is possible (piece exists and can move to given square)
        moved_piece = self.position[tuple(move.from_square)]
        if moved_piece is None:
            # No piece in specified square
            return False
        
        controlled_squares = np.array(moved_piece.get_controlled_squares())
        if move.to_square.tolist() not in controlled_squares.tolist():
            return False
            
        return self._is_move_legal(move)
    
    def _is_move_legal(self, move: Move) -> bool:
        """ Returns whether the given move is legal.
        """
        moved_piece = self.position[tuple(move.from_square)]
        piece_on_sqr = self.position[tuple(move.to_square)]
        if piece_on_sqr is not None and \
            piece_on_sqr.color == moved_piece.color:
            return False

        self._make_move(move)

        # Check if player making the move would be in check afterwards
        if self.color_in_check() == moved_piece.color:
            self.undo_last_move()
            return False

        self.undo_last_move()
        return True

    def color_in_check(self) -> Color:
        """ Returns which color is in check or None if neither
        """
        for piece in self.get_pieces_for_color(Color.Black):
            csqrs = np.array(piece.get_controlled_squares())
            if self.white_king.square.tolist() in csqrs.tolist():
                # Player would be in check
                return Color.White
        
        for piece in self.get_pieces_for_color(Color.White):
            csqrs = np.array(piece.get_controlled_squares())
            if self.black_king.square.tolist() in csqrs.tolist():
                # Player would be in check
                return Color.Black

        return None

    def is_game_over(self):
        return len(self.get_legal_moves(self.next_move_color())) == 0
    
    def get_result(self):
        """ Returns the result of the game or None if the game isn't over.
        """
        if not self.is_game_over():
            return None
        
        # TODO implement
        return None
    
    def board_fen(self) -> str:
        fen = ""
        for rank in reversed(range(self.position.shape[0])):
            counter = 0
            for file in range(self.position.shape[1]):
                piece = self.position[rank, file]
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

    def load_board_fen(self, fen: str):
        """ Loads the board position from the given FEN.
        Expects the array size to be (8,8) and always assumes white to play
        """
        self.position = np.empty((self.BOARD_SIZE, self.BOARD_SIZE), dtype=Piece)
        self.moves = []

        # In FEN the board is described top-down (from 8th rank to 1st)
        rank = self.BOARD_SIZE-1
        file = 0
        for c in fen:
            if c == " ":
                # Stop after the board part in FEN
                break
            if c == "/":
                rank -= 1
                file = 0
                continue

            if c.isnumeric():
                nr_empty_squares = int(c)
                file += nr_empty_squares
                continue

            piece = self._get_piece_from_fen_symbol(c, np.array([rank, file]))
            self.position[rank, file] = piece
            if type(piece) == King:
                if piece.color == Color.White:
                    self.white_king = piece
                else:
                    self.black_king = piece

            file += 1

        self._recalculate_controlled_squares()

    def _get_piece_from_fen_symbol(self, symbol: str, square: np.array):
        if len(symbol) != 1:
            raise ValueError("Incorrect FEN symbol")
        
        color = Color.White
        if symbol.islower():
            color = Color.Black

        symbol = symbol.lower()
        if symbol == "p":
            return Pawn(square, color)
        elif symbol == "n":
            return Knight(square, color)
        elif symbol == "b":
            return Bishop(square, color)
        elif symbol == "r":
            return Rook(square, color)
        elif symbol == "q":
            return Queen(square, color)
        elif symbol == "k":
            return King(square, color)