"""Pygame application loop and terminal-state presentation."""

import pygame

from config.settings import BLACK, FPS, GRID_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from src.event_handler import is_quit_event
from src.game_logic import (
    add_random_tile,
    draw_grid,
    is_game_over,
    move_down,
    move_left,
    move_right,
    move_up,
    reset_font_cache,
)
from src.logger import log_event, setup_logger
from src.utils import check_victory


def evaluate_state(grid):
    """Return (finished, message) for the current board."""
    if check_victory(grid):
        return True, "You Win!"
    if is_game_over(grid):
        return True, "Game Over"
    return False, None


def _move_grid(grid, key):
    """Apply a directional key and report whether the board changed."""
    moves = {
        pygame.K_LEFT: move_left,
        pygame.K_RIGHT: move_right,
        pygame.K_UP: move_up,
        pygame.K_DOWN: move_down,
    }
    move = moves.get(key)
    return move(grid) if move is not None else False


def _show_overlay(screen, message):
    """Draw the result and the exit hint."""
    title = pygame.font.Font(None, 64).render(message, True, BLACK)
    screen.blit(
        title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    )
    hint = pygame.font.Font(None, 30).render(
        "Press ENTER or ESC to exit", True, (80, 80, 80)
    )
    screen.blit(
        hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    )


def run_game(initial_grid=None):
    """Run the UI; an optional supplied board supports integration testing."""
    pygame.init()
    try:
        setup_logger()
        reset_font_cache()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"2048 Game - {GRID_SIZE}x{GRID_SIZE} Grid")
        clock = pygame.time.Clock()

        grid = initial_grid if initial_grid is not None else [
            [0] * GRID_SIZE for _ in range(GRID_SIZE)
        ]
        if initial_grid is None:
            add_random_tile(grid)
            add_random_tile(grid)

        finished, message = evaluate_state(grid)
        running = True
        while running:
            for event in pygame.event.get():
                if is_quit_event(event):
                    log_event("Game quit by user.")
                    running = False
                    break

                if finished:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        log_event("Game finished; exiting by user.")
                        running = False
                        break
                    continue

                if event.type == pygame.KEYDOWN and _move_grid(grid, event.key):
                    log_event("Valid movement")
                    add_random_tile(grid)
                    # Multiple key events can arrive in one frame. Once the board
                    # is terminal, subsequent queued movement must be ignored.
                    finished, message = evaluate_state(grid)

            if not running:
                break
            screen.fill(WHITE)
            draw_grid(screen, grid)
            if finished:
                _show_overlay(screen, message)
            pygame.display.flip()
            clock.tick(FPS)
    finally:
        pygame.quit()
