# src/game_logic.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import math

import pygame, random
from config.settings import TILE_COLORS, TILE_SIZE, MARGIN, GRID_SIZE
from src.logger import log_event
from src.assets_loader import load_font

def move_left(grid):
    moved = False
    for row in grid:
        if merge_row(row):
            moved = True
    return moved

def move_right(grid):
    moved = False
    for row in grid:
        row.reverse()
        if merge_row(row):
            moved = True
        row.reverse()
    return moved

def move_up(grid):
    moved = False
    for col in range(len(grid)):
        column = [grid[row][col] for row in range(len(grid))]
        if merge_row(column):
            moved = True
        for row in range(len(grid)):
            grid[row][col] = column[row]
    return moved

def move_down(grid):
    moved = False
    for col in range(len(grid)):
        column = [grid[row][col] for row in range(len(grid))]
        column.reverse()
        if merge_row(column):
            moved = True
        column.reverse()
        for row in range(len(grid)):
            grid[row][col] = column[row]
    return moved

def merge_row(row):
    # Compress non-zero tiles, then merge adjacent equal tiles once.
    # A tile produced by a merge must NOT merge again in the same move, so the
    # merged element is zeroed and skipped by the overlap check.
    new_row = [num for num in row if num != 0]
    for i in range(1, len(new_row)):
        if new_row[i] == new_row[i - 1]:
            new_row[i - 1] *= 2
            new_row[i] = 0
    new_row = [num for num in new_row if num != 0]
    # Pad with zeros back to the original row length.
    new_row += [0] * (len(row) - len(new_row))
    # A row only "moved" if its contents actually changed (slid or merged).
    changed = new_row != list(row)
    row[:] = new_row
    return changed

def get_max_value(grid):
    """
    获取当前网格中的最大数字。
    """
    return max(max(max(row) for row in grid), 2)

def _spawn_weights(max_value):
    """Return (values, weights) for powers of two up to max_value.

    weight(2**i) = 2**(1-i): larger values are strictly rarer. The list is
    normalized so weights sum to 1. max_value >= 2, so there is always at
    least [2] with weight 1.0.
    """
    k = max(1, int(math.log2(max_value)))
    values = [2 ** i for i in range(1, k + 1)]
    weights = [2 ** (1 - i) for i in range(1, k + 1)]
    total = sum(weights)
    if total == 0:
        weights = [1.0 / len(values)] * len(values)
    else:
        weights = [w / total for w in weights]
    return values, weights

# Add a random tile (2 or 4) to an empty spot on the grid
def add_random_tile(grid):
    """
    在网格中随机添加一个新的数字。可能生成的数字为当前最大值及以下的2的指数。
    
    Args:
        grid (list): 游戏网格，8x8的二维列表。
        
    Returns:
        bool: 如果成功添加新数字，则返回True；如果没有空位，则返回False。
    """
    # 找到所有空白格子
    empty_tiles = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 0]
    
    if not empty_tiles:
        log_event("No empty cells available; cannot add a tile.")
        return False  # 没有空位，返回 False
    
    # 获取当前网格中的最大值
    max_value = get_max_value(grid)
    
    # 生成可能数字及其确定性递减权重
    possible_values, probabilities = _spawn_weights(max_value)
    
    # Choose a value weighted so larger tiles are rarer (see _spawn_weights)
    new_value = random.choices(possible_values, probabilities)[0]
    
    # 随机选择一个空格，并将新值放入该位置
    r, c = random.choice(empty_tiles)
    grid[r][c] = new_value
    
    return True


# Cache rendered fonts by pixel size so we create them once, not per tile per frame.
# Cached Font objects are only valid while the pygame font subsystem is initialized;
# calling pygame.quit() frees them, so the cache must be cleared on restart to avoid
# reusing freed SDL memory (a use-after-free segfault).
_font_cache = {}

def reset_font_cache():
    """Drop all cached fonts. Call after pygame.quit() / a fresh pygame.init()."""
    _font_cache.clear()

def _get_font(size):
    """Return a cached font object, preferring the bundled game font."""
    if size not in _font_cache:
        font = load_font(size)
        if font is None:
            font = pygame.font.Font(None, size)  # fall back to default pygame font
        _font_cache[size] = font
    return _font_cache[size]

def _font_size_for(value):
    """Scale the font size so large numbers still fit inside a tile."""
    return max(12, int(TILE_SIZE * 0.8 / max(1, len(str(value)))))

# Draw the grid and its tiles
def draw_grid(screen, grid):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            value = grid[r][c]
            rect = pygame.Rect(c * (TILE_SIZE + MARGIN) + MARGIN, r * (TILE_SIZE + MARGIN) + MARGIN, TILE_SIZE, TILE_SIZE)
            color = TILE_COLORS.get(value, (60, 58, 50))  # Default color for large numbers
            pygame.draw.rect(screen, color, rect)  # Color tiles based on their value
            if value != 0:
                font = _get_font(_font_size_for(value))
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
                
# Check if the game is over (no empty tiles and no mergeable tiles)
def is_game_over(grid):
    size = min(len(grid), GRID_SIZE)
    # Check if there are any empty tiles
    empty_tiles = [(r, c) for r in range(size) for c in range(size) if grid[r][c] == 0]
    if empty_tiles:
        return False

    # Check for possible merges in rows and columns
    for r in range(size):
        for c in range(size):
            if c < size - 1 and grid[r][c] == grid[r][c+1]:
                return False  # Adjacent columns can merge
            if r < size - 1 and grid[r][c] == grid[r+1][c]:
                return False  # Adjacent rows can merge

    return True  # No empty tiles and no merges possible
