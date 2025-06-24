import pygame
from resources import ResourceManager

class GameSprite(pygame.sprite.Sprite):
    """Базовый класс для всех игровых спрайтов"""
    def __init__(self, picture, width, height, x, y):
        super().__init__()
        self.image = ResourceManager.load_image(picture, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self, surface):
        """Отрисовка спрайта на поверхности"""
        surface.blit(self.image, (self.rect.x, self.rect.y))