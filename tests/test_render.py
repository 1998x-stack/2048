# tests/test_render.py
# Rendering tests. These use the real pygame with a dummy video/audio driver
# (headless). The game initializes pygame once and keeps it for the whole run,
# so the drawing tests share a single pygame session.

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame

from config.settings import GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, MARGIN
from src.game_logic import draw_grid, _font_size_for, reset_font_cache

SCREEN = None  # reused surface for the single session


def setup_session():
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def test_font_size_scales_down_for_large_numbers():
    assert _font_size_for(2) > _font_size_for(2048) > _font_size_for(131072)
    assert _font_size_for(131072) >= 12  # never goes below the floor


def test_draw_grid_empty_board():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    draw_grid(SCREEN, grid)


def test_draw_grid_with_large_values():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    grid[0][0] = 2
    grid[0][1] = 2048
    grid[7][7] = 131072  # beyond the color table -> default color path
    draw_grid(SCREEN, grid)


def test_draw_grid_all_full():
    grid = [[2 * (r + c + 1) for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
    draw_grid(SCREEN, grid)


def test_font_cache_survives_within_session_but_resets_on_restart():
    # Draw once to populate the font cache.
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    grid[0][0] = 2048
    draw_grid(SCREEN, grid)

    # Simulate a game restart: quit (frees SDL font memory), then re-init.
    pygame.quit()
    reset_font_cache()  # MUST be called, otherwise cached fonts are use-after-free
    setup_session()

    # Drawing again (which would recreate fonts) must not crash.
    draw_grid(SCREEN, grid)
    pygame.quit()
    print("restart-safe OK")


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    # Font-size scaling is pure and needs no session.
    setup_session()
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except Exception:
            import traceback
            traceback.print_exc()
            print(f"FAIL  {t.__name__}")
    print(f"\n{passed}/{len(tests)} passed")
    sys.exit(0 if passed == len(tests) else 1)


if __name__ == "__main__":
    main()