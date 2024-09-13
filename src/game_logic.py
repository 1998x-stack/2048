# src/game_logic.py
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import pygame, random
from config.settings import TILE_COLORS, TILE_SIZE, MARGIN, GRID_SIZE
import numpy as np

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
    new_row = [num for num in row if num != 0]
    merged = False
    for i in range(1, len(new_row)):
        if new_row[i] == new_row[i - 1]:
            new_row[i - 1] *= 2
            new_row[i] = 0
            merged = True
    new_row = [num for num in new_row if num != 0]
    if len(new_row) < len(row):
        merged = True
    row[:] = new_row + [0] * (len(row) - len(new_row))
    return merged

def get_max_value(grid):
    """
    获取当前网格中的最大数字。
    """
    return max(max(max(row) for row in grid), 2)

def poisson_probabilities(max_value):
    """
    生成 2 的指数数字的泊松分布概率。
    
    Args:
        max_value (int): 当前网格中的最大数字。
    
    Returns:
        list: 包含可能生成的 2 的指数及其泊松分布概率。
    """
    powers_of_two = [2**i for i in range(1, int(np.log2(max_value)) + 1)]  # 生成从2到最大值的2的指数
    lambda_value = len(powers_of_two) / 2  # 泊松分布的λ值，数字越大概率越低
    probabilities = np.random.poisson(lambda_value, len(powers_of_two))
    
    # 正规化概率为 0 到 1 之间
    total_prob = sum(probabilities)
    if total_prob == 0:
        probabilities = [1/len(probabilities)] * len(probabilities)  # 避免全零的情况
    else:
        probabilities = [p / total_prob for p in probabilities]  # 正规化

    return powers_of_two, probabilities

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
        print("没有空白格子了!")
        return False  # 没有空位，返回 False
    
    # 获取当前网格中的最大值
    max_value = get_max_value(grid)
    
    # 生成基于泊松分布的可能数字和其概率
    possible_values, probabilities = poisson_probabilities(max_value)
    
    # 根据泊松分布的概率随机选择一个数字
    new_value = random.choices(possible_values, probabilities)[0]
    
    # 随机选择一个空格，并将新值放入该位置
    r, c = random.choice(empty_tiles)
    grid[r][c] = new_value
    
    return True


# Draw the grid and its tiles
def draw_grid(screen, grid):
    for r in range(8):
        for c in range(8):
            value = grid[r][c]
            rect = pygame.Rect(c * (TILE_SIZE + MARGIN) + MARGIN, r * (TILE_SIZE + MARGIN) + MARGIN, TILE_SIZE, TILE_SIZE)
            color = TILE_COLORS.get(value, (60, 58, 50))  # Default color for large numbers
            pygame.draw.rect(screen, color, rect)  # Color tiles based on their value
            if value != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
                
# Check if the game is over (no empty tiles and no mergeable tiles)
def is_game_over(grid):
    # Check if there are any empty tiles
    empty_tiles = [(r, c) for r in range(8) for c in range(8) if grid[r][c] == 0]
    if empty_tiles:
        return False

    # Check for possible merges in rows and columns
    for r in range(8):
        for c in range(8):
            if c < 7 and grid[r][c] == grid[r][c+1]:
                return False  # Adjacent columns can merge
            if r < 7 and grid[r][c] == grid[r+1][c]:
                return False  # Adjacent rows can merge

    return True  # No empty tiles and no merges possible