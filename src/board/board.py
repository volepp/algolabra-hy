import numpy as np
from .piece import *
from enum import Enum
import time
import copy
import chess # Only for ascii visualization

class Result(Enum):
    WHITE_WIN = 0
    BLACK_WIN = 1
    DRAW = 2
    STALEMATE = 3

BOARD_SIZE = 8


def flatten_moves(moves):
    return [move for moveset in moves for move in moveset]
class Position:

    def __init__(self, position: np.array = None):
        if position is None:
            self.init_default()
        else:
            self.position = position

        self.white_king = None
        self.black_king = None

        # A memory for the next player's legal moves so they don't have to be calculated multiple times
        self.white_legal_moves = []
        self.black_legal_moves = []
        # Contains True or False for each square that tells whether or not the color has a piece controlling it
        self.white_controlled_squares = np.empty((BOARD_SIZE, BOARD_SIZE), dtype=bool)
        self.black_controlled_squares = np.empty((BOARD_SIZE, BOARD_SIZE), dtype=bool)

    def init_default(self):
        # The position is defined so that row 0 will be the first rank and row 7 will be the 8th rank.
        # Column 0 -> a-file, column 7 -> h-file
        self.position = np.empty((BOARD_SIZE, BOARD_SIZE), dtype=Piece)

        # Set kings
        self[0, 4] = King(np.array([0,4]), Color.White)
        self[7, 4] = King(np.array([7,4]), Color.Black)

        # Set queens
        self[0, 3] = Queen(np.array([0,3]), Color.White)
        self[7, 3] = Queen(np.array([7,3]), Color.Black)

        # Set rooks
        self[0, 0] = Rook(np.array([0,0]), Color.White)
        self[0, 7] = Rook(np.array([0,7]), Color.White)
        self[7, 0] = Rook(np.array([7,0]), Color.Black)
        self[7, 7] = Rook(np.array([7,7]), Color.Black)

        # Set bishops
        self[0, 2] = Bishop(np.array([0,2]), Color.White)
        self[0, 5] = Bishop(np.array([0,5]), Color.White)
        self[7, 2] = Bishop(np.array([7,2]), Color.Black)
        self[7, 5] = Bishop(np.array([7,5]), Color.Black)

        # Set knights
        self[0, 1] = Knight(np.array([0,1]), Color.White)
        self[0, 6] = Knight(np.array([0,6]), Color.White)
        self[7, 1] = Knight(np.array([7,1]), Color.Black)
        self[7, 6] = Knight(np.array([7,6]), Color.Black)

        # Set pawns
        for i in range(0, BOARD_SIZE):
            self[1, i] = Pawn(np.array([1,i]), Color.White)
            self[BOARD_SIZE-2, i] = Pawn(np.array([6,i]), Color.Black)

    def make_move(self, move: Move):
        """ Makes the given move in the position and returns the resulting position. 
        Doesn't check whether the move is legal or not.
        """
        new_pos = Position(copy.deepcopy(self.position))

        new_pos[tuple(move.from_square)].move(move)
        new_pos[tuple(move.to_square)] = new_pos[tuple(move.from_square)]
        new_pos[tuple(move.from_square)] = None

        return new_pos

    def process(self):
        """ Computes the legal moves and controlled squares in the position.
        Saves them to self.white/black_legal_moves and self.white/black_controlled_squares.
        """
        self._process_pieces()

        self.white_legal_moves = self._calc_legal_moves_for_color(Color.White)
        self.black_legal_moves = self._calc_legal_moves_for_color(Color.Black)
    
    def _process_pieces(self):
        """ Calculates the controlled squares for white and black. Also finds the white and black
        kings and stores them in self.white/black_king
        """
        pieces = self.position[self.position != None]
        # First reset all piecces so that no pins or checks will be 
        # accidentally left hanging around from e.g. a previous position.
        for piece in pieces:
            piece.reset()
        for piece in pieces:
            if piece is None: continue
            piece.calculate_controlled_squares(self.position)
            if type(piece) == King:
                if piece.color == Color.White:
                    self.white_king = piece
                else:
                    self.black_king = piece

        white_controlled = np.vstack([\
            piece.get_controlled_squares()\
                for (_,_), piece in np.ndenumerate(self.position)\
                    if piece is not None and piece.color == Color.White ])
        black_controlled = np.vstack([\
            piece.get_controlled_squares()\
                for (_,_), piece in np.ndenumerate(self.position)\
                    if piece is not None and piece.color == Color.Black ])
        self.white_controlled_squares = np.full(self.white_controlled_squares.shape, False)
        self.black_controlled_squares = np.full(self.black_controlled_squares.shape, False)
        self.white_controlled_squares[white_controlled[:,0], white_controlled[:,1]] = True
        self.black_controlled_squares[black_controlled[:,0], black_controlled[:,1]] = True

    def _calc_legal_moves_for_color(self, color: Color):
        """ Calculates the legal moves.
        """
        legal_moves = []
        color_pieces = self.position[self.position != None]
        color_pieces = np.array([piece for piece in color_pieces if piece.color == color])

        candidate_moves = [[Move(piece.square, to_square) for to_square in piece.get_movable_squares()] for piece in color_pieces]
        candidate_moves = flatten_moves(candidate_moves)
        legal_moves = [move for move in candidate_moves if self.is_legal(move)]

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
            print("No piece on specified square")
            return False
        
        # Check that the piece that is moved can move to the specified square.
        movable_squares = np.array(moved_piece.get_movable_squares())
        if move.to_square.tolist() not in movable_squares.tolist():
            print("Not a controlled square")
            return False
        
        # Check that square isn't occupied by own piece
        piece_on_sqr = self.position[tuple(move.to_square)]
        if piece_on_sqr is not None and \
            piece_on_sqr.color == moved_piece.color:
            return False
        
        if self._would_lead_to_check(move): return False

        return True

    def _would_lead_to_check(self, move: Move) -> bool:
        """ Returns whether the given move would lead to the
        player making the move to be in check.
        """
        moved_piece = self.position[tuple(move.from_square)]
        op_controlled_squares = self.black_controlled_squares
        own_king = self.white_king
        if moved_piece.color == Color.Black:
            own_king = self.black_king
            op_controlled_squares = self.white_controlled_squares

        if moved_piece.is_pinned:
            return True

        # Color currently in check. Check if move evades check
        if moved_piece.is_king():
            # Make sure moves away from check
            if op_controlled_squares[tuple(move.to_square)]:
                return True
        else:
            # If not moving the king and not pinned. The move
            # cannot lead to check if not in check already.
            if not self.is_color_in_check(moved_piece.color):
                return False
            
            # If not moving the king, cannot block 2 checks at once
            if len(own_king.attacked_by) > 1:
                return True
        
        # Check if blocks check by making the move and 
        # checking if the previously checking pieces are still
        # controlling the square the king is on in the new position.
        # Also makes sure that if the moving piece is the king, 
        # actually evades the check instead of e.g. moving backwards "away"
        # from a rook check.
        own_king_sqr = own_king.square
        if moved_piece.is_king():
            own_king_sqr = move.to_square
        result_pos = self.make_move(move)
        checking_piece_sqrs = [piece.square for piece in own_king.attacked_by]
        for sqr in checking_piece_sqrs:
            piece = result_pos.position[tuple(sqr)]
            piece.calculate_controlled_squares(result_pos.position)
            piece_controlled_squares = piece.get_controlled_squares()
            if own_king_sqr.tolist() in piece_controlled_squares.tolist():
                return True
        return False

    def is_color_in_check(self, color: Color) -> bool:
        """ Returns which color is in check or None if neither.
        Expects self.white/black_controlled_squares to be up-to-date.
        """
        if color == Color.White:
            return len(self.white_king.attacked_by) > 0
        else:
            return len(self.black_king.attacked_by) > 0
        
    def get_square_value_weights(self):
        """ Returns weights between 0 and 1 to all the squares based on 
        how valuable the square is to control. In general, central squares 
        are considered higher value as well as squares closer to the enemy king. 
        """
        weights = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=float)
        # The basic idea is that the central squares are 0.5 and the weight
        # decreases linearly the further we go from the center.
        center_weight = 0.5
        weights[3:5, 3:5] = center_weight
        non_center_coordinates = np.argwhere(weights == 0)
        # Distance from center (in theory can be thought of as (3.5, 3.5))
        coordinate_distances = np.abs(non_center_coordinates.astype(float)-np.array([3.5, 3.5]))
        coordinate_distances = np.linalg.norm(coordinate_distances, axis=1)
        weights[tuple(zip(*non_center_coordinates))] = center_weight/coordinate_distances
        
        return weights
    
    def get_control_scores(self):
        """ Returns the total sum of values of controlled squares weighted by 
        how important the squares are (get_square_value_weights) for white and black respectively.
        """
        square_weights = self.get_square_value_weights()
        white_score = np.sum(np.multiply(self.white_controlled_squares, square_weights))
        black_score = np.sum(np.multiply(self.black_controlled_squares, square_weights))

        return white_score, black_score

    def get_piece_control_score(self, piece):
        """ Returns the sum of the values of the squares that the given piece controls.
        """
        square_weights = self.get_square_value_weights()
        piece_control_score = 0
        for square in piece.get_controlled_squares():
            piece_control_score += square_weights[tuple(square)]

        return piece_control_score

    def __getitem__(self, key):
        return self.position.__getitem__(key)

    def __setitem__(self, key, value):
        self.position.__setitem__(key, value)

    def __eq__(self, other):
        return self.position.__eq__(other)

    def __ne__(self, other):
        return self.position.__ne__(other)

    def __repr__(self):
        return self.position.__repr__()

