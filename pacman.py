import pygame
from constants import CELL_SIZE

class Pacman:
    def __init__(self, start_x, start_y, level):
        self.x = start_x
        self.y = start_y
        self.level = level
        self.direction = None
        self.score = 0
        self.lives = 3
        self.dead = False

    def draw(self, screen):
        # Convert grid coordinates to pixel coordinates
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
    
        # Draw Pac-Man as a yellow circle
        radius = CELL_SIZE // 2  # or slightly smaller like CELL_SIZE // 2 - 2
        pygame.draw.circle(screen, 'yellow', (center_x, center_y), radius)

    
    def handle_keypress(self, event):
        if event.key == pygame.K_RIGHT:
            self.direction = 'right'
        elif event.key == pygame.K_LEFT:
            self.direction = 'left'
        elif event.key == pygame.K_UP:
            self.direction = 'up'
        elif event.key == pygame.K_DOWN:
            self.direction = 'down'
    
    def is_valid_move(self, x, y):
        inbounds = x >= 0 and x < len(self.level.level[0]) and y >= 0 and y < len(self.level.level)
        if not inbounds:
            return False
        if self.level.is_wall(x, y):
            return False
        return True

    def move(self):
        next_x, next_y = self.x, self.y
        
        if self.direction == 'right':
            next_x += 1
        elif self.direction == 'left':
            next_x -= 1
        elif self.direction == 'up':
            next_y -= 1
        elif self.direction == 'down':
            next_y += 1
            
        if self.is_valid_move(next_x, next_y):
            self.x = next_x
            self.y = next_y
            if self.level.collect_dot(self.x, self.y):
                self.score += 10
            if self.level.collect_powerup(self.x, self.y):
                self.score += 50
                # trigger power mode here later

    



    
