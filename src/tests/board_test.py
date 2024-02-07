import unittest
import numpy as np
from board import *
from board.piece import *

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_play_move(self):
        move = Move.parse_uci("e2e4")
        self.board.play_move(move)
        self.assertEqual(len(self.board.moves), 1)
        self.assertIn(move, self.board.moves)

    def test_play_illegal_move(self):
        move = Move.parse_uci("e2e5")
        with self.assertRaises(ValueError):
            self.board.play_move(move)

    def test_update_moves(self):
        moves = "e2e4 e7e5 g1f3"
        self.board.update_moves(moves)
        self.assertEqual(len(self.board.moves), 3)
        self.assertIn(Move.parse_uci("e2e4"), self.board.moves)
        self.assertIn(Move.parse_uci("e7e5"), self.board.moves)
        self.assertIn(Move.parse_uci("g1f3"), self.board.moves)

        # Test that resets game with empty input
        self.board.update_moves("")
        self.assertEqual(len(self.board.moves), 0)

    def test_last_move(self):
        self.assertIsNone(self.board.get_last_move())

        move = Move.parse_uci("e2e4")
        self.board.play_move(move)
        self.assertEqual(move, self.board.get_last_move())

        move = Move.parse_uci("e7e5")
        self.board.play_move(move)
        self.assertEqual(move, self.board.get_last_move())

    def test_next_move_color(self):
        self.assertEqual(self.board.next_move_color(), Color.White)
        self.board.play_move(Move.parse_uci("e2e4"))
        self.assertEqual(self.board.next_move_color(), Color.Black)
        self.board.play_move(Move.parse_uci("e7e5"))
        self.assertEqual(self.board.next_move_color(), Color.White)
        self.board.play_move(Move.parse_uci("g1f3"))
        self.assertEqual(self.board.next_move_color(), Color.Black)
        self.board.update_moves("")
        self.assertEqual(self.board.next_move_color(), Color.White)

    def test_get_legal_moves(self):
        # Both sides have 20 possible moves in the starting position
        legal_moves = self.board.get_legal_moves(Color.White)
        self.assertEqual(len(legal_moves), 20)
        legal_moves = self.board.get_legal_moves(Color.Black)
        self.assertEqual(len(legal_moves), 20)

        # Load position which only has one legal move to escape check
        self.board.load_board_fen("2K5/3q2n1/2k5/5P2/3b4/1pQ3N1/8/8") 
        legal_moves = self.board.get_legal_moves(Color.White)
        self.assertEqual(len(legal_moves), 1)
        self.assertEqual(legal_moves[0], Move.parse_uci("c8b8"))

    def test_is_check(self):
        # Shouldn't be check in the beginning
        self.assertFalse(self.board.position.is_color_in_check(Color.White))
        self.assertFalse(self.board.position.is_color_in_check(Color.Black))

    def test_is_over(self):
        # Shouldn't be over when just started
        self.assertFalse(self.board.is_game_over())

        self.board.load_board_fen("8/8/8/8/8/3k4/3q4/3K4") # Checkmate position
        self.assertTrue(self.board.is_game_over())

    def test_get_result(self):
        # Should return None while ongoing
        self.assertIsNone(self.board.get_result())

    def test_load_fen(self):
        fen = "6k1/3b4/1rR2n2/5N2/2pB2Q1/4q1P1/1K6/8"
        self.board.load_board_fen(fen)

        nr_pieces = self.board.position[self.board.position != None].size
        self.assertEqual(nr_pieces, 12)

        self.assertEqual(self.board.position[1, 1], King(None, Color.White))
        self.assertEqual(self.board.position[2, 6], Pawn(None, Color.White))
        self.assertEqual(self.board.position[3, 3], Bishop(None, Color.White))
        self.assertEqual(self.board.position[3, 6], Queen(None, Color.White))
        self.assertEqual(self.board.position[4, 5], Knight(None, Color.White))
        self.assertEqual(self.board.position[5, 2], Rook(None, Color.White))

        self.assertEqual(self.board.position[7, 6], King(None, Color.Black))
        self.assertEqual(self.board.position[3, 2], Pawn(None, Color.Black))
        self.assertEqual(self.board.position[6, 3], Bishop(None, Color.Black))
        self.assertEqual(self.board.position[2, 4], Queen(None, Color.Black))
        self.assertEqual(self.board.position[5, 5], Knight(None, Color.Black))
        self.assertEqual(self.board.position[5, 1], Rook(None, Color.Black))

    def test_fen_output(self):
        fen = "6k1/3b4/1rR2n2/5N2/2pB2Q1/4q1P1/1K6/8"
        self.board.load_board_fen(fen)
        self.assertEqual(self.board.board_fen(), fen)