class Board:

    def __init__(self):
        self.position = Position()
        self.position.process()
        # Keeps track of the positions before self.position
        self.position_history = []
        self.moves = []
        self.result = None

    def update_moves(self, movestr: str):
        """ Update multiple moves as a space separated string e.g. 'e2e4 e7e5'.
        Resets all moves if an empty string is given.
        """
        if len(movestr) == 0:
            self.moves = []
            return
        for mstr in movestr.strip().split(" "):
            self.play_move(Move.parse_uci(mstr))

    def play_move(self, move: Move, check_legality=True):
        """ Makes the given move on the board. Raises an error if the move is illegal.
        Returns the result if the game ends (None if game is still ongoing) and whether the move was played.
        The might will not be played if the game has already ended.
        """
        if self.result != None:
            return self.result, False

        if check_legality and not self.position.is_legal(move):
            raise ValueError(f"Illegal move attempted: {move}")

        self.moves.append(move)

        self.position_history.append(copy.deepcopy(self.position))
        self.position = self.position.make_move(move)
        self.position.process()
        
        self.update_game_result()
        return self.result, True

    def update_game_result(self):
        next_color = self.next_move_color()
        next_player_moves = self.get_legal_moves(next_color)
        if len(next_player_moves) == 0:
            if next_color == Color.White and self.position.is_color_in_check(Color.White):
                self.result = Result.BLACK_WIN
            elif next_color == Color.Black and self.position.is_color_in_check(Color.Black):
                self.result = Result.WHITE_WIN
            else:
                self.result = Result.STALEMATE
            return

        self.result = None

    def get_pieces_for_color(self, color: Color):
        pieces = []
        for (_, _), piece in np.ndenumerate(self.position):
            if piece is not None and piece.color == color:
                pieces.append(piece)
        
        return pieces

    def undo_last_move(self):
        self.moves = self.moves[:-1]
        self.position = self.position_history.pop()
        # Assume that the game must've been ongoing before the last move
        self.result = None

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
    
    def get_nr_moves(self):
        return len(self.moves)

    def get_legal_moves(self, color: Color):
        if color == Color.White:
            return self.position.white_legal_moves
        else:
            return self.position.black_legal_moves

    def is_game_over(self):
        return self.result != None
    
    def get_result(self) -> Result:
        """ Returns the result of the game or None if the game isn't over.
        """
        return self.result
    
    def board_fen(self) -> str:
        fen = ""
        for rank in reversed(range(BOARD_SIZE)):
            counter = 0
            for file in range(BOARD_SIZE):
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

    def fen(self):
        fen = self.board_fen()
        if self.next_move_color() == Color.White:
            fen += " w"
        else:
            fen += " b"
        return fen

    def load_board_fen(self, fen: str):
        """ Loads the board position from the given FEN.
        Expects the array size to be (8,8) and always assumes white to play
        """
        self.position = Position(np.empty((BOARD_SIZE, BOARD_SIZE), dtype=Piece))
        self.moves = []

        # In FEN the board is described top-down (from 8th rank to 1st)
        rank = BOARD_SIZE-1
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
                    self.position.white_king = piece
                else:
                    self.position.black_king = piece

            file += 1
        self.position.process()
        self.update_game_result()

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

    def visualize(self):
        vis_board = chess.Board()
        vis_board.set_board_fen(self.board_fen())
        print(vis_board)