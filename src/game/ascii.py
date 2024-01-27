from game import Game
import chess
from engine import *
import os

class AsciiGame(Game):

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.visual_board = chess.Board()
        self.player_starts = True # For now, player always starts

    def run(self):
        self.render()

        engine_move = None
        if not self.player_starts:
            engine_move = self.engine.make_move(self.board)
            self.update(engine_move)

        while True:
            player_move = self.get_player_move()
            self.update(player_move)
            if self.board.is_over():
                break

            engine_move = self.engine.make_move(self.board)
            self.update(engine_move)
            if self.board.is_over():
                break


    def update(self, move: str):
        """Updates the given move to the UI and renders.
        Assumes the move not to be None.
        """
        self.board.make_move(move)
        self.visual_board.push_uci(move)
        self.render()

    def render(self):
        os.system("clear")
        print(self.visual_board)

    def get_player_move(self):
        next_move = input("Move UCI: ")
        if len(next_move) == 0:
            return None
        return next_move