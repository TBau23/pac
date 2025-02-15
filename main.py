import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from level import Level
from pacman import Pacman

# Maze
# Pacman
# Ghosts


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()
    level = Level('levels/level1.txt')
    pacman = Pacman(8, 14, level)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pacman.handle_keypress(event)
        
        pacman.move()
        # drawing
        screen.fill('black')
        level.draw(screen)
        pacman.draw(screen)

        # update display
        pygame.display.flip()
        clock.tick(FPS)
    
main()


