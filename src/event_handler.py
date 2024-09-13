# src/event_handler.py
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import pygame
from src.logger import log_event

def handle_events(event):
    log_event(f"Event: {event}")
    if event.type == pygame.QUIT:
        log_event("Game quit by user.")
        return False  # 返回 False 表示用户请求退出
    return True  # 游戏继续运行