# 2048 — Python + Pygame

[![Python game checks](https://github.com/1998x-stack/2048/actions/workflows/ci.yml/badge.svg)](https://github.com/1998x-stack/2048/actions/workflows/ci.yml)

An 8×8 2048 variant written in Python. Use the arrow keys to slide equal tiles together, reach a tile of **2048 or higher**, or keep playing until no legal moves remain. A finished game displays a win/loss overlay; press Enter or Esc to exit.

## Quick start

Requires Python 3.9+ and Pygame 2.x. The game does **not** require NumPy.

```bash
git clone https://github.com/1998x-stack/2048.git
cd 2048
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python -m pip install 'pygame>=2.5,<3'
python main.py
```

Use the arrow keys to move. A move that leaves the board unchanged does not spawn a tile. Close the window or press Esc to quit.

## Rules and architecture

- `src/board.py`: pure Python movement, merging, spawning, and terminal-state checks. It has no Pygame dependency and can be imported by bots or test runners.
- `src/game_logic.py`: rendering and backward-compatible exports of the board functions. Tile fonts are cached for one Pygame session and invalidated before a new run.
- `src/game.py`: keyboard events, window lifecycle, and win/loss overlays. The state is checked after every valid move, including when multiple key events are queued in one frame.
- `config/settings.py`: the default 8×8 board, tile and window sizes, colors, and asset locations.
- `src/logger.py`: an independent, rotating game logger. Runtime logs are created in `logs/game.log` relative to the repository, regardless of the current working directory, and are not tracked in Git.

**Variant-specific spawning:** after a valid move, one empty cell is chosen uniformly. The value is chosen from powers of two up to the current maximum tile, with descending normalized weights `weight(2**i) = 2**(1-i)` for `i >= 1`. On an empty board the only value is 2. This is **not** the classic 2048 fixed 2/4 spawn distribution and is **not** a Poisson distribution.

Tiles merge at most once per move. On a full board with no adjacent equal tiles, the game is over. Reaching 2048 or more wins; this variant gives victory precedence over game-over when evaluating a finished board. No score counter or persistent high-score system is currently implemented.

## Testing

Run all checks from the repository root after installing Pygame:

```bash
bash run_tests.sh
```

The runner executes the pure board and logger tests plus the six existing game, render, event, and integration suites. It preserves each test's output and exits immediately on failure. For logic-only tests without installing Pygame:

```bash
python3 -m unittest discover -s tests -p 'test_board_pure.py' -v
python3 -m unittest discover -s tests -p 'test_logger.py' -v
```

`run_tests.sh` defaults `SDL_VIDEODRIVER` and `SDL_AUDIODRIVER` to `dummy`; see [Pygame's headless driver guide](https://www.pygame.org/wiki/DummyVideoDriver). `.github/workflows/ci.yml` runs a syntax check and the full runner on pushes to `main` and on pull requests.

## Project layout

```text
assets/                   Bundled font and image
config/settings.py        Display constants and asset paths
docs/                     Design notes, review, and plans
src/board.py              Pure board rules and spawn probabilities
src/game_logic.py         Pygame tile rendering and compatibility exports
src/game.py               Application loop and overlays
src/logger.py             Isolated game logging
src/assets_loader.py      Image/font fallback handling
src/event_handler.py      Quit-event detection
src/utils.py              Victory and reset helpers
tests/                    Pure, rendering, event, and integration checks
main.py                   Run the game
run_tests.sh              Run all tests with failure reporting
```

## Next steps

Potential future features include score tracking, an undo history, an AI player based on the pure board module, and accessibility improvements. See `docs/REVIEW-2026-09-22.md` for the review findings, validation scope, and follow-up plan.

## License

MIT — see [LICENSE](LICENSE).
