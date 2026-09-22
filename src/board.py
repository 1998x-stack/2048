"""Pure 2048 board rules; no Pygame or filesystem dependencies.

Moves mutate the supplied board in place and return whether any cell changed.
The existing variant uses an 8x8 board and weighted spawns based on its
current maximum tile; both behaviors are preserved by the UI.
"""

import random
from typing import List

Board = List[List[int]]


def merge_row(row: List[int]) -> bool:
    """Slide left and merge each original tile at most once."""
    original = row[:]
    nonzero = [value for value in row if value]
    merged = []
    index = 0
    while index < len(nonzero):
        if index + 1 < len(nonzero) and nonzero[index] == nonzero[index + 1]:
            merged.append(nonzero[index] * 2)
            index += 2
        else:
            merged.append(nonzero[index])
            index += 1
    row[:] = merged + [0] * (len(row) - len(merged))
    return row != original


def move_left(grid: Board) -> bool:
    return any_changes(merge_row(row) for row in grid)


def move_right(grid: Board) -> bool:
    changed = False
    for row in grid:
        reversed_row = row[::-1]
        moved = merge_row(reversed_row)
        row[:] = reversed_row[::-1]
        changed = moved or changed
    return changed


def _move_vertical(grid: Board, *, reverse: bool) -> bool:
    if not grid:
        return False
    changed = False
    for column_index in range(len(grid[0])):
        column = [row[column_index] for row in grid]
        if reverse:
            column.reverse()
        moved = merge_row(column)
        if reverse:
            column.reverse()
        for row, value in zip(grid, column):
            row[column_index] = value
        changed = moved or changed
    return changed


def move_up(grid: Board) -> bool:
    return _move_vertical(grid, reverse=False)


def move_down(grid: Board) -> bool:
    return _move_vertical(grid, reverse=True)


def any_changes(changes) -> bool:
    """Consume every move; short-circuiting would skip later rows."""
    changed = False
    for item in changes:
        changed = item or changed
    return changed


def get_max_value(grid: Board) -> int:
    return max(2, max((tile for row in grid for tile in row), default=2))


def _spawn_weights(max_value: int):
    """Return descending normalized probabilities for powers of two."""
    highest = max(1, max_value.bit_length() - 1)
    values = [1 << power for power in range(1, highest + 1)]
    weights = [2.0 ** (1 - power) for power in range(1, highest + 1)]
    total = sum(weights)
    return values, [weight / total for weight in weights]


def add_random_tile(grid: Board, rng=None) -> bool:
    """Spawn on an empty cell using the variant's weighted distribution."""
    empty = [(r, c) for r, row in enumerate(grid) for c, value in enumerate(row) if value == 0]
    if not empty:
        return False
    source = random if rng is None else rng
    values, weights = _spawn_weights(get_max_value(grid))
    tile = source.choices(values, weights=weights, k=1)[0]
    row, column = source.choice(empty)
    grid[row][column] = tile
    return True


def is_game_over(grid: Board) -> bool:
    """A populated rectangular board is lost only when no moves remain."""
    if not grid or not grid[0]:
        return False
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value == 0:
                return False
            if col_index + 1 < len(row) and value == row[col_index + 1]:
                return False
            if row_index + 1 < len(grid) and col_index < len(grid[row_index + 1]):
                if value == grid[row_index + 1][col_index]:
                    return False
    return True
