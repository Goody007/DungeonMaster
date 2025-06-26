import pygame
import sys
from buttons import ImageButton
from pygame.locals import *

from config import *
from resources import ResourceManager, load_player_animations, load_enemy_animations, load_tips
from sprites.player import Player
from sprites.enemy import Enemy
from level import Level
from sprite_manager import SpriteManager
from camera import Camera

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
        self.bg = ResourceManager.load_image(BG_IMAGE)  # Без масштабирования, чтобы сохранить детализацию
        
        # Устанавливаем размеры игрового мира на основе фона
        world_width = self.bg.get_width()
        world_height = self.bg.get_height()
        
        # Создаем камеру с меньшей областью видимости и устанавливаем размеры мира
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT, 450, 400)
        self.camera.set_world_size(world_width, world_height)
        
        # Остальные изображения
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

        # Создаем централизованный менеджер спрайтов
        self.sprite_manager = SpriteManager()
        
        # Створення рівня с использованием менеджера спрайтов
        self.level = Level(self.sprite_manager)
        self.level.create_barriers()
        self.level.create_level_objects(self.tips)

        # Створення гравця
        self.hero = Player("Finals/hero/stay/r_stay.png", PLAYER_SIZE[0], PLAYER_SIZE[1], 
                           10, 220, 0, 0, self.player_anims)
        self.sprite_manager.add(self.hero, 'players')

        # Створення ворога
        self.skeleton = Enemy('Finals/enemy/up/u_run_1.png', ENEMY_SIZE[0], ENEMY_SIZE[1], 
                              180, 185, 0, 0, self.enemy_anims)
        self.sprite_manager.add(self.skeleton, 'monsters')

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
        
        # Создаем поверхность для увеличенного изображения
        self.zoom_surface = pygame.Surface((self.camera.zoom_width, self.camera.zoom_height))
        self.scaled_surface = pygame.Surface((
            int(self.camera.zoom_width * self.camera.scale_factor),
            int(self.camera.zoom_height * self.camera.scale_factor)
        ))

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

    def update(self):
        """Оновлення ігрового стану"""
        if self.finish:
            return

        # Оновлення гравця
        self.hero.update(self.level.barriers)
        bullet = self.hero.update_animation()
        if bullet:
            self.sprite_manager.add(bullet, 'bullets')

        # Оновлення куль
        # Используем централизованное обновление для пуль
        self.sprite_manager.bullets.update()

        # Оновлення ворогів
        for enemy in self.sprite_manager.monsters:
            enemy.update()
            enemy.update_animation()

            # Якщо ворог помер і ще не створена могила
            if enemy.dead and not self.sprite_manager.graves:
                grave, key = enemy.create_grave_and_key()
                # Добавляем проверку на наличие могилы
                if grave:
                    self.level.add_grave_and_key(grave, key)
                else:
                    # Добавляем только ключ, без могилы
                    self.sprite_manager.add(key, 'keys')
                # Полностью удаляем enemy из всех групп
                self.sprite_manager.remove(enemy)  # без аргументов удалит из всех групп

        # Перевірка зіткнення куль
        enemy_hit, hit_enemy = self.level.check_bullet_collisions(self.tips)

        # Перевірка підбору ключа
        self.level.check_key_collection(self.hero)

        # Перевірка зіткнення з ворогами
        if pygame.sprite.spritecollideany(self.hero, self.sprite_manager.monsters):
            self.window.blit(self.lose_fon, (0, 0))
            self.window.blit(self.lose_image, (150, 50))
            self.finish = True

        # Перевірка досягнення фіналу (двері)
        if pygame.sprite.collide_rect(self.hero, self.level.final_door):
            if self.level.key_collected:
                self.window.blit(self.win_fon, (0, 0))
                self.window.blit(self.win_image, (150, 50))
                self.finish = True

    def render(self):
        """Відрисовка ігрового світу"""
        if not self.finish:
            # Очищаем поверхность зума
            self.zoom_surface.fill(BLACK)
            
            # Обновляем камеру, чтобы она следовала за героем
            self.camera.update(self.hero)
            
            # Отрисовка фона с учетом смещения камеры
            bg_rect = pygame.Rect(0, 0, self.bg.get_width(), self.bg.get_height())
            bg_draw_rect = self.camera.apply_rect(bg_rect)
            self.zoom_surface.blit(self.bg, bg_draw_rect)
            
            # Сортируем спрайты по Y-координате перед отрисовкой
            # Это обеспечит правильный порядок отображения по глубине
            sorted_sprites = sorted(self.sprite_manager.all_sprites, key=lambda sprite: sprite.rect.bottom)
            
            # Отрисовка всех спрайтов с учетом камеры и в правильном порядке
            for sprite in sorted_sprites:
                # Получаем смещенную позицию для спрайта
                camera_rect = self.camera.apply(sprite)
                # Отрисовываем спрайт на смещенной позиции
                self.zoom_surface.blit(sprite.image, camera_rect)

            # Відрисовка додаткових підказок с учетом камеры
            if hasattr(self.level, 'tip_1') and self.level.tip_1:
                tip1_rect = self.camera.apply(self.level.tip_1)
                self.zoom_surface.blit(self.level.tip_1.image, tip1_rect)
            
            if self.level.tip_2_visible and hasattr(self.level, 'tip_2') and self.level.tip_2:
                tip2_rect = self.camera.apply(self.level.tip_2)
                self.zoom_surface.blit(self.level.tip_2.image, tip2_rect)
            
            if self.level.tip_3_visible and hasattr(self.level, 'tip_3') and self.level.tip_3:
                tip3_rect = self.camera.apply(self.level.tip_3)
                self.zoom_surface.blit(self.level.tip_3.image, tip3_rect)

            # Масштабируем zoom_surface до размеров экрана
            pygame.transform.scale(self.zoom_surface, 
                                (int(WINDOW_WIDTH), int(WINDOW_HEIGHT)), 
                                self.window)
            
            # Опционально: нарисовать рамку для отладки коллизий
            if DEBUG_COLLISIONS:
                for barrier in self.sprite_manager.barriers:
                    barrier_rect = self.camera.apply(barrier)
                    pygame.draw.rect(self.window, (255, 0, 0), barrier_rect, 1)
                
                # Отображаем рамку игрока для отладки
                player_rect = self.camera.apply(self.hero)
                pygame.draw.rect(self.window, (0, 255, 0), player_rect, 1)
        else:
            # Отрисовка экрана завершения
            if pygame.sprite.collide_rect(self.hero, self.level.final_door) and self.level.key_collected:
                self.window.blit(self.win_fon, (0, 0))
                self.window.blit(self.win_image, (150, 50))
            else:
                self.window.blit(self.lose_fon, (0, 0))
                self.window.blit(self.lose_image, (150, 50))

        # Оновлення екрану
        pygame.display.update()

    def run(self):
        """Основний ігровий цикл"""
        while self.running:
            # Обробка подій
            self.handle_events()

            # Обновление игрового состояния
            self.update()

            # Відрисовка
            self.render()

            # Обмеження FPS
            self.clock.tick(FPS)
       
        return
