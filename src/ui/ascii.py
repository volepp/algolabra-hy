import chess
import os

class Ascii:

    def __init__(self):
        self.board = chess.Board()

    def start(self):
        self.render()

    def update(self, move: str):
        """Updates the given move to the UI if the move is not None and renders.
        Then waits for the user to make a move and returns it.
        Returns None if the player resigns.
        """

        if move is not None:
            self.board.push_san(move)
            self.render()
        next_move = input()
        if len(next_move) == 0:
            return None
        self.board.push_san(next_move)
        self.render()
        return next_move

    def render(self):
        os.system("clear")
        print(self.board)