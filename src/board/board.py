import numpy as np

class Board:

    def __init__(self):
        self.board = np.zeros((8,8))
        self.last_move = None

    def update(self, move):
        self.last_move = move
        return None

    def get_last_move(self):
        return self.last_move

    def is_over(self):
        return False
    
    def get_result(self):
        return None
        