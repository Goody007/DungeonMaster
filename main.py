import pygame
import sys
from menu import Menu

def main():
    try:
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)
        
        menu = Menu()
        menu.run()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
