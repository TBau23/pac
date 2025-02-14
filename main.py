import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Maze
# Pacman
# Ghosts


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        

        # drawing
        screen.fill('black')

        # update display
        pygame.display.flip()
        clock.tick(FPS)
    
main()


