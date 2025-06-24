import pygame
from sprites.base import GameSprite

class Bullet(GameSprite):
    """Класс пули"""
    def __init__(self, picture, width, height, x, y, speed):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
    
    def update(self):
        """Обновление позиции пули"""
        self.rect.x += self.speed