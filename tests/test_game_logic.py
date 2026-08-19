# tests/test_game_logic.py
# Tests for the core 2048 game logic.
#
# These tests import src.game_logic, which imports pygame. To run without a
# display / without pygame installed, a minimal pygame stub is injected first.

import sys
import os
import types

PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PARENT)

# --- Minimal pygame stub so src/game_logic.py can be imported headlessly ---
if "pygame" not in sys.modules:
    mock = types.ModuleType("pygame")
    mock.Rect = lambda *a, **k: None
    mock.font = types.SimpleNamespace(Font=lambda *a, **k: None)
    mock.draw = types.SimpleNamespace(rect=lambda *a, **k: None)
    sys.modules["pygame"] = mock

from src.game_logic import merge_row, move_left, move_right, move_up, move_down, add_random_tile


def test_merge_basic_pair():
    row = [2, 2, 0, 0]
    assert merge_row(row) is True   # moved
    assert row == [4, 0, 0, 0]


def test_merge_four_of_a_kind():
    row = [2, 2, 2, 2]
    assert merge_row(row) is True
    assert row == [4, 4, 0, 0]


def test_merge_three_of_a_kind_merges_once():
    row = [2, 2, 2, 0]
    assert merge_row(row) is True
    assert row == [4, 2, 0, 0]


def test_merge_existing_merge_pair():
    row = [4, 2, 2, 0]
    assert merge_row(row) is True
    assert row == [4, 4, 0, 0]


def test_move_returns_false_when_nothing_changes():
    # Row is already packed to the left with no possible merge.
    row = [2, 4, 0, 0]
    assert merge_row(row) is False   # BUG: returned True before the fix
    assert row == [2, 4, 0, 0]


def test_move_left_slides_and_merges():
    g = [
        [2, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert move_left(g) is True
    assert g[0][0] == 4


def test_move_left_reports_false_when_grid_unchanged():
    g = [
        [2, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert move_left(g) is False   # nothing can move left
    assert g[0] == [2, 4, 0, 0, 0, 0, 0, 0]


def test_move_right_merges_to_right():
    g = [
        [2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert move_right(g) is True
    assert g[0][7] == 4


def test_move_up_and_down():
    g_up = [[2, 0, 0, 0, 0, 0, 0, 0] for _ in range(8)]
    g_up[7][0] = 2
    assert move_up(g_up) is True
    assert g_up[0][0] == 4

    g_down = [[2, 0, 0, 0, 0, 0, 0, 0] for _ in range(8)]
    g_down[0][0] = 2
    assert move_down(g_down) is True
    assert g_down[7][0] == 4


def _seed_spawn_once(grid):
    import random
    add_random_tile(grid)
    return tuple(tuple(row) for row in grid)


def test_add_random_tile_deterministic_under_seed():
    import random
    random.seed(7)
    a = _seed_spawn_once([[0] * 8 for _ in range(8)])
    random.seed(7)
    b = _seed_spawn_once([[0] * 8 for _ in range(8)])
    assert a == b


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
        except Exception as e:
            print(f"ERROR {t.__name__}: {e!r}")
    print(f"\n{passed}/{len(tests)} passed")
    if passed != len(tests):
        sys.exit(1)


if __name__ == "__main__":
    main()