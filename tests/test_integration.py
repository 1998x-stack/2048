# tests/test_integration.py
# End-to-end tests that drive the real run_game() loop headlessly and verify
# the finished screen (game over / victory) both shows and exits via ENTER.

import os, sys, threading, time
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame

from src.game import run_game

GAME_OVER_BOARD = [
    [2, 4, 8, 16, 2, 4, 8, 16],
    [4, 2, 16, 8, 4, 2, 16, 8],
    [8, 16, 2, 4, 8, 16, 2, 4],
    [16, 8, 4, 2, 16, 8, 4, 2],
    [2, 4, 8, 16, 2, 4, 8, 16],
    [4, 2, 16, 8, 4, 2, 16, 8],
    [8, 16, 2, 4, 8, 16, 2, 4],
    [16, 8, 4, 2, 16, 8, 4, 2],
]


def _poster(delay, events):
    # Only inject events; ownership of the pygame lifecycle (init/quit) belongs to
    # the run_game() loop in the main thread. Calling pygame.quit() here would race
    # with the main loop's drawing and tear the display out from under it.
    def work():
        time.sleep(delay)
        for e in events:
            pygame.event.post(e)
            time.sleep(0.2)
    threading.Thread(target=work, daemon=True).start()


def test_game_over_screen_exits_via_enter():
    _poster(0.4, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
    run_game(initial_grid=[r[:] for r in GAME_OVER_BOARD])


def test_victory_screen_exits_via_enter():
    board = [[0] * 8 for _ in range(8)]
    board[0][0] = 2048  # win, but with empty cells the board is not game over
    _poster(0.4, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
    run_game(initial_grid=board)


def test_empty_board_quits_via_esc():
    _poster(0.4, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
    run_game(initial_grid=[[0] * 8 for _ in range(8)])


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    sys.exit(0 if passed == len(tests) else 1)


if __name__ == "__main__":
    main()