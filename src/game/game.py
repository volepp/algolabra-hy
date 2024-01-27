from engine import Engine
from board import Board

# Default game is the ASCII version
class Game:

    def __init__(self, engine: Engine):
        self.board = Board()
        self.engine = engine
    
    def run(self):
        pass