# src/player.py
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, IMAGE_PATH

class Player:
    def __init__(self, image_path=IMAGE_PATH):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, keys_pressed):
        move_speed = 5
        if keys_pressed[pygame.K_LEFT]:
            self.move(-move_speed, 0)
        if keys_pressed[pygame.K_RIGHT]:
            self.move(move_speed, 0)
        if keys_pressed[pygame.K_UP]:
            self.move(0, -move_speed)
        if keys_pressed[pygame.K_DOWN]:
            self.move(0, move_speed)