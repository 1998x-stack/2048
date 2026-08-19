# src/logger.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import logging

def setup_logger():
    logging.basicConfig(
        filename='logs/game.log',
        filemode='a',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    logging.info("Logger initialized")

def log_event(event_message: str):
    logging.info(event_message)

def log_error(error_message: str):
    logging.error(error_message)
