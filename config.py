import pygame
from pygame.locals import *

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

BLACK = (0, 0, 0)

PLAYER_SPEED = 16

FPS = 15

BG_IMAGE = "background/game.png"
WIN_IMAGE = "background/Winer_1.png"
LOSE_IMAGE = "background/Loser_1.png"
WIN_FON_IMAGE = "background/dungeon_menu.jpeg"
LOSE_FON_IMAGE = "background/pause_fon.png"

MENU_BG = "menu/bg/main_1.jpg"
MENU_BUTTON_START_PASSIVE = "menu/buttons/start_passive.png"
MENU_BUTTON_START_ACTIVE = "menu/buttons/start_active.png"
MENU_BUTTON_EXIT_PASSIVE = "menu/buttons/quit_passive.png"
MENU_BUTTON_EXIT_ACTIVE = "menu/buttons/quit_active.png"
MENU_BUTTON_SETTINGS_PASSIVE = "menu/buttons/settings_passive.png"
MENU_BUTTON_SETTINGS_ACTIVE = "menu/buttons/settings_active.png"
MENU_TITLE = "menu/DungeonMaster_480.png"
MENU_MUSIC = "menu/main_menu_sound.mp3"

PLAYER_SIZE = (36, 52)
ENEMY_SIZE = (27, 42)
BULLET_RIGHT_SIZE = (31, 5)
BULLET_LEFT_SIZE = (31, 5)

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
