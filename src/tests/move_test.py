import unittest
import numpy as np
from board.piece import Move

class TestMove(unittest.TestCase):

    def test_parse_uci(self):
        move = Move.parse_uci("e2e4")
        self.assertTrue(np.all(move.from_square == np.array([1,4])))
        self.assertTrue(np.all(move.to_square == np.array([3,4])))

    def test_error_on_invalid_uci(self):
        with self.assertRaises(ValueError):
            Move.parse_uci("asdf")

    def test_equal(self):
        move1 = Move(np.array([1,1]), np.array([2,1]))
        move2 = Move(np.array([1,1]), np.array([2,1]))
        self.assertEqual(move1, move2)
        move2.from_square = np.array([0,1])
        self.assertNotEqual(move1, move2)
        move2.from_square = np.array([1,1])
        move2.to_square = np.array([3,1])
        self.assertNotEqual(move1, move2)