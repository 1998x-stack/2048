# tests/test_event_assets.py
# Tests for the event handler (quit detection) and the asset loader's error
# handling (missing paths must return None and log, not crash).

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from src.event_handler import is_quit_event, handle_events
from src.assets_loader import load_image, load_font
from config.settings import FONT_PATH, IMAGE_PATH


def test_quit_event_window_close():
    ev = pygame.event.Event(pygame.QUIT)
    assert is_quit_event(ev) is True


def test_quit_event_escape_key():
    ev = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    assert is_quit_event(ev) is True


def test_arrow_key_is_not_quit():
    for k in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
        ev = pygame.event.Event(pygame.KEYDOWN, key=k)
        assert is_quit_event(ev) is False


def test_noisy_event_is_not_quit():
    ev = pygame.event.Event(pygame.MOUSEMOTION, pos=(1, 1), rel=(0, 0), buttons=(0, 0, 0))
    assert is_quit_event(ev) is False
    assert handle_events(ev) is True  # ignored, game continues


def test_handle_events_quit_returns_false():
    assert handle_events(pygame.event.Event(pygame.QUIT)) is False


def test_asset_loader_loads_real_font():
    pygame.init()
    f = load_font(24)
    pygame.quit()
    assert f is not None


def test_asset_loader_missing_font_returns_none():
    pygame.init()
    f = load_font.__wrapped__ if hasattr(load_font, "__wrapped__") else None
    # Try a path that does not exist via load_font default is FONT_PATH; simulate a bad path:
    import src.assets_loader as al
    try:
        result = al.load_font.__code__  # ensure callable
        # call internal load with a bad path by monkeypatching module constant
        orig = al.FONT_PATH
        al.FONT_PATH = "/nonexistent/nope.ttf"
        # load_font uses module-level FONT_PATH
        got = al.load_font(24)
        al.FONT_PATH = orig
        assert got is None
    finally:
        al.FONT_PATH = orig if 'orig' in locals() else ""
    pygame.quit()


def test_asset_loader_missing_image_returns_none():
    assert load_image("/nonexistent/missing.png") is None


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