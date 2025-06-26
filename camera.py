import pygame

class Camera:
    def __init__(self, width, height, zoom_width=450, zoom_height=400):
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
        
        # Добавляем ограничения для камеры
        self.world_width = 0   # Будет установлено позже
        self.world_height = 0  # Будет установлено позже

    def set_world_size(self, width, height):
        """Устанавливает размеры мира для ограничения камеры"""
        self.world_width = width
        self.world_height = height

    def update(self, target):
        # Центрирование камеры на цель
        self.offset_x = target.rect.centerx - self.zoom_width // 2
        self.offset_y = target.rect.centery - self.zoom_height // 2
        
        # Ограничиваем смещение камеры мировыми границами, если они установлены
        if self.world_width > 0:
            self.offset_x = max(0, min(self.offset_x, self.world_width - self.zoom_width))
        
        if self.world_height > 0:
            self.offset_y = max(0, min(self.offset_y, self.world_height - self.zoom_height))

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
        
    def get_offset(self):
        """Возвращает текущее смещение камеры"""
        return (self.offset_x, self.offset_y)