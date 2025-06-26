import pygame
import math
from sprites.base import GameSprite
from sprites.bullet import Bullet

class Player(GameSprite):
    """Клас гравця з покращеною системою руху"""
    def __init__(self, picture, width, height, x, y, x_speed, y_speed, animations):
        super().__init__(picture, width, height, x, y)
        self.base_speed = 3  # базова швидкість
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.animations = animations
        
        # Стани руху (тепер незалежні)
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        
        # Стани атаки
        self.attacking_left = False
        self.attacking_right = False
        
        # Індекси анімацій
        self.run_animation_index = 0
        self.attack_animation_index = 0
        
        # Останній напрямок для правильної анімації спокою
        self.last_direction = 'right'
    
    def update_movement(self):
        """Оновлення швидкості на основі активних клавіш"""
        if self.attacking_left or self.attacking_right:
            self.x_speed = 0
            self.y_speed = 0
            return
        
        # Скидання швидкості
        self.x_speed = 0
        self.y_speed = 0
        
        # Горизонтальний рух
        if self.moving_left:
            self.x_speed -= self.base_speed
            self.last_direction = 'left'
        if self.moving_right:
            self.x_speed += self.base_speed
            self.last_direction = 'right'
        
        # Вертикальний рух
        if self.moving_up:
            self.y_speed -= self.base_speed
            if not (self.moving_left or self.moving_right):
                self.last_direction = 'up'
        if self.moving_down:
            self.y_speed += self.base_speed
            if not (self.moving_left or self.moving_right):
                self.last_direction = 'down'
        
        # Нормалізація швидкості для діагонального руху
        if self.x_speed != 0 and self.y_speed != 0:
            diagonal_speed = self.base_speed / math.sqrt(2)
            self.x_speed = diagonal_speed if self.x_speed > 0 else -diagonal_speed
            self.y_speed = diagonal_speed if self.y_speed > 0 else -diagonal_speed
    
    def update(self, barriers):
        """Оновлення позиції гравця з урахуванням перешкод"""
        self.update_movement()
        
        # Store original position for restoring if collision occurs
        original_x = self.rect.x
        original_y = self.rect.y
        
        # Горизонтальний рух
        self.rect.x += self.x_speed
        
        # Перевірка меж екрану
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > pygame.display.get_surface().get_width():
            self.rect.right = pygame.display.get_surface().get_width()
        
        # Перевірка зіткнень з перешкодами по горизонталі
        collisions = False
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:  # рух вправо
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
                collisions = True
        if self.x_speed < 0:  # рух вліво
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
                collisions = True
                
        # If there was a collision, stop horizontal movement
        if collisions:
            self.x_speed = 0
        
        # Вертикальний рух - проверяем отдельно после горизонтального
        original_y = self.rect.y  # Сохраняем позицию после горизонтальных коррекций
        self.rect.y += self.y_speed
        
        # Перевірка меж екрану
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.rect.bottom = pygame.display.get_surface().get_height()
        
        # Перевірка зіткнень з перешкодами по вертикалі
        collisions = False
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # рух вниз
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
                collisions = True
        if self.y_speed < 0:  # рух вгору
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
                collisions = True
                
        # If there was a collision, stop vertical movement
        if collisions:
            self.y_speed = 0
    
    def fire_right(self):
        """Постріл вправо"""
        bullet = Bullet("objects/arrow_r.png", 31, 5, 
                       self.rect.x + self.rect.width, 
                       (self.rect.y + self.rect.height // 2) + 17, 
                       18)
        return bullet
    
    def fire_left(self):
        """Постріл вліво"""
        bullet = Bullet("objects/arrow_l.png", 31, 5, 
                       (self.rect.x + self.rect.width) - 50, 
                       (self.rect.y + self.rect.height // 2) + 17, 
                       -18)
        return bullet
    
    def update_animation(self):
        """Оновлення анімації гравця"""
        # Анімація атаки має пріоритет
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
        
        # Анімація руху
        if self.x_speed != 0 or self.y_speed != 0:
            self.run_animation_index = (self.run_animation_index + 1) % 8
            
            # Вибір анімації на основі напрямку
            if abs(self.x_speed) > abs(self.y_speed):
                # Горизонтальний рух домінує
                if self.x_speed > 0:
                    anim_frame = self.animations['run_right'][self.run_animation_index]
                else:
                    anim_frame = self.animations['run_left'][self.run_animation_index]
            else:
                # Вертикальний рух домінує або діагональ
                if self.y_speed > 0:
                    anim_frame = self.animations['run_down'][self.run_animation_index]
                else:
                    anim_frame = self.animations['run_up'][self.run_animation_index]
            
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
        else:
            # Анімація спокою
            self.image = self.animations['stay'][self.last_direction]
        
        return None
    
    def start_left_move(self):
        self.moving_left = True
    
    def start_right_move(self):
        self.moving_right = True
    
    def start_up_move(self):
        self.moving_up = True
    
    def start_down_move(self):
        self.moving_down = True
    
    def stop_left_move(self):
        self.moving_left = False
    
    def stop_right_move(self):
        self.moving_right = False
    
    def stop_up_move(self):
        self.moving_up = False
    
    def stop_down_move(self):
        self.moving_down = False
    
    def start_left_attack(self):
        if not self.attacking_right:  # запобігання одночасним атакам
            self.attacking_left = True
            self.attack_animation_index = 0
    
    def start_right_attack(self):
        if not self.attacking_left:  # запобігання одночасним атакам
            self.attacking_right = True
            self.attack_animation_index = 0
