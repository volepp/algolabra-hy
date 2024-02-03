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

    def test_knight_controlled_squares(self):
        white_knight_1 = self.board.position[0, 1]
        white_knight_2 = self.board.position[0, 6]
        black_knight_1 = self.board.position[7, 1]
        black_knight_2 = self.board.position[7, 6]
        self.assertEqual(len(white_knight_1.get_controlled_squares()), 3)
        self.assertEqual(len(white_knight_2.get_controlled_squares()), 3)
        self.assertEqual(len(black_knight_1.get_controlled_squares()), 3)
        self.assertEqual(len(black_knight_2.get_controlled_squares()), 3)

        self.board.load_board_fen("8/8/3k4/2N3n1/3K4/8/8/8")
        white_knight = self.board.position[4, 2]
        black_knight = self.board.position[4, 6]
        self.assertEqual(len(white_knight.get_controlled_squares()), 8)
        self.assertEqual(len(black_knight.get_controlled_squares()), 6)

    def test_bishop_controlled_squares(self):
        wb1 = self.board.position[0,2]
        wb2 = self.board.position[0,5]
        bb1 = self.board.position[7,2]
        bb2 = self.board.position[7,5]
        self.assertEqual(len(wb1.get_controlled_squares()), 2)
        self.assertEqual(len(wb2.get_controlled_squares()), 2)
        self.assertEqual(len(bb1.get_controlled_squares()), 2)
        self.assertEqual(len(bb2.get_controlled_squares()), 2)

        self.board.load_board_fen("8/8/3k4/3b4/3K4/4B3/8/8")
        wb = self.board.position[2, 4]
        bb = self.board.position[4, 3]
        self.assertEqual(len(wb.get_controlled_squares()), 8)
        self.assertEqual(len(bb.get_controlled_squares()), 13)

    def test_queen_controlled_squares(self):
        wq = self.board.position[0,3]
        bq = self.board.position[7,3]
        self.assertEqual(len(wq.get_controlled_squares()), 5)
        self.assertEqual(len(bq.get_controlled_squares()), 5)

        self.board.load_board_fen("8/8/3k4/4q3/3K1Q2/8/8/8")
        wq = self.board.position[3, 5]
        bq = self.board.position[4, 4]
        self.assertEqual(len(wq.get_controlled_squares()), 19)
        self.assertEqual(len(bq.get_controlled_squares()), 20)
        
    def test_rook_controlled_squares(self):
        wr1 = self.board.position[0,0]
        wr2 = self.board.position[0,7]
        br1 = self.board.position[7,0]
        br2 = self.board.position[7,7]
        self.assertEqual(len(wr1.get_controlled_squares()), 2)
        self.assertEqual(len(wr2.get_controlled_squares()), 2)
        self.assertEqual(len(br1.get_controlled_squares()), 2)
        self.assertEqual(len(br2.get_controlled_squares()), 2)

        self.board.load_board_fen("8/8/3k1r2/4R3/3K4/8/8/8")
        wr = self.board.position[4, 4]
        br = self.board.position[5, 5]
        self.assertEqual(len(wr.get_controlled_squares()), 14)
        self.assertEqual(len(br.get_controlled_squares()), 11)

    def test_pawn_controlled_squares(self):
        for (_, _), piece in np.ndenumerate(self.board.position):
            if type(piece) == Pawn:
                # TODO: Currently considers the squares in front of the pawn controlled as well which will have to be fixed
                self.assertEqual(len(piece.get_controlled_squares()), 2)

        self.board.load_board_fen("8/4p3/3k1P2/4N3/3K4/8/8/8")
        wp = self.board.position[5, 5]
        bp = self.board.position[6, 4]
        wp.nr_moves = 2
        wp.calculate_controlled_squares(self.board.position)
        bp.nr_moves = 0
        bp.calculate_controlled_squares(self.board.position)
        print(wp.get_controlled_squares())
        self.assertEqual(len(wp.get_controlled_squares()), 2)
        self.assertEqual(len(bp.get_controlled_squares()), 2)