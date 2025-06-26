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
    def __init__(self, background_music=None):
        pygame.init()
        pygame.mixer.init()

        self.menu_music = background_music

        self.game_music = pygame.mixer.Sound("sounds/mists.mp3")
        self.game_music.set_volume(0.1)
        
        self.win_sound = pygame.mixer.Sound("sounds/win.mp3")
        self.win_sound.set_volume(0.1)
        
        self.lose_sound = pygame.mixer.Sound("sounds/lose.mp3")
        self.lose_sound.set_volume(0.1)
        
        self.key_pickup_sound = pygame.mixer.Sound("sounds/key-get.mp3")
        self.key_pickup_sound.set_volume(0.5)
        
        self.enemy_death_sound = pygame.mixer.Sound("sounds/skeleton-fall.mp3")
        self.enemy_death_sound.set_volume(0.2)
        
        self.bow_draw_sound = pygame.mixer.Sound("sounds/bow_1.mp3")
        self.bow_draw_sound.set_volume(1.0)

        self.bow_release_sound = pygame.mixer.Sound("sounds/bow_2.mp3")
        self.bow_release_sound.set_volume(1.0)

        self.hero_steps_sound = pygame.mixer.Sound("sounds/steps.mp3")
        self.hero_steps_sound.set_volume(0.5)

        self.skeleton_steps_sound = pygame.mixer.Sound("sounds/skeleton_steps.mp3")
        self.skeleton_steps_sound.set_volume(0.2)

        self.door_unlock_sound = pygame.mixer.Sound("sounds/key_lock.mp3")
        self.door_unlock_sound.set_volume(0.5)
        
        self.hero_is_moving = False

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        self.background_music = background_music

        self.bg = ResourceManager.load_image(BG_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.win_image = ResourceManager.load_image(WIN_IMAGE, (500, 300))
        self.lose_image = ResourceManager.load_image(LOSE_IMAGE, (500, 300))
        self.win_fon = ResourceManager.load_image(WIN_FON_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.lose_fon = ResourceManager.load_image(LOSE_FON_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()

        self.player_anims = load_player_animations()
        self.enemy_anims = load_enemy_animations()
        self.tips = load_tips()

        self.level = Level()
        self.level.create_barriers()
        self.level.create_level_objects(self.tips)

        self.hero = Player("Finals/hero/stay/r_stay.png", PLAYER_SIZE[0], PLAYER_SIZE[1], 
                           10, 220, 0, 0, self.player_anims)
        self.hero.game = self

        self.skeleton = Enemy('Finals/enemy/up/u_run_1.png', ENEMY_SIZE[0], ENEMY_SIZE[1], 
                              180, 185, 0, 0, self.enemy_anims)
        self.skeleton.game = self
        self.level.monsters.add(self.skeleton)

        self.running = True
        self.finish = False

        self.keys_pressed = {
            CONTROLS['MOVE_UP']: False,
            CONTROLS['MOVE_DOWN']: False,
            CONTROLS['MOVE_LEFT']: False,
            CONTROLS['MOVE_RIGHT']: False
        }

    def set_sound_volume(self, volume):
        self.game_music.set_volume(volume * 0.3)
        self.win_sound.set_volume(volume * 0.5)
        self.lose_sound.set_volume(volume * 0.5)
        self.key_pickup_sound.set_volume(volume * 0.4)
        self.enemy_death_sound.set_volume(volume * 0.2)
        self.bow_draw_sound.set_volume(volume * 0.9)
        self.bow_release_sound.set_volume(volume * 0.9)
        self.hero_steps_sound.set_volume(volume * 0.2)
        self.skeleton_steps_sound.set_volume(volume * 0.3)
        self.door_unlock_sound.set_volume(volume * 0.5)
        
    def stop_gameplay_sounds(self):
        self.hero_steps_sound.stop()
        self.skeleton_steps_sound.stop()
        self.bow_draw_sound.stop()
        self.bow_release_sound.stop()
        self.key_pickup_sound.stop()
        self.enemy_death_sound.stop()
        self.door_unlock_sound.stop()
        self.hero_is_moving = False

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()

            if self.finish and self.quit_button:
                if e.type == MOUSEBUTTONDOWN:
                    self.quit_button.handle_event(e)
                elif e.type == USEREVENT and hasattr(e, 'button') and e.button == self.quit_button:
                    self.running = False
                    return
                continue

            if e.type == KEYDOWN:
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

                if e.key == CONTROLS['ATTACK_LEFT']:
                    self.hero.start_left_attack()
                if e.key == CONTROLS['ATTACK_RIGHT']:
                    self.hero.start_right_attack()

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
        if self.finish:
            if self.hero_is_moving:
                self.hero_steps_sound.stop()
                self.hero_is_moving = False
            return
        
        is_moving_now = any([keys[CONTROLS['MOVE_UP']], keys[CONTROLS['MOVE_DOWN']], 
                             keys[CONTROLS['MOVE_LEFT']], keys[CONTROLS['MOVE_RIGHT']]])
        
        if is_moving_now and not self.hero_is_moving:
            self.hero_steps_sound.play(-1)
        elif not is_moving_now and self.hero_is_moving:
            self.hero_steps_sound.stop()
            
        self.hero_is_moving = is_moving_now

    def update(self):
        if self.finish:
            return

        self.update_player_position(self.keys_pressed)

        if self.hero.attacking_left or self.hero.attacking_right:
            if self.hero.attack_animation_index == 0:
                self.bow_draw_sound.play()
            elif self.hero.attack_animation_index == 7:
                self.bow_release_sound.play()

        self.hero.update(self.level.barriers)
        bullet = self.hero.update_animation()
        if bullet:
            self.level.bullets.add(bullet)

        self.level.bullets.update()

        for enemy in self.level.monsters:
            previous_pos = (enemy.rect.x, enemy.rect.y)
            enemy.update()
            enemy.update_animation()

            if enemy.dead and not self.level.graves:
                grave, key = enemy.create_grave_and_key()
                self.level.add_grave_and_key(grave, key, self)
                enemy.kill()

            if (enemy.rect.x, enemy.rect.y) != previous_pos:
                if not pygame.mixer.Channel(1).get_busy():
                    self.skeleton_steps_sound.play()

        enemy_hit, hit_enemy = self.level.check_bullet_collisions(self.tips)
        if enemy_hit:
            self.skeleton_steps_sound.stop()
            self.enemy_death_sound.play()

        key_collected = self.level.check_key_collection(self.hero)
        if key_collected:
            self.key_pickup_sound.play()

        if pygame.sprite.spritecollideany(self.hero, self.level.monsters):
            self.stop_gameplay_sounds()
            self.game_music.stop()
            self.lose_sound.play()
            
            self.quit_button = ImageButton(
                (WINDOW_WIDTH / 2) - 100, 350, 200, 65,
                MENU_BUTTON_EXIT_PASSIVE, MENU_BUTTON_EXIT_ACTIVE, 
                "menu/click.mp3", 0.3
            )
            self.window.blit(self.lose_fon, (0, 0))
            self.window.blit(self.lose_image, (150, 50))
            self.finish = True
            return

        if pygame.sprite.collide_rect(self.hero, self.level.final_door):
            if self.level.key_collected:
                self.stop_gameplay_sounds()
                self.door_unlock_sound.play()
                self.game_music.stop()
                self.win_sound.play()
                
                self.quit_button = ImageButton(
                    (WINDOW_WIDTH / 2) - 100, 350, 200, 65,
                    MENU_BUTTON_EXIT_PASSIVE, MENU_BUTTON_EXIT_ACTIVE, 
                    "menu/click.mp3", 0.3
                )
                self.window.blit(self.win_fon, (0, 0))
                self.window.blit(self.win_image, (150, 50))
                self.finish = True

    def render(self):
        if not self.finish:
            self.window.blit(self.bg, (0, 0))

            self.level.final_door.reset(self.window)
            self.level.tip_1.reset(self.window)

            if self.level.graves:
                self.level.graves.draw(self.window)
                self.level.keys.update()
                self.level.keys.draw(self.window)

            self.hero.reset(self.window)

            self.level.barriers.draw(self.window)

            self.level.monsters.draw(self.window)

            self.level.bullets.draw(self.window)

            self.level.update_tips(self.tips, self.window)

        if self.finish:
            if self.quit_button:
                mouse_pos = pygame.mouse.get_pos()
                self.quit_button.check_hover(mouse_pos)
                self.quit_button.draw(self.window)
            pygame.display.update()
            return

        pygame.display.update()

    def run(self):
        self.game_music.play(loops=-1)
        
        while self.running:
            self.handle_events()

            self.update()

            self.render()

            self.clock.tick(FPS)

        self.game_music.stop()
        
        return