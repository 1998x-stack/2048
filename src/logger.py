"""Game-specific logging that does not configure the process root logger."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

_LOGGER = logging.getLogger("game2048")
_LOGGER.addHandler(logging.NullHandler())
_LOGGER.propagate = False
_DEFAULT_LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "game.log"


def setup_logger(log_path=None):
    """Initialize the game log once, independently of the working directory."""
    if any(isinstance(handler, RotatingFileHandler) for handler in _LOGGER.handlers):
        return _LOGGER

    path = Path(log_path) if log_path is not None else _DEFAULT_LOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        path, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.INFO)
    _LOGGER.info("Logger initialized")
    return _LOGGER


def log_event(event_message: str):
    _LOGGER.info("%s", event_message)


def log_error(error_message: str):
    _LOGGER.error("%s", error_message)
