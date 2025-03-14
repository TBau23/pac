import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CELL_SIZE
from level import Level
from pacman import Pacman
from ghost import Ghost

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()
    
    # Initialize game elements
    level = Level('levels/level1.txt')
    pacman = Pacman(8, 14, level)
    
    # Create ghosts with different personalities
    ghosts = [
        Ghost(13, 11, level, 'blinky', pacman),  # Red ghost - direct chaser
        Ghost(14, 11, level, 'pinky', pacman),   # Pink ghost - ambusher
        Ghost(13, 12, level, 'inky', pacman),    # Cyan ghost - unpredictable
        Ghost(14, 12, level, 'clyde', pacman)    # Orange ghost - random
    ]
    
    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pacman.handle_keypress(event)
        
        # Update game state
        pacman.move()
        
        # Check if power pellet was eaten
        if level.power_pellet_eaten:
            for ghost in ghosts:
                ghost.make_vulnerable()
            level.power_pellet_eaten = False
        
        # Update ghosts
        for ghost in ghosts:
            ghost.update()
        
        # Check if level is complete (all dots and power pellets eaten)
        if level.is_complete():
            # You could load the next level here or show a victory screen
            print("Level Complete!")
            pygame.quit()
            sys.exit()
            
        # Check if pacman is dead
        if pacman.dead:
            pacman.lives -= 1
            if pacman.lives <= 0:
                # Game over logic would go here
                print("Game Over!")
                pygame.quit()
                sys.exit()
            else:
                # Reset positions
                pacman.grid_x = 8
                pacman.grid_y = 14
                pacman.pixel_x = pacman.grid_x * CELL_SIZE
                pacman.pixel_y = pacman.grid_y * CELL_SIZE
                pacman.direction = None
                pacman.queued_direction = None
                pacman.dead = False
                pacman.ghost_score_multiplier = 1
                
                # Reset ghosts
                for i, ghost in enumerate(ghosts):
                    ghost.grid_x = 13 + (i % 2)
                    ghost.grid_y = 11 + (i // 2)
                    ghost.pixel_x = ghost.grid_x * CELL_SIZE
                    ghost.pixel_y = ghost.grid_y * CELL_SIZE
                    ghost.direction = 'left'
                    ghost.vulnerable = False
                    ghost.returning_home = False
        
        # Drawing
        screen.fill('black')
        level.draw(screen)
        pacman.draw(screen)
        
        # Draw ghosts
        for ghost in ghosts:
            ghost.draw(screen)
        
        # Draw score
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f'Score: {pacman.score}', True, 'white')
        screen.blit(score_text, (10, 10))
        
        # Draw lives
        lives_text = font.render(f'Lives: {pacman.lives}', True, 'white')
        screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
if __name__ == "__main__":
    main()