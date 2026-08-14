<div align="center">

# 2048 <sub>· Python & Pygame</sub>

A classic **2048** game implemented in pure Python with **Pygame** — merge
equal tiles, chase the 2048 tile, and outlast the board on a harder **8×8 grid**.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.x-yellowgreen)](https://www.pygame.org/)
[![NumPy](https://img.shields.io/badge/NumPy-required-013243)](https://numpy.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-45%2F45%20passed-brightgreen)](https://github.com/1998x-stack/2048)

[Getting Started](#getting-started) · [Controls](#controls) ·
[Game Logic](#game-logic) · [Project Structure](#project-structure) ·
[Testing](#testing) · [Documentation](#documentation) ·
[Roadmap](#roadmap) · [License](#license)

</div>

A summary of what makes this variant stand out:

- 🏆 **Victory is actually detected** — reaching `2048`+ shows a **You Win!** overlay.
- 🎬 **Game-over screen** — no more abrupt window close; ENTER / ESC to exit.
- 🧪 **Headless test suite** — 45 checks across 6 suites; no display required.
- 🛡️ **Graceful asset loading** — missing fonts/images return a default instead of crashing.

---

## Features

- **8×8 grid** — a more challenging board than the classic 4×4.
- **Correct 2048 rules** — tiles merge once per move; a merged tile never
  merges again in the same move; only a *valid* move spawns a new tile.
- **Win / loss states** — reaching `2048`+ wins; a full board with no merges loses.
- **Page-high styling** — tiles are color-coded by value and the font auto-scales,
  so even `131072` stays readable.
- **Configurable** — grid size, tile size, colors, and FPS are centralized in
  `config/settings.py`; changing `GRID_SIZE` re-scales the whole game.
- **Logging** — every move and quit is recorded in `logs/game.log`.

---

## Getting Started

### Requirements

- **Python 3.9+**
- **Pygame** and **NumPy**

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/1998x-stack/2048.git
cd 2048

# 2. (Recommended) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate                # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install pygame numpy
```

> **Slow or unreachable PyPI?** Use the Tsinghua mirror:
>
> ```bash
> pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pygame numpy
> ```

### Run the game

```bash
python main.py
```

A window opens with two starting tiles already placed. Use the arrow keys to
merge tiles, aiming for `2048` (or beyond).

---

## Controls

| Action               | Key            |
| -------------------- | -------------- |
| Move up              | `↑` (Up Arrow)    |
| Move down            | `↓` (Down Arrow)  |
| Move left            | `←` (Left Arrow)  |
| Move right           | `→` (Right Arrow) |
| Quit the game        | `Esc`           |
| Exit the finished screen | `Enter` or `Esc` |

---

## Game Logic

- Tiles slide in the pressed direction; equal adjacent tiles **merge once** per move.
- A tile **spawned by a merge cannot merge again** in the same move.
- After every **valid** move a new tile is placed in a random empty cell;
  a move that changes nothing does **not** spawn a tile.
- **Victory** — any tile reaches `2048` or higher.
- **Game over** — the board is full and no adjacent tiles are mergeable.

*Spawning weights* use a Poisson-based model over powers of two up to the
current maximum tile, so larger numbers appear less often.

---

## Project Structure

```dir
.
├── assets/                     # Bundled game assets
│   ├── fonts/game_font.ttf     # Tile-number font
│   └── images/player.png       # Placeholder (future sprites)
├── config/settings.py          # Grid, window, colors, paths
├── logs/game.log               # Runtime log (auto-generated)
├── src/
│   ├── assets_loader.py        # Image/font loading (graceful on missing files)
│   ├── event_handler.py        # Quit detection, filtered logging
│   ├── game.py                 # Main loop, state evaluation, overlays
│   ├── game_logic.py           # Move/merge/spawn/is-over + rendering
│   ├── logger.py               # Logging setup
│   ├── player.py               # Placeholder player class (unused)
│   └── utils.py                # reset_game, check_victory
├── tests/                      # 6 headless test suites
│   ├── test_game_logic.py
│   ├── test_edge_cases.py
│   ├── test_render.py
│   ├── test_game_state.py
│   ├── test_event_assets.py
│   └── test_integration.py
├── main.py                     # Entry point
├── run_tests.sh                # Runs the full test suite
├── remove_pycache.sh           # Cleans __pycache__ folders
├── .gitignore
├── LICENSE
└── README.md
```

---

## Testing

The suite runs **headlessly** against a dummy SDL driver — no display or window
needed. Run everything at once:

```bash
./run_tests.sh
```

Or run individual suites:

```bash
python3 tests/test_game_logic.py    # core move/merge logic + regression
python3 tests/test_edge_cases.py    # edge cases (full boards, game over, Poisson)
python3 tests/test_render.py        # rendering + font-cache restart safety
python3 tests/test_game_state.py    # victory / game-over evaluation
python3 tests/test_event_assets.py  # events + asset-loader error handling
python3 tests/test_integration.py   # end-to-end game loop
```

---

## Configuration

All settings live in [`config/settings.py`](config/settings.py):

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `GRID_SIZE` | `8` | Board size (rows × columns) |
| `TILE_SIZE` | `80` | Tile width/height in px |
| `MARGIN` | `5` | Gap between tiles, px |
| `FPS` | `60` | Frame rate |
| `TILE_COLORS` | —  | Value→color palette |
| `FONT_PATH` | — | Path to the bundled font |

---

## Roadmap

- [ ] AI player for automated play
- [ ] Themes and tile customization
- [ ] Multiplayer mode
- [ ] High-score tracking (persistent)
- [ ] Undo last move

---

## Contributing

Contributions, issues, and feature requests are welcome. Fork the repo and open
a pull request; for larger changes, open an issue first to discuss the design.

---

## License

Released under the [MIT License](LICENSE) © 2024
[1998x-stack](https://github.com/1998x-stack).

---

<div align="center"><sub>Made with ❤️ — merge wisely.</sub></div>