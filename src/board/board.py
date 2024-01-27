import numpy as np
from enum import Enum

class Color(Enum):
    White = 1
    Black = 2

class Board:

    def __init__(self):
        self.board = np.zeros((8,8))
        self.moves = []

    def update_moves(self, movestr: str):
        """ Update multiple moves as a space separated string e.g. 'e2e4 e7e5'.
        Resets all moves if an empty string is given.
        """
        if len(movestr) == 0:
            self.moves = []
            return
        self.moves = movestr.strip().split(" ")

    def make_move(self, move: str):
        """ Make a single move on the board.
        """
        self.moves.append(move)

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

    def is_over(self):
        # TODO implement
        return False
    
    def get_result(self):
        # TODO implement
        return None
        