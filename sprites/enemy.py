import pygame
from sprites.base import GameSprite

class Enemy(GameSprite):
    def __init__(self, picture, width, height, x, y, speed_x, speed_y, animations):
        super().__init__(picture, width, height, x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.animations = animations
        self.game = None
        
        self.e_left = False
        self.e_right = False
        self.e_up = False
        self.e_down = False
        self.dying = False
        self.dead = False
        
        self.anim_index = 0
        self.death_index = 0
    
    def update(self):
        if self.dying or self.dead:
            return
            
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.y <= 185:
            self.speed_y = 0
            self.speed_x = 2
            self.e_up = False
            self.e_right = True
        
        if self.rect.x >= 500:
            self.speed_x = 0
            self.speed_y = 2
            self.e_right = False
            self.e_down = True
        
        if self.rect.y >= 250 and self.rect.x >= 500:
            self.speed_y = 0
            self.speed_x = -2
            self.e_down = False
            self.e_left = True
        
        if self.rect.x <= 180 and self.rect.y >= 250:
            self.speed_x = 0
            self.speed_y = -2
            self.e_left = False
            self.e_up = True
    
    def start_death(self):
        self.dying = True
        self.speed_x = 0
        self.speed_y = 0
        self.death_index = 0
    
    def update_animation(self):
        if self.dying:
            if self.death_index < len(self.animations['death']) - 1:
                self.death_index += 1
                self.image = pygame.transform.scale(self.animations['death'][self.death_index], 
                                                    self.animations['death'][self.death_index].get_size())
            else:
                self.dead = True
                self.dying = False
            return
        
        if self.e_left:
            self.anim_index = (self.anim_index + 1) % 9
            anim_frame = self.animations['run_left'][self.anim_index]
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
        
        elif self.e_right:
            self.anim_index = (self.anim_index + 1) % 9
            anim_frame = self.animations['run_right'][self.anim_index]
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
        
        elif self.e_up:
            self.anim_index = (self.anim_index + 1) % 9
            anim_frame = self.animations['run_up'][self.anim_index]
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
        
        elif self.e_down:
            self.anim_index = (self.anim_index + 1) % 9
            anim_frame = self.animations['run_down'][self.anim_index]
            self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
    
    def create_grave_and_key(self):
        from sprites.base import GameSprite
        
        grave = Enemy('Finals/enemy/death/death_5.png', 27, 28, 
                      self.rect.x, self.rect.y + 18, 0, 0, self.animations)
        grave.dead = True
        
        key = GameSprite("objects/key.png", 16, 16, self.rect.x + 3, self.rect.y + 24)
        
        return grave, key