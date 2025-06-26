import pygame
import sys
from pygame.locals import *

from config import *
from resources import ResourceManager, load_player_animations, load_enemy_animations, load_tips
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.base import GameSprite
from level import Level
from menu import *
from buttons import ImageButton

class Game:
    """Головний клас гри"""
    def __init__(self, background_music=None):
        pygame.init()

        # Сохраняем ссылку на фоновую музыку
        self.background_music = background_music

        # Створення вікна
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        # Завантаження фонових зображень
        self.bg = ResourceManager.load_image(BG_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.win_image = ResourceManager.load_image(WIN_IMAGE, (500, 300))
        self.lose_image = ResourceManager.load_image(LOSE_IMAGE, (500, 300))
        self.win_fon = ResourceManager.load_image(WIN_FON_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.lose_fon = ResourceManager.load_image(LOSE_FON_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Створення годинника для контролю FPS
        self.clock = pygame.time.Clock()

        # Завантаження анімацій
        self.player_anims = load_player_animations()
        self.enemy_anims = load_enemy_animations()
        self.tips = load_tips()

        # Створення рівня
        self.level = Level()
        self.level.create_barriers()
        self.level.create_level_objects(self.tips)

        # Створення гравця
        self.hero = Player("Finals/hero/stay/r_stay.png", PLAYER_SIZE[0], PLAYER_SIZE[1], 
                           10, 220, 0, 0, self.player_anims)

        # Створення ворога
        self.skeleton = Enemy('Finals/enemy/up/u_run_1.png', ENEMY_SIZE[0], ENEMY_SIZE[1], 
                              180, 185, 0, 0, self.enemy_anims)
        self.level.monsters.add(self.skeleton)

        # Ігровий стан
        self.running = True
        self.finish = False

        # Стан клавіш для плавного керування
        self.keys_pressed = {
            CONTROLS['MOVE_UP']: False,
            CONTROLS['MOVE_DOWN']: False,
            CONTROLS['MOVE_LEFT']: False,
            CONTROLS['MOVE_RIGHT']: False
        }

    def handle_events(self):
        """Обробка подій гри"""
        for e in pygame.event.get():
            if e.type == QUIT:
                # Полностью завершаем программу при нажатии на крестик
                pygame.quit()
                sys.exit()

            # Обробка натискань клавіш
            if e.type == KEYDOWN:
                # Рух
                if e.key == CONTROLS['MOVE_UP'] and not self.keys_pressed[CONTROLS['MOVE_UP']]:
                    self.keys_pressed[CONTROLS['MOVE_UP']] = True
                    self.hero.start_up_move()
                if e.key == CONTROLS['MOVE_DOWN'] and not self.keys_pressed[CONTROLS['MOVE_DOWN']]:
                    self.keys_pressed[CONTROLS['MOVE_DOWN']] = True
                    self.hero.start_down_move()
                if e.key == CONTROLS['MOVE_LEFT'] and not self.keys_pressed[CONTROLS['MOVE_LEFT']]:
                    self.keys_pressed[CONTROLS['MOVE_LEFT']] = True
                    self.hero.start_left_move()
                if e.key == CONTROLS['MOVE_RIGHT'] and not self.keys_pressed[CONTROLS['MOVE_RIGHT']]:
                    self.keys_pressed[CONTROLS['MOVE_RIGHT']] = True
                    self.hero.start_right_move()

                # Атака
                if e.key == CONTROLS['ATTACK_LEFT']:
                    self.hero.start_left_attack()
                if e.key == CONTROLS['ATTACK_RIGHT']:
                    self.hero.start_right_attack()

            # Обробка відпускання клавіш
            if e.type == KEYUP:
                if e.key == CONTROLS['MOVE_UP'] and self.keys_pressed[CONTROLS['MOVE_UP']]:
                    self.keys_pressed[CONTROLS['MOVE_UP']] = False
                    self.hero.stop_up_move()
                if e.key == CONTROLS['MOVE_DOWN'] and self.keys_pressed[CONTROLS['MOVE_DOWN']]:
                    self.keys_pressed[CONTROLS['MOVE_DOWN']] = False
                    self.hero.stop_down_move()
                if e.key == CONTROLS['MOVE_LEFT'] and self.keys_pressed[CONTROLS['MOVE_LEFT']]:
                    self.keys_pressed[CONTROLS['MOVE_LEFT']] = False
                    self.hero.stop_left_move()
                if e.key == CONTROLS['MOVE_RIGHT'] and self.keys_pressed[CONTROLS['MOVE_RIGHT']]:
                    self.keys_pressed[CONTROLS['MOVE_RIGHT']] = False
                    self.hero.stop_right_move()

            if self.finish and self.quit_button:
                if e.type == MOUSEBUTTONDOWN:
                    self.quit_button.handle_event(e)
                elif e.type == USEREVENT and hasattr(e, 'button') and e.button == self.quit_button:
                    pygame.quit()
                    sys.exit()

    def update(self):
        """Оновлення ігрового стану"""
        if self.finish:
            return

        # Оновлення гравця
        self.hero.update(self.level.barriers)
        bullet = self.hero.update_animation()
        if bullet:
            self.level.bullets.add(bullet)

        # Оновлення куль
        self.level.bullets.update()

        # Оновлення ворогів
        for enemy in self.level.monsters:
            enemy.update()
            enemy.update_animation()

            # Якщо ворог помер і ще не створена могила
            if enemy.dead and not self.level.graves:
                grave, key = enemy.create_grave_and_key()
                self.level.add_grave_and_key(grave, key)
                enemy.kill()

        # Перевірка зіткнення куль
        enemy_hit, hit_enemy = self.level.check_bullet_collisions(self.tips)

        # Перевірка підбору ключа
        self.level.check_key_collection(self.hero)

        # Перевірка зіткнення з ворогами
        if pygame.sprite.spritecollideany(self.hero, self.level.monsters):
            self.quit_button = ImageButton(
                (WINDOW_WIDTH / 2) - 100, 350, 200, 65,
                MENU_BUTTON_EXIT_PASSIVE, MENU_BUTTON_EXIT_ACTIVE, "menu/click.mp3", 0.2
            )
            self.window.blit(self.lose_fon, (0, 0))
            self.window.blit(self.lose_image, (150, 50))
            self.finish = True
            return  # Прерываем метод, чтобы не выполнять остальные проверки

        # Перевірка досягнення фіналу (двері)
        if pygame.sprite.collide_rect(self.hero, self.level.final_door):
            if self.level.key_collected:
                self.quit_button = ImageButton(
                    (WINDOW_WIDTH / 2) - 100, 350, 200, 65,
                    MENU_BUTTON_EXIT_PASSIVE, MENU_BUTTON_EXIT_ACTIVE, "menu/click.mp3", 0.2
                )
                self.window.blit(self.win_fon, (0, 0))
                self.window.blit(self.win_image, (150, 50))
                self.finish = True

    def render(self):
        """Відрисовка ігрового світу"""
        if not self.finish:
            # Відрисовка фону
            self.window.blit(self.bg, (0, 0))

            # Відрисовка об'єктів рівня
            self.level.final_door.reset(self.window)
            self.level.tip_1.reset(self.window)

            # Відрисовка могил і ключів, якщо є
            if self.level.graves:
                self.level.graves.draw(self.window)
                self.level.keys.update()
                self.level.keys.draw(self.window)

            # Відрисовка гравця
            self.hero.reset(self.window)

            # Відрисовка бар'єрів
            self.level.barriers.draw(self.window)

            # Відрисовка ворогів
            self.level.monsters.draw(self.window)

            # Відрисовка куль
            self.level.bullets.draw(self.window)

            # Відрисовка додаткових підказок
            self.level.update_tips(self.tips, self.window)

        if self.finish:
            if self.quit_button:
                mouse_pos = pygame.mouse.get_pos()
                self.quit_button.check_hover(mouse_pos)
                self.quit_button.draw(self.window)
            pygame.display.update()
            return

        # Оновлення екрану
        pygame.display.update()

    def run(self):
        """Основний ігровий цикл"""
        while self.running:
            # Обробка подій
            self.handle_events()

            # Оновлення ігрового стану
            self.update()

            # Відрисовка
            self.render()

            # Обмеження FPS
            self.clock.tick(FPS)

        # Удаляем вызов pygame.quit() отсюда, так как он закрывает весь pygame контекст
        # и делает невозможным возврат в меню
        return
