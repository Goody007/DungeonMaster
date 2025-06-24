import pygame
from sprites.base import GameSprite
from sprites.bullet import Bullet

class Player(GameSprite):
    """Класс игрока"""
    def __init__(self, picture, width, height, x, y, x_speed, y_speed, animations):
        super().__init__(picture, width, height, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.animations = animations
        
        # Состояния игрока
        self.running_left = False
        self.running_right = False
        self.running_up = False
        self.running_down = False
        self.attacking_left = False
        self.attacking_right = False
        
        # Индексы анимаций
        self.run_animation_index = 0
        self.attack_animation_index = 0
    
    def update(self, barriers):
        """Обновление позиции игрока с учетом препятствий"""
        # Горизонтальное движение
        self.rect.x += self.x_speed
        
        # Проверка границ экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > pygame.display.get_surface().get_width():
            self.rect.right = pygame.display.get_surface().get_width()
        
        # Проверка столкновений с препятствиями по горизонтали
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:  # движение вправо
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        if self.x_speed < 0:  # движение влево
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        
        # Вертикальное движение
        self.rect.y += self.y_speed
        
        # Проверка границ экрана
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.rect.bottom = pygame.display.get_surface().get_height()
        
        # Проверка столкновений с препятствиями по вертикали
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # движение вниз
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        if self.y_speed < 0:  # движение вверх
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    
    def fire_right(self):
        """Выстрел вправо"""
        bullet = Bullet("objects/arrow_r.png", 31, 5, 
                       self.rect.x + self.rect.width, 
                       (self.rect.y + self.rect.height // 2) - 7, 
                       18)
        return bullet
    
    def fire_left(self):
        """Выстрел влево"""
        bullet = Bullet("objects/arrow_l.png", 31, 5, 
                       (self.rect.x + self.rect.width) - 50, 
                       (self.rect.y + self.rect.height // 2) - 7, 
                       -18)
        return bullet
    
    def update_animation(self):
        """Обновление анимации игрока"""
        # Обработка анимации бега
        if self.running_left:
            self.run_animation_index = (self.run_animation_index + 1) % 8
            anim_frame = self.animations['run_left'][self.run_animation_index]
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
        
        elif self.running_right:
            self.run_animation_index = (self.run_animation_index + 1) % 8
            anim_frame = self.animations['run_right'][self.run_animation_index]
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
        
        elif self.running_up:
            self.run_animation_index = (self.run_animation_index + 1) % 8
            anim_frame = self.animations['run_up'][self.run_animation_index]
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
        
        elif self.running_down:
            self.run_animation_index = (self.run_animation_index + 1) % 8
            anim_frame = self.animations['run_down'][self.run_animation_index]
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
        
        # Обработка анимации атаки
        if self.attacking_left:
            if self.attack_animation_index == 9:
                bullet = self.fire_left()
                self.attack_animation_index += 1
                return bullet
            elif self.attack_animation_index == 11:
                self.attack_animation_index = 0
                self.attacking_left = False
                return None
            else:
                self.attack_animation_index += 1
            
            anim_frame = self.animations['attack_left'][self.attack_animation_index]
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
            return None
        
        if self.attacking_right:
            if self.attack_animation_index == 9:
                bullet = self.fire_right()
                self.attack_animation_index += 1
                return bullet
            elif self.attack_animation_index == 11:
                self.attack_animation_index = 0
                self.attacking_right = False
                return None
            else:
                self.attack_animation_index += 1
            
            anim_frame = self.animations['attack_right'][self.attack_animation_index]
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
            return None
        
        return None
    
    def start_left_run(self):
        self.running_left = True
        self.x_speed = -3
    
    def start_right_run(self):
        self.running_right = True
        self.x_speed = 3
    
    def start_up_run(self):
        self.running_up = True
        self.y_speed = -3
    
    def start_down_run(self):
        self.running_down = True
        self.y_speed = 3
    
    def stop_left_run(self):
        self.running_left = False
        self.x_speed = 0
        self.image = self.animations['stay']['left']
    
    def stop_right_run(self):
        self.running_right = False
        self.x_speed = 0
        self.image = self.animations['stay']['right']
    
    def stop_up_run(self):
        self.running_up = False
        self.y_speed = 0
        self.image = self.animations['stay']['up']
    
    def stop_down_run(self):
        self.running_down = False
        self.y_speed = 0
        self.image = self.animations['stay']['down']
    
    def start_left_attack(self):
        self.attacking_left = True
        self.x_speed = 0
        self.y_speed = 0
        self.attack_animation_index = 0
    
    def start_right_attack(self):
        self.attacking_right = True
        self.x_speed = 0
        self.y_speed = 0
        self.attack_animation_index = 0