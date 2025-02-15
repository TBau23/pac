import pygame
import math
from constants import CELL_SIZE

class Pacman:
    def __init__(self, start_x, start_y, level):
        self.grid_x = start_x
        self.grid_y = start_y
        self.pixel_x = start_x * CELL_SIZE
        self.pixel_y = start_y * CELL_SIZE
        self.level = level
        self.direction = None
        self.score = 0
        self.lives = 3
        self.dead = False
        self.speed = 2

    def draw(self, screen):
        # Draw the base yellow circle
        center_x = self.pixel_x + CELL_SIZE // 2
        center_y = self.pixel_y + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        # Base circle
        pygame.draw.circle(screen, 'yellow', (center_x, center_y), radius)
        
        # Draw mouth as black triangle
        # Points for the triangle
        mouth_points = [
            (center_x, center_y),  # Center point
            (center_x + radius, center_y - radius//2),  # Top right
            (center_x + radius, center_y + radius//2)   # Bottom right
        ]
        pygame.draw.polygon(screen, 'black', mouth_points)

    
    def handle_keypress(self, event):
        if event.key == pygame.K_RIGHT:
            self.direction = 'right'
        elif event.key == pygame.K_LEFT:
            self.direction = 'left'
        elif event.key == pygame.K_UP:
            self.direction = 'up'
        elif event.key == pygame.K_DOWN:
            self.direction = 'down'
    
    def is_valid_move(self, next_grid_x, next_grid_y):
        # Check bounds
        inbounds = (next_grid_x >= 0 and 
                    next_grid_x < len(self.level.level[0]) and 
                    next_grid_y >= 0 and 
                    next_grid_y < len(self.level.level))
        if not inbounds:
            return False
            
        # Check for wall
        return not self.level.is_wall(next_grid_x, next_grid_y)

    def move(self):
        if self.direction:
            # Calculate next pixel position
            next_pixel_x = self.pixel_x
            next_pixel_y = self.pixel_y
            
            if self.direction == 'right':
                next_pixel_x += self.speed
            elif self.direction == 'left':
                next_pixel_x -= self.speed
            elif self.direction == 'up':
                next_pixel_y -= self.speed
            elif self.direction == 'down':
                next_pixel_y += self.speed

            # Calculate the grid position we're moving to, considering Pac-Man's size
            next_grid_x = next_pixel_x // CELL_SIZE
            next_grid_y = next_pixel_y // CELL_SIZE
            
            # For right and down movement, also check the cell we might overlap into
            if self.direction in ['right', 'down']:
                # Check the far edge of Pac-Man's position
                edge_x = (next_pixel_x + (CELL_SIZE - 1)) // CELL_SIZE
                edge_y = (next_pixel_y + (CELL_SIZE - 1)) // CELL_SIZE
                
                # Only move if both current cell and next cell are valid
                if self.is_valid_move(next_grid_x, next_grid_y) and self.is_valid_move(edge_x, edge_y):
                    self.pixel_x = next_pixel_x
                    self.pixel_y = next_pixel_y
                    
                    # Update grid position when we've moved to a new cell
                    if self.grid_x != next_grid_x or self.grid_y != next_grid_y:
                        self.grid_x = next_grid_x
                        self.grid_y = next_grid_y
                        if self.level.collect_dot(self.grid_x, self.grid_y):
                            self.score += 10
                        if self.level.collect_powerup(self.grid_x, self.grid_y):
                            self.score += 50
            else:
                # For left and up movement, we can use the original logic
                if self.is_valid_move(next_grid_x, next_grid_y):
                    self.pixel_x = next_pixel_x
                    self.pixel_y = next_pixel_y
                    
                    if self.grid_x != next_grid_x or self.grid_y != next_grid_y:
                        self.grid_x = next_grid_x
                        self.grid_y = next_grid_y
                        if self.level.collect_dot(self.grid_x, self.grid_y):
                            self.score += 10
                        if self.level.collect_powerup(self.grid_x, self.grid_y):
                            self.score += 50

    
