import pygame
from pygame.locals import *

# Файл з константами та конфігурацією

# Розміри вікна
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

# Кольори
BLACK = (0, 0, 0)

# Швидкості руху
PLAYER_SPEED = 12

# Ігрові налаштування
FPS = 15

# Шляхи до файлів
BG_IMAGE = "background/game.png"
WIN_IMAGE = "background/Winer.png"
LOSE_IMAGE = "background/Loser.png"
WIN_FON_IMAGE = "background/dungeon_menu.jpeg"
LOSE_FON_IMAGE = "background/pause_fon.png"

# Розміри об'єктів
PLAYER_SIZE = (36, 52)
ENEMY_SIZE = (27, 42)
BULLET_RIGHT_SIZE = (31, 5)
BULLET_LEFT_SIZE = (31, 5)

# Керування
CONTROLS = {
    'MOVE_UP': K_w,
    'MOVE_DOWN': K_s,
    'MOVE_LEFT': K_a,
    'MOVE_RIGHT': K_d,
    'ATTACK_LEFT': K_LEFT,
    'ATTACK_RIGHT': K_RIGHT
}

# CONTROLS = {
#     'MOVE_UP': K_e,
#     'MOVE_DOWN': K_d,
#     'MOVE_LEFT': K_s,
#     'MOVE_RIGHT': K_f,
#     'ATTACK_LEFT': K_SPACE,
#     'ATTACK_RIGHT': K_RETURN
# }
