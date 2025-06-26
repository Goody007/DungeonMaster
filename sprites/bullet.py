import pygame
from sprites.base import GameSprite

class Bullet(GameSprite):
    def __init__(self, picture, width, height, x, y, speed):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
    
    def update(self):
        self.rect.x += self.speed