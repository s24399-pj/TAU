import unittest

from board import Board
from player import Player

class TestGame(unittest.TestCase):
    def setUp(self):
        self.board = Board(rows=9, cols=9, obstacle_ratio=0.2)
        self.player = Player(self.board.start, self.board)

    def test_player_reaches_goal(self):
        self.player.position = self.board.stop
        self.assertEqual(self.player.get_position(), self.board.stop)

if __name__ == '__main__':
    unittest.main()
