# src/assets_loader.py
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import pygame
from src.logger import log_error
from config.settings import FONT_PATH

def load_image(image_path: str):
    try:
        return pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        log_error(f"Image loading failed: {image_path}, Error: {e}")
        return None

def load_font(size: int):
    try:
        return pygame.font.Font(FONT_PATH, size)
    except pygame.error as e:
        log_error(f"Font loading failed: {FONT_PATH}, Error: {e}")
        return None