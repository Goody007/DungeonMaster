import pygame

class ImageButton:
    """Класс для кнопки с изображением"""
    def __init__(self, x, y, width, height, image_path, hover_image_path=None, sound_path=None, sound_volume=0.3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
            self.sound.set_volume(sound_volume)  # Установка громкости звука
        self.is_hovered = False

    def draw(self, surface):
        """Отрисовка кнопки на поверхности"""
        current_image = self.hover_image if self.is_hovered else self.image
        surface.blit(current_image, (self.x, self.y))

    def check_hover(self, mouse_pos):
        """Check if the mouse is hovering over the button"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        """Handle mouse events for the button"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def set_sound_volume(self, volume):
        """Устанавливает громкость звука нажатия кнопки"""
        if self.sound:
            self.sound.set_volume(volume)  # volume должен быть от 0.0 до 1.0
