import pygame
from sprites.base import GameSprite
from resources import ResourceManager

class Level:
    """Класс для создания и управления игровым уровнем"""
    def __init__(self):
        # Группы спрайтов
        self.barriers = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.graves = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        
        # Объекты уровня
        self.final_door = None
        self.tip_1 = None
        self.tip_2 = None
        self.tip_3 = None
        
        # Флаги
        self.key_collected = False
        self.tip_2_visible = False
        self.tip_3_visible = False
    
    def create_barriers(self):
        """Создание препятствий на уровне"""
        # Здесь создаются все барьеры
        barriers_data = [
            {"path": "background/barrier.png", "size": (8, 140), "pos": (427, 10)},
            {"path": "background/barrier.png", "size": (8, 140), "pos": (554, 10)},
            {"path": "background/barrier.png", "size": (80, 33), "pos": (522, 149)},
            {"path": "background/barrier.png", "size": (462, 33), "pos": (0, 149)},
            {"path": "background/barrier.png", "size": (150, 33), "pos": (410, 20)},
            {"path": "background/barrier.png", "size": (232, 33), "pos": (0, 300)},
            {"path": "background/barrier.png", "size": (8, 140), "pos": (225, 300)},
            {"path": "background/barrier.png", "size": (140, 8), "pos": (225, 420)},
            {"path": "background/barrier.png", "size": (8, 140), "pos": (324, 300)},
            {"path": "background/barrier.png", "size": (300, 8), "pos": (332, 300)},
            {"path": "background/barrier.png", "size": (8, 140), "pos": (590, 180)},
            {"path": "background/barrier.png", "size": (28, 33), "pos": (230, 387)},
            {"path": "background/barrier.png", "size": (37, 33), "pos": (285, 340)},
            {"path": "background/barrier.png", "size": (26, 42), "pos": (566, 187)}
        ]
        
        for barrier_data in barriers_data:
            barrier = GameSprite(
                barrier_data["path"],
                barrier_data["size"][0],
                barrier_data["size"][1],
                barrier_data["pos"][0],
                barrier_data["pos"][1]
            )
            self.barriers.add(barrier)
    
    def create_level_objects(self, tips):
        """Создание объектов уровня (двери, подсказки и т.д.)"""
        self.final_door = GameSprite("objects/furniture/door.png", 35, 42, 460, 45)
        self.tip_1 = GameSprite("objects/tip_1.png", 350, 30, 10, 350)
        self.tip_2 = GameSprite("objects/tip_2.png", 350, 30, 10, 400)
        self.tip_3 = GameSprite("objects/tip_3.png", 300, 35, 10, 450)
    
    def update_tips(self, tips, surface):
        """Обновление состояния подсказок"""
        if self.tip_2_visible:
            self.tip_2.reset(surface)
        
        if self.tip_3_visible:
            self.tip_3.reset(surface)
    
    def check_key_collection(self, hero):
        """Проверка подбора ключа"""
        if not self.key_collected and pygame.sprite.spritecollideany(hero, self.keys):
            self.keys.empty()
            self.key_collected = True
            self.tip_2.image = ResourceManager.load_image("objects/tip_2_done.png", (300, 30))
            self.tip_3_visible = True
            return True
        return False
    
    def check_bullet_collisions(self, tips):
        """Проверка столкновения пуль с врагами и барьерами"""
        for bullet in self.bullets:
            # Проверка столкновения с врагами
            enemy_hit = pygame.sprite.spritecollideany(bullet, self.monsters)
            if enemy_hit:
                bullet.kill()
                self.tip_1.image = ResourceManager.load_image("objects/tip_1_done.png", (300, 30))
                enemy_hit.start_death()
                return True, enemy_hit
            
            # Проверка столкновения с барьерами
            if pygame.sprite.spritecollideany(bullet, self.barriers):
                bullet.kill()
        
        return False, None
    
    def add_grave_and_key(self, grave, key):
        """Добавление могилы и ключа после смерти врага"""
        self.graves.add(grave)
        self.keys.add(key)
        self.tip_2_visible = True