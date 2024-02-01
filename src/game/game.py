from engine import Engine
from board import Board

class Game:

    def __init__(self, engine: Engine):
        self.board = Board()
        self.engine = engine
    
    def run(self):
        pass