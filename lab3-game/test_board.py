import unittest
from board import Board


class TestBoard(unittest.TestCase):
    def test_board_size(self):
        board = Board(rows=5, cols=5)
        self.assertEqual(len(board.grid), 5)
        self.assertEqual(len(board.grid[0]), 5)

    def test_start_stop_unique(self):
        board = Board(rows=5, cols=5)
        self.assertNotEqual(board.start, board.stop)

    def test_obstacle_placement(self):
        board = Board(rows=5, cols=5, obstacle_ratio=0.2)
        expected_obstacles = int(25 * 0.2)
        self.assertEqual(len(board.obstacles), expected_obstacles)

    def test_obstacles_not_on_start_stop(self):
        board = Board(rows=5, cols=5, obstacle_ratio=0.2)
        self.assertNotIn(board.start, board.obstacles)
        self.assertNotIn(board.stop, board.obstacles)


if __name__ == '__main__':
    unittest.main()
