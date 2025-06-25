import pygame
import sys
from resources import ResourceManager

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sprite Sheet Example")
clock = pygame.time.Clock()

# Путь к файлу спрайт-листа
sprite_sheet_path = "sprites/character_spritesheet.png"  # Замените на свой путь

# Параметры спрайт-листа
sprite_width = 64
sprite_height = 64
rows = 4  # Количество строк в спрайт-листе
cols = 6  # Количество столбцов в спрайт-листе

# Загрузка спрайтов
sprites = ResourceManager.load_sprite_sheet(sprite_sheet_path, sprite_width, sprite_height, rows, cols)

# Индекс текущего спрайта для анимации
current_sprite = 0

# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Очистка экрана
    screen.fill((0, 0, 0))
    
    # Отображение текущего спрайта
    if sprites and current_sprite < len(sprites):
        screen.blit(sprites[current_sprite], (400 - sprite_width//2, 300 - sprite_height//2))
    
    # Обновление индекса для анимации
    current_sprite = (current_sprite + 1) % len(sprites) if sprites else 0
    
    # Обновление экрана
    pygame.display.flip()
    
    # Ограничение FPS
    clock.tick(10)  # Более низкий FPS для наглядности анимации

# Завершение работы
pygame.quit()
sys.exit()
