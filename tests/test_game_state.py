# tests/test_game_state.py
# Unit tests for the terminal-state evaluation (victory / game over) and
# utility helpers that the game loop now uses.

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from src.utils import check_victory, reset_game
from src.game import evaluate_state


def empty():
    return [[0] * 8 for _ in range(8)]


def test_check_victory_false_on_empty():
    assert check_victory(empty()) is False


def test_check_victory_true_at_2048():
    g = empty()
    g[3][3] = 2048
    assert check_victory(g) is True


def test_check_victory_true_beyond_2048():
    g = empty()
    g[0][0] = 4096
    assert check_victory(g) is True  # tile can spawn/merge past 2048


def test_check_victory_false_below_2048():
    g = empty()
    g[0][0] = 1024
    assert check_victory(g) is False


def test_reset_game_zeroes_full_board():
    g = [[2**i for i in range(8)] for _ in range(8)]
    reset_game(g)
    assert g == [[0] * 8 for _ in range(8)]


def test_reset_game_idempotent():
    g = [[0] * 8 for _ in range(8)]
    reset_game(g)
    assert g == [[0] * 8 for _ in range(8)]


def test_evaluate_state_ongoing():
    finished, message = evaluate_state(empty())
    assert finished is False and message is None


def test_evaluate_state_victory():
    g = empty()
    g[0][0] = 2048
    finished, message = evaluate_state(g)
    assert finished is True and message == "You Win!"


def test_evaluate_state_game_over():
    g = [
        [2, 4, 8, 16, 2, 4, 8, 16],
        [4, 2, 16, 8, 4, 2, 16, 8],
        [8, 16, 2, 4, 8, 16, 2, 4],
        [16, 8, 4, 2, 16, 8, 4, 2],
        [2, 4, 8, 16, 2, 4, 8, 16],
        [4, 2, 16, 8, 4, 2, 16, 8],
        [8, 16, 2, 4, 8, 16, 2, 4],
        [16, 8, 4, 2, 16, 8, 4, 2],
    ]
    finished, message = evaluate_state(g)
    assert finished is True and message == "Game Over"


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