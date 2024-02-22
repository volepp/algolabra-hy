import unittest
import numpy as np
from board import Board
from board.piece import Move, Color
from engine import Engine

class TestEngine(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.engine = Engine()
        self.engine.max_depth = 2

    def test_simple_checkmate_in_one(self):
        self.board.load_board_fen("3k4/8/3K4/8/6Q1/8/8/8")
        move = self.engine.make_move(self.board)
        self.assertEqual(move, Move.parse_uci("g4d7"))

    def test_more_pieces_checkmate_in_one(self):
        self.board.load_board_fen("r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR")
        move = self.engine.make_move(self.board)
        self.assertEqual(move, move.parse_uci("h5f7"))

    def test_checkmate_in_two(self):
        # https://www.chess.com/puzzles/problem/564204
        self.board.load_board_fen("8/5ppk/p2R4/1p6/5PK1/1P5N/1r1p4/8")
        self.engine.max_depth = 3
        move = self.engine.make_move(self.board)
        self.assertEqual(move, move.parse_uci("h3g5"))

    def test_pawn_checkmate_in_two(self):
        # https://www.chess.com/puzzles/problem/480308
        self.board.load_board_fen("8/8/4ppp1/3p1k1p/5P2/4PKPP/8/8")
        self.engine.max_depth = 3
        move = self.engine.make_move(self.board)
        self.assertEqual(move, move.parse_uci("g3g4"))
        self.board.play_move(move)
        self.board.play_move(Move.parse_uci("h5g4"))
        move = self.engine.make_move(self.board)
        self.assertEqual(move, move.parse_uci("h3g4"))
    
    def test_sort_moves_by_potential(self):
        self.board.play_move(Move.parse_uci("e2e4"))
        self.board.play_move(Move.parse_uci("a7a5"))
        self.board.play_move(Move.parse_uci("b2b4"))
        legal_moves = self.board.get_legal_moves(Color.Black)
        self.engine.sort_moves_by_evaluation(self.board, legal_moves)
        # Capture should be the most interesting
        self.assertEqual(legal_moves[0], Move.parse_uci("a5b4"))