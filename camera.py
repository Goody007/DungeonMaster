import pygame

class Camera:
    def __init__(self, width, height, zoom_width=200, zoom_height=200):
        # Размеры окна камеры
        self.width = width
        self.height = height
        
        # Размеры зума камеры (область видимости)
        self.zoom_width = zoom_width
        self.zoom_height = zoom_height
        
        # Смещение камеры
        self.offset_x = 0
        self.offset_y = 0
        
        # Создаем поверхность для зума
        self.zoom_surface = pygame.Surface((zoom_width, zoom_height))
        
        # Масштабирование (увеличение) зума на экран
        self.scale_factor = min(width / zoom_width, height / zoom_height)

    def update(self, target):
        # Центрирование камеры на цель без сглаживания для более точного следования
        self.offset_x = target.rect.centerx - self.zoom_width // 2
        self.offset_y = target.rect.centery - self.zoom_height // 2

    def apply(self, entity):
        # Перемещение объекта относительно камеры
        return pygame.Rect(
            entity.rect.x - self.offset_x,
            entity.rect.y - self.offset_y,
            entity.rect.width,
            entity.rect.height
        )
    
    def apply_rect(self, rect):
        # Применяет смещение камеры к прямоугольнику (для фона)
        return pygame.Rect(
            rect.x - self.offset_x,
            rect.y - self.offset_y,
            rect.width,
            rect.height
        )