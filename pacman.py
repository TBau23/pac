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
        self.queued_direction = None  # Store the next turn
        self.score = 0
        self.lives = 3
        self.dead = False
        self.speed = 2
        self.mouth_angle = 45  # Angle for the mouth opening
        self.mouth_opening = True  # Whether mouth is opening or closing
        self.rotation = 0
        self.ghost_score_multiplier = 1  # For consecutive ghost eating

    def handle_keypress(self, event):
        # Store the requested direction instead of immediately changing
        if event.key == pygame.K_RIGHT:
            self.queued_direction = 'right'
        elif event.key == pygame.K_LEFT:
            self.queued_direction = 'left'
        elif event.key == pygame.K_UP:
            self.queued_direction = 'up'
        elif event.key == pygame.K_DOWN:
            self.queued_direction = 'down'

    def is_aligned_with_grid(self):
        # Check if Pac-Man is aligned with the grid
        return (self.pixel_x % CELL_SIZE == 0 and 
                self.pixel_y % CELL_SIZE == 0)

    def try_queued_direction(self):
        if self.queued_direction and self.is_aligned_with_grid():
            # Calculate the next grid position for the queued direction
            next_grid_x = self.grid_x
            next_grid_y = self.grid_y
            
            if self.queued_direction == 'right':
                next_grid_x += 1
            elif self.queued_direction == 'left':
                next_grid_x -= 1
            elif self.queued_direction == 'up':
                next_grid_y -= 1
            elif self.queued_direction == 'down':
                next_grid_y += 1

            # If the turn is valid, make it
            if self.is_valid_move(next_grid_x, next_grid_y):
                self.direction = self.queued_direction
                self.queued_direction = None

    def move(self):
        # Try to make the queued turn first
        self.try_queued_direction()

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

            # Calculate the grid position we're moving to
            next_grid_x = next_pixel_x // CELL_SIZE
            next_grid_y = next_pixel_y // CELL_SIZE
            
            # For right and down movement, check the far edge
            if self.direction in ['right', 'down']:
                edge_x = (next_pixel_x + (CELL_SIZE - 1)) // CELL_SIZE
                edge_y = (next_pixel_y + (CELL_SIZE - 1)) // CELL_SIZE
                if not (self.is_valid_move(next_grid_x, next_grid_y) and 
                       self.is_valid_move(edge_x, edge_y)):
                    # Snap to grid if we can't move
                    self.pixel_x = self.grid_x * CELL_SIZE
                    self.pixel_y = self.grid_y * CELL_SIZE
                    return

            # Otherwise just check the next position
            elif not self.is_valid_move(next_grid_x, next_grid_y):
                # Snap to grid if we can't move
                self.pixel_x = self.grid_x * CELL_SIZE
                self.pixel_y = self.grid_y * CELL_SIZE
                return

            # Update pixel position
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
                    # Reset ghost score multiplier when a new power pellet is eaten
                    self.ghost_score_multiplier = 1

    def eat_ghost(self):
        # Score for eating a ghost doubles for each ghost eaten during one power pellet
        ghost_points = 200 * self.ghost_score_multiplier
        self.score += ghost_points
        self.ghost_score_multiplier *= 2
        return ghost_points

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

    def draw(self, screen):
        # Draw the base yellow circle
        center_x = self.pixel_x + CELL_SIZE // 2
        center_y = self.pixel_y + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        # Base circle
        pygame.draw.circle(screen, 'yellow', (center_x, center_y), radius)
        
        # Update mouth animation
        if self.mouth_opening:
            self.mouth_angle += 3
            if self.mouth_angle >= 45:
                self.mouth_opening = False
        else:
            self.mouth_angle -= 3
            if self.mouth_angle <= 5:
                self.mouth_opening = True
        
        # Set rotation based on direction
        if self.direction == 'right':
            self.rotation = 0
        elif self.direction == 'left':
            self.rotation = 180
        elif self.direction == 'up':
            self.rotation = 90
        elif self.direction == 'down':
            self.rotation = 270
        
        # Draw mouth using an arc
        # Convert rotation and mouth angle to radians for pygame
        start_angle = math.radians(self.rotation - self.mouth_angle)
        end_angle = math.radians(self.rotation + self.mouth_angle)
        
        # Draw the mouth as a black "pie slice"
        pygame.draw.arc(screen, 'black', 
                    (center_x - radius, center_y - radius, 
                        radius * 2, radius * 2),
                    start_angle, end_angle, radius)