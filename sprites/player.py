import pygame
import math
from sprites.base import GameSprite
from sprites.bullet import Bullet

class Player(GameSprite):
    def __init__(self, picture, width, height, x, y, x_speed, y_speed, animations):
        super().__init__(picture, width, height, x, y)
        self.base_speed = 3
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.animations = animations
        self.game = None
        
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        
        self.attacking_left = False
        self.attacking_right = False
        
        self.run_animation_index = 0
        self.attack_animation_index = 0
        
        self.last_direction = 'right'
    
    def update_movement(self):
        if self.attacking_left or self.attacking_right:
            self.x_speed = 0
            self.y_speed = 0
            return
        
        self.x_speed = 0
        self.y_speed = 0
        
        if self.moving_left:
            self.x_speed -= self.base_speed
            self.last_direction = 'left'
        if self.moving_right:
            self.x_speed += self.base_speed
            self.last_direction = 'right'
        
        if self.moving_up:
            self.y_speed -= self.base_speed
            if not (self.moving_left or self.moving_right):
                self.last_direction = 'up'
        if self.moving_down:
            self.y_speed += self.base_speed
            if not (self.moving_left or self.moving_right):
                self.last_direction = 'down'
        
        if self.x_speed != 0 and self.y_speed != 0:
            diagonal_speed = self.base_speed / math.sqrt(2)
            self.x_speed = diagonal_speed if self.x_speed > 0 else -diagonal_speed
            self.y_speed = diagonal_speed if self.y_speed > 0 else -diagonal_speed
    
    def update(self, barriers):
        self.update_movement()
        
        self.rect.x += self.x_speed
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > pygame.display.get_surface().get_width():
            self.rect.right = pygame.display.get_surface().get_width()
        
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        if self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        
        self.rect.y += self.y_speed
        
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.rect.bottom = pygame.display.get_surface().get_height()
        
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        if self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    
    def fire_right(self):
        bullet = Bullet("objects/arrow_r.png", 31, 5, 
                       self.rect.x + self.rect.width, 
                       (self.rect.y + self.rect.height // 2) - 7, 
                       18)
        return bullet
    
    def fire_left(self):
        bullet = Bullet("objects/arrow_l.png", 31, 5, 
                       (self.rect.x + self.rect.width) - 50, 
                       (self.rect.y + self.rect.height // 2) - 7, 
                       -18)
        return bullet
    
    def update_animation(self):
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
        
        if self.x_speed != 0 or self.y_speed != 0:
            self.run_animation_index = (self.run_animation_index + 1) % 8
            
            if abs(self.x_speed) > abs(self.y_speed):
                if self.x_speed > 0:
                    anim_frame = self.animations['run_right'][self.run_animation_index]
                else:
                    anim_frame = self.animations['run_left'][self.run_animation_index]
            else:
                if self.y_speed > 0:
                    anim_frame = self.animations['run_down'][self.run_animation_index]
                else:
                    anim_frame = self.animations['run_up'][self.run_animation_index]
            
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
        else:
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
        if not self.attacking_right:
            self.attacking_left = True
            self.attack_animation_index = 0
    
    def start_right_attack(self):
        if not self.attacking_left:
            self.attacking_right = True
            self.attack_animation_index = 0
