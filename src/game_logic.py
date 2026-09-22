"""Pygame tile rendering and backward-compatible exports of board rules."""

import pygame

from config.settings import GRID_SIZE, MARGIN, TILE_COLORS, TILE_SIZE
from src.assets_loader import load_font
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

# Pygame font objects become invalid after pygame.quit(); reset on each run.
_font_cache = {}


def reset_font_cache():
    """Discard fonts from the previous Pygame session."""
    _font_cache.clear()


def _get_font(size):
    if size not in _font_cache:
        _font_cache[size] = load_font(size) or pygame.font.Font(None, size)
    return _font_cache[size]


def _font_size_for(value):
    """Keep large tile values readable without shrinking below 12 pixels."""
    return max(12, int(TILE_SIZE * 0.8 / max(1, len(str(value)))))


def draw_grid(screen, grid):
    """Render the configured board without changing its contents."""
    for row_index in range(GRID_SIZE):
        for column_index in range(GRID_SIZE):
            value = grid[row_index][column_index]
            rect = pygame.Rect(
                column_index * (TILE_SIZE + MARGIN) + MARGIN,
                row_index * (TILE_SIZE + MARGIN) + MARGIN,
                TILE_SIZE,
                TILE_SIZE,
            )
            pygame.draw.rect(screen, TILE_COLORS.get(value, (60, 58, 50)), rect)
            if value:
                font = _get_font(_font_size_for(value))
                text = font.render(str(value), True, (0, 0, 0))
                screen.blit(text, text.get_rect(center=rect.center))
