import pygame
import sys
from resources import ResourceManager

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Enemy Sprite Sheet Example")
clock = pygame.time.Clock()

# Путь к файлу спрайт-листа
sprite_sheet_path = "sprites/enemy_spritelist.png"

# Параметры спрайт-листа
sprite_width = 64
sprite_height = 64
rows = 5  # 5 строк в спрайт-листе (4 направления + смерть)
cols = 9  # 9 кадров для каждой анимации движения, 6 для смерти

# Загрузка спрайтов
all_sprites = ResourceManager.load_sprite_sheet(sprite_sheet_path, sprite_width, sprite_height, rows, cols, (64, 64))

# Разделение спрайтов на группы анимаций
animations = {
    'run_right': all_sprites[0:9],
    'run_left': all_sprites[9:18],
    'run_up': all_sprites[18:27],
    'run_down': all_sprites[27:36],
    'death': all_sprites[36:42]
}

# Выбор текущей анимации для просмотра
current_animation = 'run_right'
frame_index = 0

# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Переключение анимаций с помощью клавиш
            if event.key == pygame.K_RIGHT:
                current_animation = 'run_right'
                frame_index = 0
            elif event.key == pygame.K_LEFT:
                current_animation = 'run_left'
                frame_index = 0
            elif event.key == pygame.K_UP:
                current_animation = 'run_up'
                frame_index = 0
            elif event.key == pygame.K_DOWN:
                current_animation = 'run_down'
                frame_index = 0
            elif event.key == pygame.K_SPACE:
                current_animation = 'death'
                frame_index = 0
    
    # Очистка экрана
    screen.fill((0, 0, 0))
    
    # Отображение текущего спрайта
    current_sprites = animations[current_animation]
    if frame_index < len(current_sprites):
        screen.blit(current_sprites[frame_index], (400 - sprite_width//2, 300 - sprite_height//2))
    
    # Текст с инструкциями
    font = pygame.font.SysFont(None, 24)
    instructions = [
        "Нажмите стрелки для просмотра анимаций движения:",
        "← → ↑ ↓ - соответствующие направления",
        "Пробел - анимация смерти"
    ]
    
    y_offset = 450
    for line in instructions:
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (50, y_offset))
        y_offset += 30
    
    # Обновление индекса для анимации
    # Если дошли до конца анимации смерти, останавливаемся на последнем кадре
    if current_animation == 'death' and frame_index >= len(current_sprites) - 1:
        frame_index = len(current_sprites) - 1
    else:
        frame_index = (frame_index + 1) % len(current_sprites)
    
    # Обновление экрана
    pygame.display.flip()
    
    # Ограничение FPS
    clock.tick(8)  # Низкий FPS для наглядности анимации

# Завершение работы
pygame.quit()
sys.exit()
