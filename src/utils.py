# src/utils.py
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

def reset_game(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            grid[row][col] = 0  # Reset all tiles to 0

def check_victory(grid):
    """Return True once any tile reaches the 2048 target (or beyond).

    A tile can be spawned/merged directly past 2048, so victory is triggered
    at ``>= 2048`` (see README: "reach 2048 or even beyond").
    """
    for row in grid:
        for tile in row:
            if tile >= 2048:
                return True
    return False