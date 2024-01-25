import ui
from engine import Engine
from board import Board

class Game:

    def __init__(self, ui_client: ui.Ascii|ui.Lichess, engine: Engine, player_starts: bool):
        self.ui_client = ui_client
        self.engine = engine
        self.player_starts = player_starts
        self.board = Board()

    def run(self):
        self.ui_client.start()

        engine_move = None
        if not self.player_starts:
            engine_move = self.engine.make_move(self.board)
            self.board.update(engine_move)

        while True:
            player_move = self.ui_client.update(engine_move)
            self.board.update(player_move)
            if self.board.is_over():
                break

            engine_move = self.engine.make_move(self.board)
            self.board.update(engine_move)
            if self.board.is_over():
                break
