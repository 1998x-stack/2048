# src/game.py
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, GRID_SIZE
from src.game_logic import move_left, move_right, move_up, move_down, add_random_tile, draw_grid, is_game_over
from src.logger import setup_logger, log_event
from src.event_handler import handle_events

# Initialize Pygame and the logger
def run_game():
    pygame.init()
    setup_logger()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"2048 Game - {GRID_SIZE}x{GRID_SIZE} Grid")
    clock = pygame.time.Clock()

    # Create the 8x8 grid
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_random_tile(grid)  # Generate the first random tile
    add_random_tile(grid)  # Generate the second random tile

    running = True
    while running:
        screen.fill(WHITE)

        # Handle input events (using event.get() instead of get_pressed())
        for event in pygame.event.get():
            running = handle_events(event)
            moved = False  # Tracks whether any movement happened

            if event.type == pygame.KEYDOWN:
                # Handle movement keys once per keydown event
                if event.key == pygame.K_LEFT:
                    moved = move_left(grid)
                    log_event(f"Moved left: {moved}")  # Debugging info
                elif event.key == pygame.K_RIGHT:
                    moved = move_right(grid)
                    log_event(f"Moved right: {moved}")  # Debugging info
                elif event.key == pygame.K_UP:
                    moved = move_up(grid)
                    log_event(f"Moved up: {moved}")  # Debugging info
                elif event.key == pygame.K_DOWN:
                    moved = move_down(grid)
                    log_event(f"Moved down: {moved}")  # Debugging info

                # After a valid move, add a random tile
                if moved:
                    add_random_tile(grid)

        # Check if the game is over
        if is_game_over(grid):
            log_event("游戏结束！没有可用的格子或合并。")
            running = False  # End the game

        # Draw the grid and tiles
        draw_grid(screen, grid)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
