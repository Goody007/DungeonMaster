import pygame
import sys
from config import *
from buttons import ImageButton
from resources import ResourceManager
from game import Game

class Menu:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()   

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dungeon Master")

        self.background = ResourceManager.load_image(MENU_BG, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title_menu = ResourceManager.load_image(MENU_TITLE)
        
        self.background_music = pygame.mixer.Sound(MENU_MUSIC)
        self.background_music.set_volume(0.5)   
        self.background_music.play(loops=-1)  

        self.start_button = ImageButton(
            (WINDOW_WIDTH / 2) - 100, 200, 200, 65,
            MENU_BUTTON_START_PASSIVE, MENU_BUTTON_START_ACTIVE, "menu/click.mp3", 0.2
        )
        self.quit_button = ImageButton(
            (WINDOW_WIDTH / 2) - 100, 300, 200, 65,
            MENU_BUTTON_EXIT_PASSIVE, MENU_BUTTON_EXIT_ACTIVE, "menu/click.mp3", 0.2
        )

        self.clock = pygame.time.Clock()

        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.start_button.handle_event(event)
                self.quit_button.handle_event(event)
            elif event.type == pygame.USEREVENT:
                if event.button == self.start_button:
                    self.start_game()
                elif event.button == self.quit_button:
                    self.quit_game()

    def update(self):
        if not pygame.get_init():  
            return
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        title_x = (WINDOW_WIDTH - self.title_menu.get_width()) // 2
        self.screen.blit(self.title_menu, (title_x, 50))
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        pygame.display.flip()

    def start_game(self):
        self.background_music.stop()
        
        game = Game(self.background_music)  
        game.run()
        
        if self.running and pygame.get_init():
            self.background_music.play(loops=-1)

    def quit_game(self):
        self.running = False  
        self.background_music.stop()  
        pygame.quit()
        sys.exit()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            
            if pygame.get_init():
                self.render()
                self.clock.tick(FPS)
            else:
                self.running = False
