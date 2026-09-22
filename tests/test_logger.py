"""Logger contract tests requiring no pygame or graphical display."""

import logging
from pathlib import Path
import tempfile
import unittest

from src.logger import log_error, log_event, setup_logger


class LoggerTest(unittest.TestCase):
    def test_logger_is_isolated_and_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = logging.getLogger()
            existing_root_handlers = tuple(root.handlers)
            output = Path(directory) / "subdir" / "game.log"
            logger = setup_logger(output)
            self.assertIs(setup_logger(output), logger)
            self.assertFalse(logger.propagate)
            self.assertEqual(tuple(root.handlers), existing_root_handlers)
            file_handlers = [handler for handler in logger.handlers if hasattr(handler, "baseFilename")]
            self.assertEqual(len(file_handlers), 1)
            log_event("test-event")
            log_error("test-error")
            file_handlers[0].flush()
            text = output.read_text(encoding="utf-8")
            self.assertIn("test-event", text)
            self.assertIn("test-error", text)
            # Do not retain an open handle to a temporary file on Windows.
            logger.removeHandler(file_handlers[0])
            file_handlers[0].close()


if __name__ == "__main__":
    unittest.main()
