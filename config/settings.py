# config/settings.py
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

# Grid and screen settings
GRID_SIZE = 8  # 8x8 grid
TILE_SIZE = 80  # Tile size
MARGIN = 5  # Margin between tiles
SCREEN_WIDTH = GRID_SIZE * (TILE_SIZE + MARGIN) + MARGIN
SCREEN_HEIGHT = SCREEN_WIDTH  # Square window
FPS = 60

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font path
# FONT_PATH = "assets/fonts/game_font.ttf"
FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'game_font.ttf')
IMAGE_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'player.png')


# Color dictionary for different values
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}