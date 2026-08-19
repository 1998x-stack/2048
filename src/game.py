# src/game.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, GRID_SIZE
from src.game_logic import move_left, move_right, move_up, move_down, add_random_tile, draw_grid, is_game_over, reset_font_cache
from src.logger import setup_logger, log_event
from src.event_handler import is_quit_event
from src.utils import check_victory


def evaluate_state(grid):
    """Return ``(finished, message)`` describing the board's terminal state.

    ``finished`` is True once the game is won or lost; ``message`` is the text
    to draw as an overlay (None while the game is still in progress).
    """
    if check_victory(grid):
        return True, "You Win!"
    if is_game_over(grid):
        return True, "Game Over"
    return False, None


def _move_grid(grid, key):
    """Apply the movement for *key* and return whether the grid changed."""
    if key == pygame.K_LEFT:
        return move_left(grid)
    if key == pygame.K_RIGHT:
        return move_right(grid)
    if key == pygame.K_UP:
        return move_up(grid)
    if key == pygame.K_DOWN:
        return move_down(grid)
    return False


def _show_overlay(screen, message):
    """Draw a centered game-over / victory message with an exit hint."""
    title = pygame.font.Font(None, 64).render(message, True, BLACK)
    rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(title, rect)

    hint = pygame.font.Font(None, 30).render(
        "Press ENTER or ESC to exit", True, (80, 80, 80)
    )
    rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(hint, rect)


def run_game(initial_grid=None):
    """Run the game. *initial_grid* overrides the starting board (used by tests)."""
    pygame.init()
    setup_logger()
    reset_font_cache()  # discard any fonts cached by a previous run that quit() freed

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"2048 Game - {GRID_SIZE}x{GRID_SIZE} Grid")
    clock = pygame.time.Clock()

    # Create the 8x8 grid
    grid = initial_grid if initial_grid is not None else [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    if initial_grid is None:
        add_random_tile(grid)  # Generate the first random tile
        add_random_tile(grid)  # Generate the second random tile

    running = True
    finished, message = False, None

    while running:
        screen.fill(WHITE)

        # Handle input events (using event.get() instead of get_pressed())
        for event in pygame.event.get():
            if is_quit_event(event):        # window close or ESC
                running = False
                log_event("Game quit by user.")
                continue

            # On the finished screen only ENTER leaves the game.
            if finished:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False
                    log_event("Game finished; exiting by user.")
                continue

            # Movement is only meaningful while the game is in progress.
            if event.type == pygame.KEYDOWN:
                moved = _move_grid(grid, event.key)
                if moved:
                    log_event(f"Moved: moved={moved}")
                    add_random_tile(grid)

        # Update the terminal state (victory / game over) and overlay.
        if not finished:
            finished, message = evaluate_state(grid)

        draw_grid(screen, grid)
        if finished:
            _show_overlay(screen, message)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
