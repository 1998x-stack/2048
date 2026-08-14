# tests/test_edge_cases.py
# Edge-case tests for the 2048 game logic.

import sys
import os

PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, PARENT)

from src.game_logic import (
    merge_row,
    move_left,
    move_right,
    move_up,
    move_down,
    add_random_tile,
    is_game_over,
    get_max_value,
    poisson_probabilities,
)


def empty():
    return [[0] * 8 for _ in range(8)]


def board(*rows):
    return [list(r) for r in rows]


def test_full_board_no_moves_is_game_over():
    g = board(
        [2, 4, 8, 16, 2, 4, 8, 16],
        [4, 2, 16, 8, 4, 2, 16, 8],
        [8, 16, 2, 4, 8, 16, 2, 4],
        [16, 8, 4, 2, 16, 8, 4, 2],
        [2, 4, 8, 16, 2, 4, 8, 16],
        [4, 2, 16, 8, 4, 2, 16, 8],
        [8, 16, 2, 4, 8, 16, 2, 4],
        [16, 8, 4, 2, 16, 8, 4, 2],
    )
    assert is_game_over(g) is True


def test_full_board_with_adjacent_merge_not_over():
    # Full board, but each row has horizontally-mergeable equal pairs.
    row = [2, 2, 8, 8, 16, 16, 32, 32]
    g = board(*[row[:] for _ in range(8)])
    assert is_game_over(g) is False


def test_board_with_empty_tile_not_over():
    g = empty()
    g[0][0] = 2
    assert is_game_over(g) is False


def test_empty_board_not_over():
    assert is_game_over(empty()) is False


def test_add_random_tile_on_full_board_returns_false():
    g = board(
        [2, 4, 8, 16, 2, 4, 8, 16],
        [4, 2, 16, 8, 4, 2, 16, 8],
        [8, 16, 2, 4, 8, 16, 2, 4],
        [16, 8, 4, 2, 16, 8, 4, 2],
        [2, 4, 8, 16, 2, 4, 8, 16],
        [4, 2, 16, 8, 4, 2, 16, 8],
        [8, 16, 2, 4, 8, 16, 2, 4],
        [16, 8, 4, 2, 16, 8, 4, 2],
    )
    before = [r[:] for r in g]
    assert add_random_tile(g) is False
    assert g == before  # unchanged


def test_add_random_tile_places_valid_power_of_two():
    g = empty()
    assert add_random_tile(g) is True
    nonzero = [v for row in g for v in row if v != 0]
    assert len(nonzero) == 1
    assert nonzero[0] in (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096)


def test_get_max_value_on_empty_board_returns_at_least_2():
    assert get_max_value(empty()) == 2


def test_move_up_when_already_at_top_returns_false():
    g = empty()
    g[0][0] = 2
    g[0][1] = 4
    assert move_up(g) is False


def test_move_down_when_already_at_bottom_returns_false():
    g = empty()
    g[7][0] = 2
    g[7][1] = 4
    assert move_down(g) is False


def test_no_random_costly_moves_do_not_change_board():
    # This mirrors the bug we fixed: a dead move must not mutate or report a move.
    g = empty()
    g[0][0] = 2
    g[0][1] = 4
    before = [r[:] for r in g]
    assert move_left(g) is False
    assert g == before


def test_poisson_probabilities_normalize_to_one():
    for m in (2, 4, 16, 256, 2048):
        vals, probs = poisson_probabilities(m)
        assert len(vals) == len(probs)
        assert all(p >= 0 for p in probs)
        assert abs(sum(probs) - 1.0) < 1e-9
        # values must be powers of two, max <= m
        import math
        for v in vals:
            assert v == 2 ** int(math.log2(v))
            assert v <= m


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
    sys.exit(0 if passed == len(tests) else 1)


if __name__ == "__main__":
    main()