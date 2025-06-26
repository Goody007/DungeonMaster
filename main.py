import pygame
import sys
from menu import Menu

def main():
    try:
        menu = Menu()
        menu.run()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
