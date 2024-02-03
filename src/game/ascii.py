from game import Game
import chess
from engine import *
from board.piece import Move, Color
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
            if self.board.is_game_over():
                break

            engine_move = self.engine.make_move(self.board)
            self.update(engine_move)
            if self.board.is_game_over():
                break


    def update(self, move: Move|str):
        """Updates the given move to the UI and renders.
        Assumes the move not to be None.
        """
        if type(move) is str:
            move = Move.parse_uci(move)
        self.board.play_move(move)
        self.render()

    def render(self):
        os.system("clear")
        self.visual_board.set_board_fen(self.board.board_fen())
        print(self.visual_board)
        print("Legal moves (W): ", self.board.get_legal_moves(Color.White))
        print("Legal moves (B): ", self.board.get_legal_moves(Color.Black))

    def get_player_move(self):
        while True:
            next_move = input("Move UCI: ")
            if len(next_move) == 0:
                return None
            try:
                # Check move validity
                chess.Move.from_uci(next_move)
                return next_move
            except chess.InvalidMoveError:
                print("Invalid move!")
                continue