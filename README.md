# 2048 Game

This is an implementation of the classic 2048 game using Python and Pygame. The game grid is 8x8, and you can use arrow keys to merge tiles and attempt to reach the 2048 tile (or even beyond). The game ends when no more moves are possible.

https://github.com/1998x-stack/2048

## Project Structure

```bash
.
├── assets                  # Folder containing game assets
│   ├── fonts               # Fonts used in the game
│   │   └── game_font.ttf   # Default font for the game
│   └── images              # Images used in the game
│       └── player.png      # Placeholder image for future use
├── config                  # Game configuration files
│   └── settings.py         # Game settings (screen size, tile size, colors)
├── logs                    # Folder containing logs
│   └── game.log            # Log file for game events
├── main.py                 # Main entry point for running the game
├── remove_pycache.sh       # Script to remove Python cache files
└── src                     # Source code files
    ├── assets_loader.py    # Module for loading images and fonts
    ├── event_handler.py    # Handles user input and events
    ├── game.py             # Main game loop and drawing logic
    ├── game_logic.py       # Core 2048 game logic (movement, merging)
    ├── logger.py           # Logging system for debugging
    ├── player.py           # Placeholder for future player implementation
    └── utils.py            # Utility functions for the game
```

## How to Run

1. Ensure you have Python installed on your system.
2. Install the required dependencies:
   ```bash
   pip install pygame numpy
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Game Controls

- Use the arrow keys to move the tiles:
  - **Up Arrow**: Move tiles up.
  - **Down Arrow**: Move tiles down.
  - **Left Arrow**: Move tiles left.
  - **Right Arrow**: Move tiles right.
  
- Merge tiles of the same number to create larger numbers, aiming to reach 2048 (or higher!).

## Game Logic

- After each move, a new tile (2 or 4) is randomly added to the grid.
- The game ends when no more moves are possible (no empty tiles and no mergeable adjacent tiles).
  
## Features

- **Custom Grid Size**: The game grid is 8x8, providing a more challenging experience than the traditional 4x4 grid.
- **Tile Merging**: Same-number tiles merge to form a higher value.
- **Dynamic Colors**: Tiles are color-coded based on their values.
- **Logging**: Events such as key presses and errors are logged in `logs/game.log`.
- **Font & Image Loading**: Game assets such as fonts and images are dynamically loaded using the `assets_loader.py` module.

## Files Overview

- **`assets/`**:
  - `fonts/game_font.ttf`: The font used for rendering tile numbers.
  - `images/player.png`: Placeholder image for potential use (e.g., game sprites).
  
- **`config/settings.py`**:
  - Defines game constants such as screen size, FPS, and tile colors.

- **`logs/game.log`**:
  - Logs key events such as movement and game state changes, useful for debugging and tracking game progress.

- **`src/assets_loader.py`**:
  - Contains utility functions for loading images and fonts with error handling.

- **`src/event_handler.py`**:
  - Manages user inputs such as arrow key movements and quitting the game.

- **`src/game.py`**:
  - The core of the game, containing the main loop, game state updates, and tile rendering.

- **`src/game_logic.py`**:
  - Implements the core 2048 logic (tile merging, movement, and checking for valid moves).

- **`src/logger.py`**:
  - Handles logging of events, errors, and key game actions for debugging purposes.

- **`src/player.py`**:
  - Placeholder for potential future implementation of a player character or feature.

- **`src/utils.py`**:
  - Contains utility functions that assist in various game operations.

- **`remove_pycache.sh`**:
  - A simple shell script to remove all Python cache files (`__pycache__` folders).

## Future Improvements

- **AI Player**: Implement an AI player to automatically play the game.
- **Player Customization**: Add more customization options for player tiles or themes.
- **Multiplayer Mode**: Introduce a multiplayer mode where players can compete.
- **High Score Tracker**: Implement a system to track high scores.

## License

This project is open-source and available under the MIT License.

---

Enjoy playing the 2048 Game! If you encounter any issues or have suggestions, feel free to contribute or open an issue.