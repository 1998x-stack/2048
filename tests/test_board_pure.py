"""Tests for board rules without pygame or a display server."""

import random
import unittest

from src.board import (
    _spawn_weights,
    add_random_tile,
    get_max_value,
    is_game_over,
    merge_row,
    move_down,
    move_left,
    move_right,
    move_up,
)


class BoardRulesTest(unittest.TestCase):
    def test_merge_once(self):
        for before, expected in (
            ([2, 2, 2, 2], [4, 4, 0, 0]),
            ([2, 2, 4, 4], [4, 8, 0, 0]),
            ([2, 0, 2, 4], [4, 4, 0, 0]),
            ([0, 0, 0, 0], [0, 0, 0, 0]),
        ):
            with self.subTest(before=before):
                row = before[:]
                self.assertEqual(merge_row(row), row != before)
                self.assertEqual(row, expected)

    def test_move_left_processes_every_row(self):
        board = [[0, 2, 0, 0], [0, 4, 0, 0], [0, 8, 0, 0]]
        self.assertTrue(move_left(board))
        self.assertEqual(board, [[2, 0, 0, 0], [4, 0, 0, 0], [8, 0, 0, 0]])
        self.assertFalse(move_left(board))

    def test_move_right_processes_every_row(self):
        board = [[2, 0, 0, 0], [4, 4, 0, 0]]
        self.assertTrue(move_right(board))
        self.assertEqual(board, [[0, 0, 0, 2], [0, 0, 0, 8]])
        self.assertFalse(move_right(board))

    def test_vertical_rectangular(self):
        up = [[2, 0, 4], [2, 0, 4], [0, 0, 0]]
        down = [row[:] for row in up]
        self.assertTrue(move_up(up))
        self.assertEqual(up, [[4, 0, 8], [0, 0, 0], [0, 0, 0]])
        self.assertTrue(move_down(down))
        self.assertEqual(down, [[0, 0, 0], [0, 0, 0], [4, 0, 8]])

    def test_empty_board_moves_are_safe(self):
        for move in (move_left, move_right, move_up, move_down):
            self.assertFalse(move([]))

    def test_game_over_uses_actual_board_dimensions(self):
        locked = [[2, 4, 8, 16, 32], [4, 8, 16, 32, 64]]
        self.assertTrue(is_game_over(locked))
        locked[0][4] = 0
        self.assertFalse(is_game_over(locked))
        self.assertFalse(is_game_over([]))

    def test_game_over_recognizes_vertical_merge(self):
        self.assertFalse(is_game_over([[2, 4], [2, 8]]))

    def test_spawn_on_full_board_noop(self):
        full = [[2, 4], [8, 16]]
        self.assertFalse(add_random_tile(full, rng=random.Random(1)))
        self.assertEqual(full, [[2, 4], [8, 16]])

    def test_seeded_spawn_independent_of_global_random(self):
        before = random.getstate()
        a = [[0] * 4 for _ in range(4)]
        b = [[0] * 4 for _ in range(4)]
        add_random_tile(a, rng=random.Random(7))
        add_random_tile(b, rng=random.Random(7))
        self.assertEqual(a, b)
        self.assertEqual(random.getstate(), before)
        self.assertEqual(sum(tile != 0 for row in a for tile in row), 1)

    def test_spawn_distribution(self):
        for maximum in (2, 4, 16, 2048):
            values, weights = _spawn_weights(maximum)
            self.assertEqual(values[0], 2)
            self.assertLessEqual(values[-1], maximum)
            self.assertAlmostEqual(sum(weights), 1)
            self.assertTrue(all(a > b for a, b in zip(weights, weights[1:])))
        self.assertEqual(get_max_value([[0]]), 2)


if __name__ == "__main__":
    unittest.main()
