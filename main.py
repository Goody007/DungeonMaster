import pygame
import sys
from menu import Menu

def main():
    try:
        # Initialize pygame mixer for sound support
        pygame.mixer.init()
        # Set a higher number of audio channels to handle multiple sounds
        pygame.mixer.set_num_channels(8)
        
        menu = Menu()
        menu.run()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
