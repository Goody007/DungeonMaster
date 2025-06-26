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
        pygame.mixer.init()

        # Сохраняем ссылку на фоновую музыку меню
        self.menu_music = background_music

        # Создание звуков игры
        self.game_music = pygame.mixer.Sound("sounds/mists.mp3")  # Замените на свой файл
        self.game_music.set_volume(0.1)
        
        self.win_sound = pygame.mixer.Sound("sounds/win.mp3")  # Замените на свой файл
        self.win_sound.set_volume(0.1)
        
        self.lose_sound = pygame.mixer.Sound("sounds/lose.mp3")  # Замените на свой файл
        self.lose_sound.set_volume(0.1)
        
        # Другие звуки (опционально)
        self.key_pickup_sound = pygame.mixer.Sound("sounds/key-get.mp3")  # Звук подбора ключа
        self.key_pickup_sound.set_volume(0.5)
        
        self.enemy_death_sound = pygame.mixer.Sound("sounds/skeleton-fall.mp3")  # Звук смерти врага
        self.enemy_death_sound.set_volume(0.2)  # Уменьшаем громкость звука смерти скелета
        
        # Initialize sound effects with increased volume
        self.bow_draw_sound = pygame.mixer.Sound("sounds/bow_1.mp3")
        self.bow_draw_sound.set_volume(1.0)  # Увеличиваем громкость с 0.7 до 1.0

        self.bow_release_sound = pygame.mixer.Sound("sounds/bow_2.mp3")
        self.bow_release_sound.set_volume(1.0)  # Увеличиваем громкость с 0.7 до 1.0

        self.hero_steps_sound = pygame.mixer.Sound("sounds/steps.mp3")
        self.hero_steps_sound.set_volume(0.5)

        self.skeleton_steps_sound = pygame.mixer.Sound("sounds/skeleton_steps.mp3")
        self.skeleton_steps_sound.set_volume(0.2)

        self.door_unlock_sound = pygame.mixer.Sound("sounds/key_lock.mp3")
        self.door_unlock_sound.set_volume(0.5)
        
        self.hero_is_moving = False

        # Створення вікна
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        # Сохраняем ссылку на фоновую музыку
        self.background_music = background_music

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
        self.hero.game = self  # Добавляем ссылку на Game в Player

        # Створення ворога
        self.skeleton = Enemy('Finals/enemy/up/u_run_1.png', ENEMY_SIZE[0], ENEMY_SIZE[1], 
                              180, 185, 0, 0, self.enemy_anims)
        self.skeleton.game = self  # Добавляем ссылку на Game в Enemy
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

    def set_sound_volume(self, volume):
        """Установка громкости всех звуков игры"""
        self.game_music.set_volume(volume * 0.3)
        self.win_sound.set_volume(volume * 0.5)
        self.lose_sound.set_volume(volume * 0.5)
        self.key_pickup_sound.set_volume(volume * 0.4)
        self.enemy_death_sound.set_volume(volume * 0.2)  # Уменьшаем громкость звука смерти скелета
        self.bow_draw_sound.set_volume(volume * 0.9)  # Увеличиваем множитель громкости
        self.bow_release_sound.set_volume(volume * 0.9)  # Увеличиваем множитель громкости
        self.hero_steps_sound.set_volume(volume * 0.2)
        self.skeleton_steps_sound.set_volume(volume * 0.3)
        self.door_unlock_sound.set_volume(volume * 0.5)
        
    def stop_gameplay_sounds(self):
        """Остановить все игровые звуки, кроме музыки победы/проигрыша"""
        # Остановка всех звуков, связанных с геймплеем
        self.hero_steps_sound.stop()
        self.skeleton_steps_sound.stop()
        self.bow_draw_sound.stop()
        self.bow_release_sound.stop()
        self.key_pickup_sound.stop()
        self.enemy_death_sound.stop()
        self.door_unlock_sound.stop()
        # Сбрасываем статус движения героя
        self.hero_is_moving = False

    def handle_events(self):
        """Обробка подій гри"""
        for e in pygame.event.get():
            if e.type == QUIT:
                # Полностью завершаем программу при нажатии на крестик
                pygame.quit()
                sys.exit()

            # Если игра закончена, обрабатываем только события кнопки выхода
            if self.finish and self.quit_button:
                if e.type == MOUSEBUTTONDOWN:
                    self.quit_button.handle_event(e)
                elif e.type == USEREVENT and hasattr(e, 'button') and e.button == self.quit_button:
                    # Звук кнопки уже проигрывается автоматически в handle_event
                    # Возвращаемся в меню
                    self.running = False
                    return
                continue  # Если игра закончена, другие события не обрабатываем

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

    def update_player_position(self, keys):
        """Оновлення позиції гравця"""
        # Если игра закончена, не обновляем звуки шагов
        if self.finish:
            if self.hero_is_moving:
                self.hero_steps_sound.stop()
                self.hero_is_moving = False
            return
        
        is_moving_now = any([keys[CONTROLS['MOVE_UP']], keys[CONTROLS['MOVE_DOWN']], 
                             keys[CONTROLS['MOVE_LEFT']], keys[CONTROLS['MOVE_RIGHT']]])
        
        if is_moving_now and not self.hero_is_moving:
            self.hero_steps_sound.play(-1)  # Loop the sound while moving
        elif not is_moving_now and self.hero_is_moving:
            self.hero_steps_sound.stop()
            
        self.hero_is_moving = is_moving_now

    def update(self):
        """Оновлення ігрового стану"""
        if self.finish:
            return

        # Check player movement status and update footsteps sound
        self.update_player_position(self.keys_pressed)

        # Проверяем, начал ли игрок атаку и нужно ли проигрывать звук натяжения лука
        if self.hero.attacking_left or self.hero.attacking_right:
            if self.hero.attack_animation_index == 0:  # Звук натяжения в начале анимации
                self.bow_draw_sound.play()
            elif self.hero.attack_animation_index == 7:  # Звук выстрела на 7 кадре, примерно на пол секунды раньше
                self.bow_release_sound.play()

        # Оновлення гравця
        self.hero.update(self.level.barriers)
        bullet = self.hero.update_animation()
        if bullet:
            # В этот момент стрела только что создана - не нужно дублировать звук выстрела здесь
            self.level.bullets.add(bullet)

        # Оновлення куль
        self.level.bullets.update()

        # Оновлення ворогів
        for enemy in self.level.monsters:
            previous_pos = (enemy.rect.x, enemy.rect.y)
            enemy.update()
            enemy.update_animation()

            # Якщо ворог помер і ще не створена могила
            if enemy.dead and not self.level.graves:
                grave, key = enemy.create_grave_and_key()
                self.level.add_grave_and_key(grave, key, self)
                enemy.kill()

            # Якщо ворог рухається, відтворюємо звук кроків
            if (enemy.rect.x, enemy.rect.y) != previous_pos:
                if not pygame.mixer.Channel(1).get_busy():  # Use a specific channel for skeletons
                    self.skeleton_steps_sound.play()

        # Перевірка зіткнення куль
        enemy_hit, hit_enemy = self.level.check_bullet_collisions(self.tips)
        if enemy_hit:
            # Останавливаем другие звуки врага перед проигрыванием звука смерти
            self.skeleton_steps_sound.stop()
            self.enemy_death_sound.play()

        # Перевірка підбору ключа
        key_collected = self.level.check_key_collection(self.hero)
        if key_collected:
            self.key_pickup_sound.play()

        # Перевірка зіткнення з ворогами
        if pygame.sprite.spritecollideany(self.hero, self.level.monsters):
            # Останавливаем все игровые звуки
            self.stop_gameplay_sounds()
            self.game_music.stop()  # Останавливаем фоновую музыку
            self.lose_sound.play()  # Воспроизводим звук поражения
            
            # Создаем кнопку выхода с явно указанным звуком
            self.quit_button = ImageButton(
                (WINDOW_WIDTH / 2) - 100, 350, 200, 65,
                MENU_BUTTON_EXIT_PASSIVE, MENU_BUTTON_EXIT_ACTIVE, 
                "menu/click.mp3", 0.3  # Увеличиваем громкость, чтобы звук был более заметен
            )
            self.window.blit(self.lose_fon, (0, 0))
            self.window.blit(self.lose_image, (150, 50))
            self.finish = True
            return  # Прерываем метод, чтобы не выполнять остальные проверки

        # Перевірка досягнення фіналу (двері)
        if pygame.sprite.collide_rect(self.hero, self.level.final_door):
            if self.level.key_collected:
                # Останавливаем все игровые звуки
                self.stop_gameplay_sounds()
                self.door_unlock_sound.play()
                self.game_music.stop()  # Останавливаем фоновую музыку
                self.win_sound.play()  # Воспроизводим звук победы
                
                # Создаем кнопку выхода с явно указанным звуком
                self.quit_button = ImageButton(
                    (WINDOW_WIDTH / 2) - 100, 350, 200, 65,
                    MENU_BUTTON_EXIT_PASSIVE, MENU_BUTTON_EXIT_ACTIVE, 
                    "menu/click.mp3", 0.3  # Увеличиваем громкость, чтобы звук был более заметен
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
        self.game_music.play(loops=-1)  # -1 означает бесконечное повторение
        
        while self.running:
            # Обробка подій
            self.handle_events()

            # Оновлення ігрового стану
            self.update()

            # Відрисовка
            self.render()

            # Обмеження FPS
            self.clock.tick(FPS)

        # Останавливаем музыку при выходе
        self.game_music.stop()
        
        return