import unittest
from board import Board
from player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.board = Board(rows=5, cols=5, obstacle_ratio=0)
        self.board.start = (0, 0)
        self.board.stop = (4, 4)
        self.board.grid = [[' ' for _ in range(5)] for _ in range(5)]
        self.board.grid[0][0] = 'A'
        self.board.grid[4][4] = 'B'
        self.player = Player((2, 2), self.board)

    def test_initial_position(self):
        self.assertEqual(self.player.get_position(), (2, 2))

    def test_move_out_of_bounds(self):
        self.player.position = (0, 2)
        success, message = self.player.move('up')
        self.assertFalse(success)
        self.assertEqual(message, "Wyjście poza planszę.")

        self.player.position = (4, 2)
        success, message = self.player.move('down')
        self.assertFalse(success)
        self.assertEqual(message, "Wyjście poza planszę.")

        self.player.position = (2, 0)
        success, message = self.player.move('left')
        self.assertFalse(success)
        self.assertEqual(message, "Wyjście poza planszę.")

        self.player.position = (2, 4)
        success, message = self.player.move('right')
        self.assertFalse(success)
        self.assertEqual(message, "Wyjście poza planszę.")

    def test_move_into_obstacle(self):
        self.player.position = (2, 2)
        obstacle_pos = (2, 3)
        self.board.obstacles.add(obstacle_pos)
        self.board.grid[obstacle_pos[0]][obstacle_pos[1]] = 'X'

        success, message = self.player.move('right')
        self.assertFalse(success)
        self.assertEqual(message, "Napotkano przeszkodę.")

    def test_invalid_direction(self):
        invalid_directions = ['up-left', 'down-right', 'forward', 'backward', '', None, 123]
        for direction in invalid_directions:
            success, message = self.player.move(direction)
            self.assertFalse(success)
            self.assertEqual(message, "Nieznany kierunek ruchu.")

    def test_multiple_moves(self):
        moves = ['right', 'down', 'left', 'up']
        expected_positions = [
            (2, 2),
            (2, 3),
            (3, 3),
            (3, 2),
            (2, 2)
        ]
        for i, move in enumerate(moves, start=1):
            success, message = self.player.move(move)
            self.assertTrue(success)
            self.assertEqual(self.player.get_position(), expected_positions[i])

    def test_reach_stop(self):
        self.player.position = (3, 4)
        success, message = self.player.move('down')
        self.assertTrue(success)
        self.assertEqual(self.player.get_position(), self.board.stop)

    def test_reset_player_position(self):
        success, message = self.player.move('right')
        self.assertTrue(success)
        self.assertNotEqual(self.player.get_position(), self.board.start)

        self.player.position = self.board.start
        self.assertEqual(self.player.get_position(), self.board.start)

    def test_no_move_when_surrounded_by_obstacles(self):
        current_pos = (2, 2)
        self.player.position = current_pos
        surrounding_positions = [
            (1, 2),
            (3, 2),
            (2, 1),
            (2, 3)
        ]

        for pos in surrounding_positions:
            if self.board.is_within_bounds(pos) and pos != self.board.stop:
                self.board.obstacles.add(pos)
                self.board.grid[pos[0]][pos[1]] = 'X'

        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            success, message = self.player.move(direction)
            self.assertFalse(success)
            self.assertEqual(message, "Napotkano przeszkodę.")

    def test_move_after_blocked_path(self):
        self.player.position = (2, 2)
        obstacle_pos = (2, 3)
        self.board.obstacles.add(obstacle_pos)
        self.board.grid[obstacle_pos[0]][obstacle_pos[1]] = 'X'

        success, message = self.player.move('right')
        self.assertFalse(success)
        self.assertEqual(message, "Napotkano przeszkodę.")

        success, message = self.player.move('down')
        self.assertTrue(success)
        self.assertEqual(message, "Ruch wykonany.")

        success, message = self.player.move('right')
        self.assertTrue(success)

    def test_move_back_and_forth(self):
        self.player.position = (2, 2)
        success, message = self.player.move('right')
        self.assertTrue(success)
        expected_position = (2, 3)
        self.assertEqual(self.player.get_position(), expected_position)

        success, message = self.player.move('left')
        self.assertTrue(success)
        self.assertEqual(self.player.get_position(), (2, 2))

    def test_player_does_not_overwrite_stop(self):
        self.player.position = (4, 3)
        success, message = self.player.move('right')
        self.assertTrue(success)
        self.assertEqual(self.player.get_position(), self.board.stop)
        self.assertEqual(self.board.grid[4][4], 'B')


if __name__ == '__main__':
    unittest.main()
