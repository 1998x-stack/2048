# src/event_handler.py
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import pygame
from src.logger import log_event

# Keep only human-meaningful event types in the log; raw events such as
# MouseMotion/AudioDeviceAdded fire constantly and would flood logs/game.log.
_LOG_INTERESTING = (pygame.QUIT, pygame.KEYDOWN)

def is_quit_event(event):
    """Return True if *event* requests the game to quit (window close / ESC)."""
    if event.type == pygame.QUIT:
        return True
    return event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE

def handle_events(event):
    """Handle a single incoming pygame event.

    Returns False when the game should stop (window closed / ESC), True otherwise.
    """
    if not event or event.type not in _LOG_INTERESTING:
        return True  # ignore noisy/irrelevant events

    if is_quit_event(event):
        log_event("Game quit by user.")
        return False
    return True