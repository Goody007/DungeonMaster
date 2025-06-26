import pygame
import sys
from config import *
from buttons import ImageButton
from resources import ResourceManager
from game import Game

class Menu:
    """Class for managing the game menu"""

    def __init__(self):
        """Initialize the game menu"""
        pygame.init()
        pygame.mixer.init()  # Инициализация аудио

        # Create the window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dungeon Master")

        # Load background and title images
        self.background = ResourceManager.load_image(MENU_BG, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background.set_alpha(64)
        self.title_menu = ResourceManager.load_image(MENU_TITLE)
        
        # Загрузка и воспроизведение фоновой музыки
        self.background_music = pygame.mixer.Sound(MENU_MUSIC)
        self.background_music.set_volume(0.5)  # Громкость от 0.0 до 1.0
        self.background_music.play(loops=-1)  # -1 означает бесконечное повторение

        # Create buttons с явно заданной громкостью звука (например, 0.2)
        self.start_button = ImageButton(
            (WINDOW_WIDTH / 2) - 100, 250, 200, 65,
            MENU_BUTTON_START_PASSIVE, MENU_BUTTON_START_ACTIVE, "menu/click.mp3", 0.2
        )
        self.quit_button = ImageButton(
            (WINDOW_WIDTH / 2) - 100, 350, 200, 65,
            MENU_BUTTON_EXIT_PASSIVE, MENU_BUTTON_EXIT_ACTIVE, "menu/click.mp3", 0.2
        )

        # Clock for FPS control
        self.clock = pygame.time.Clock()

        # Menu running flag
        self.running = True

    def handle_events(self):
        """Handle menu events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Просто вызываем quit_game, который уже содержит нужные вызовы
                self.quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Передаем событие кнопкам для воспроизведения звука
                self.start_button.handle_event(event)
                self.quit_button.handle_event(event)
            elif event.type == pygame.USEREVENT:
                # Обрабатываем пользовательское событие от кнопок
                if event.button == self.start_button:
                    self.start_game()
                elif event.button == self.quit_button:
                    self.quit_game()

    def update(self):
        """Update menu state"""
        if not pygame.get_init():  # Проверяем, инициализирована ли система pygame
            return
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)

    def render(self):
        """Render menu elements"""
        self.screen.blit(self.background, (0, 0))
        title_x = (WINDOW_WIDTH - self.title_menu.get_width()) // 2
        self.screen.blit(self.title_menu, (title_x, 50))
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        pygame.display.flip()

    def start_game(self):
        """Start the main game"""
        # Приостанавливаем музыку перед запуском игры
        self.background_music.stop()
        
        game = Game(self.background_music)  # Передаем музыку в игру
        game.run()
        
        # После возвращения из игры можем возобновить музыку в меню
        if self.running and pygame.get_init():
            self.background_music.play(loops=-1)

    def quit_game(self):
        """Quit the game"""
        self.running = False  # Устанавливаем флаг завершения
        self.background_music.stop()  # Останавливаем музыку перед выходом
        pygame.quit()
        sys.exit()

    def run(self):
        """Main menu loop"""
        while self.running:
            self.handle_events()
            self.update()
            
            # Проверяем, что pygame всё ещё инициализирован перед рендерингом
            if pygame.get_init():
                self.render()
                self.clock.tick(FPS)
            else:
                # Если pygame был закрыт, выходим из цикла
                self.running = False
