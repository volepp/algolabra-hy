import unittest
from board import *

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_make_move(self):
        move = "e2e4"
        self.board.make_move(move)
        self.assertEqual(len(self.board.moves), 1)
        self.assertIn(move, self.board.moves)

    def test_update_moves(self):
        moves = "e2e4 e7e5 g1f3"
        self.board.update_moves(moves)
        self.assertEqual(len(self.board.moves), 3)
        self.assertIn("e2e4", self.board.moves)
        self.assertIn("e7e5", self.board.moves)
        self.assertIn("g1f3", self.board.moves)

        # Test that resets game with empty input
        self.board.update_moves("")
        print(self.board.moves)
        self.assertEqual(len(self.board.moves), 0)

    def test_last_move(self):
        self.assertIsNone(self.board.get_last_move())

        self.board.make_move("e2e4")
        self.assertEqual("e2e4", self.board.get_last_move())

        self.board.make_move("e7e5")
        self.assertEqual("e7e5", self.board.get_last_move())

    def test_next_move_color(self):
        self.assertEqual(self.board.next_move_color(), Color.White)
        self.board.make_move("e2e4")
        self.assertEqual(self.board.next_move_color(), Color.Black)
        self.board.make_move("e7e5")
        self.assertEqual(self.board.next_move_color(), Color.White)
        self.board.make_move("g1f3")
        self.assertEqual(self.board.next_move_color(), Color.Black)
        self.board.update_moves("")
        self.assertEqual(self.board.next_move_color(), Color.White)

    def test_is_over(self):
        # TODO implement
        self.assertFalse(self.board.is_over())

    def test_get_result(self):
        # TODO implement
        self.assertIsNone(self.board.get_result())