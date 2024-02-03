import unittest
import numpy as np
from board import *
from board.piece import *

class TestPieces(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_king_controlled_squares(self):
        # Kings should control 5 squares when game starts
        self.assertEqual(len(self.board.white_king.get_controlled_squares()), 5)
        self.assertEqual(len(self.board.black_king.get_controlled_squares()), 5)

        self.board.load_board_fen("8/8/3k4/8/3K4/8/8/8") # Position with only both kings in the middle of the board
        self.assertEqual(len(self.board.white_king.get_controlled_squares()), 8)
        self.assertEqual(len(self.board.black_king.get_controlled_squares()), 8)