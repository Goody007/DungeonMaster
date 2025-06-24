import pygame
from pygame.locals import *

from config import *
from resources import ResourceManager, load_player_animations, load_enemy_animations, load_tips
from sprites.player import Player
from sprites.enemy import Enemy
from level import Level

class Game:
    """Основной класс игры"""
    def __init__(self):
        pygame.init()
        
        # Создание окна
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game")
        
        # Загрузка фоновых изображений
        self.bg = ResourceManager.load_image(BG_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.win_image = ResourceManager.load_image(WIN_IMAGE, (500, 300))
        self.lose_image = ResourceManager.load_image(LOSE_IMAGE, (500, 300))
        self.win_fon = ResourceManager.load_image(WIN_FON_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.lose_fon = ResourceManager.load_image(LOSE_FON_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Создание часов для контроля FPS
        self.clock = pygame.time.Clock()
        
        # Загрузка анимаций
        self.player_anims = load_player_animations()
        self.enemy_anims = load_enemy_animations()
        self.tips = load_tips()
        
        # Создание уровня
        self.level = Level()
        self.level.create_barriers()
        self.level.create_level_objects(self.tips)
        
        # Создание игрока
        self.hero = Player("Finals/hero/stay/r_stay.png", PLAYER_SIZE[0], PLAYER_SIZE[1], 
                           10, 220, 0, 0, self.player_anims)
        
        # Создание врага
        self.skeleton = Enemy('Finals/enemy/up/u_run_1.png', ENEMY_SIZE[0], ENEMY_SIZE[1], 
                              180, 185, 0, 0, self.enemy_anims)
        self.level.monsters.add(self.skeleton)
        
        # Игровое состояние
        self.running = True
        self.finish = False
        
    def handle_events(self):
        """Обработка событий игры"""
        for e in pygame.event.get():
            if e.type == QUIT:
                self.running = False
            
            # Обработка нажатий клавиш
            if e.type == KEYDOWN:
                if e.key == K_w:
                    self.hero.start_up_run()
                if e.key == K_s:
                    self.hero.start_down_run()
                if e.key == K_a:
                    self.hero.start_left_run()
                if e.key == K_d:
                    self.hero.start_right_run()
                if e.key == K_LEFT:
                    self.hero.start_left_attack()
                if e.key == K_RIGHT:
                    self.hero.start_right_attack()
            
            # Обработка отпускания клавиш
            if e.type == KEYUP:
                if e.key == K_w:
                    self.hero.stop_up_run()
                if e.key == K_s:
                    self.hero.stop_down_run()
                if e.key == K_a:
                    self.hero.stop_left_run()
                if e.key == K_d:
                    self.hero.stop_right_run()
    
    def update(self):
        """Обновление игрового состояния"""
        if self.finish:
            return
        
        # Обновление игрока
        self.hero.update(self.level.barriers)
        bullet = self.hero.update_animation()
        if bullet:
            self.level.bullets.add(bullet)
        
        # Обновление пуль
        self.level.bullets.update()  # <-- Добавляем явное обновление пуль
        
        # Обновление врагов
        for enemy in self.level.monsters:
            enemy.update()
            enemy.update_animation()
            
            # Если враг умер и ещё не создана могила
            if enemy.dead and not self.level.graves:
                grave, key = enemy.create_grave_and_key()
                self.level.add_grave_and_key(grave, key)
                enemy.kill()
        
        # Проверка столкновения пуль
        enemy_hit, hit_enemy = self.level.check_bullet_collisions(self.tips)
        
        # Проверка подбора ключа
        self.level.check_key_collection(self.hero)
        
        # Проверка столкновения с врагами
        if pygame.sprite.spritecollideany(self.hero, self.level.monsters):
            self.window.blit(self.lose_fon, (0, 0))
            self.window.blit(self.lose_image, (150, 50))
            self.finish = True
        
        # Проверка достижения финала (двери)
        if pygame.sprite.collide_rect(self.hero, self.level.final_door):
            if self.level.key_collected:
                self.window.blit(self.win_fon, (0, 0))
                self.window.blit(self.win_image, (150, 50))
                self.finish = True
    
    def render(self):
        """Отрисовка игрового мира"""
        if not self.finish:
            # Отрисовка фона
            self.window.blit(self.bg, (0, 0))
            
            # Отрисовка объектов уровня
            self.level.final_door.reset(self.window)
            self.level.tip_1.reset(self.window)
            
            # Отрисовка могил и ключей, если есть
            if self.level.graves:
                self.level.graves.draw(self.window)
                self.level.keys.update()
                self.level.keys.draw(self.window)
            
            # Отрисовка игрока
            self.hero.reset(self.window)
            
            # Отрисовка барьеров
            self.level.barriers.draw(self.window)
            
            # Отрисовка врагов
            self.level.monsters.draw(self.window)
            
            # Отрисовка пуль
            self.level.bullets.draw(self.window)
            
            # Отрисовка дополнительных подсказок
            self.level.update_tips(self.tips, self.window)  # <-- Передаем self.window как параметр
        
        # Обновление экрана
        pygame.display.update()
    
    def run(self):
        """Основной игровой цикл"""
        while self.running:
            # Обработка событий
            self.handle_events()
            
            # Обновление игрового состояния
            self.update()
            
            # Отрисовка
            self.render()
            
            # Ограничение FPS
            self.clock.tick(FPS)
        
        pygame.quit()