import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
#PACMAN

#MAP
#PACMAN
#GHOSTS
#PELLETS
#POWERPELLETS
#SCORE


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        screen.fill('black')

        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()
                
            