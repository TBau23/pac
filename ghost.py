import pygame
import random
import math
from constants import CELL_SIZE

class Ghost:
    def __init__(self, start_x, start_y, level, ghost_type, pacman):
        self.grid_x = start_x
        self.grid_y = start_y
        self.pixel_x = start_x * CELL_SIZE
        self.pixel_y = start_y * CELL_SIZE
        
        self.level = level
        self.ghost_type = ghost_type  # 'blinky', 'pinky', 'inky', or 'clyde'
        self.pacman = pacman  # Reference to pacman for targeting
        self.direction = 'left'  # Default starting direction
        self.speed = 2
        self.vulnerable = False  # For power pellet mode
        self.vulnerability_timer = 0
        self.scared_time = 10 * 60  # 10 seconds at 60 FPS
        self.returning_home = False  # For when eaten while vulnerable
        self.home_position = (start_x, start_y)
        
        self.colors = {
            'blinky': 'red',
            'pinky': 'pink',
            'inky': 'cyan',
            'clyde': 'orange'
        }
        
        # Animation frames for ghosts
        self.animation_frame = 0
        self.animation_speed = 0.2

    def is_aligned_with_grid(self):
        # Check if Ghost is aligned with the grid
        return (self.pixel_x % CELL_SIZE == 0 and 
                self.pixel_y % CELL_SIZE == 0)

    def is_valid_move(self, next_grid_x, next_grid_y):
        # Check bounds
        in_bounds = (next_grid_x >= 0 and 
                   next_grid_x < len(self.level.level[0]) and 
                   next_grid_y >= 0 and 
                   next_grid_y < len(self.level.level))
        if not in_bounds:
            return False
            
        # Check for wall
        return not self.level.is_wall(next_grid_x, next_grid_y)
    
    def get_target_tile(self):
        if self.vulnerable:
            # Run away from Pacman when vulnerable
            return self.get_random_target()
        
        if self.returning_home:
            return self.home_position
            
        # Different targeting strategies based on ghost type
        if self.ghost_type == 'blinky':
            # Blinky directly targets Pacman
            return (self.pacman.grid_x, self.pacman.grid_y)
            
        elif self.ghost_type == 'pinky':
            # Pinky targets 4 tiles ahead of Pacman
            dx, dy = 0, 0
            if self.pacman.direction == 'right':
                dx = 4
            elif self.pacman.direction == 'left':
                dx = -4
            elif self.pacman.direction == 'up':
                dy = -4
            elif self.pacman.direction == 'down':
                dy = 4
            return (self.pacman.grid_x + dx, self.pacman.grid_y + dy)
            
        elif self.ghost_type == 'inky':
            # Inky targets a position that is the vector from Blinky to 2 spaces ahead of Pacman, doubled
            dx, dy = 0, 0
            if self.pacman.direction == 'right':
                dx = 2
            elif self.pacman.direction == 'left':
                dx = -2
            elif self.pacman.direction == 'up':
                dy = -2
            elif self.pacman.direction == 'down':
                dy = 2
                
            # Calculate position 2 tiles ahead of Pacman
            pacman_ahead_x = self.pacman.grid_x + dx
            pacman_ahead_y = self.pacman.grid_y + dy
            
            # Assume Blinky is at a default position if not implemented
            blinky_x, blinky_y = 0, 0
            
            # Double the vector from Blinky to the space ahead of Pacman
            vector_x = pacman_ahead_x - blinky_x
            vector_y = pacman_ahead_y - blinky_y
            
            target_x = pacman_ahead_x + vector_x
            target_y = pacman_ahead_y + vector_y
            
            return (target_x, target_y)
            
        elif self.ghost_type == 'clyde':
            # Clyde targets Pacman when far away, but moves to a corner when close
            distance = math.sqrt((self.grid_x - self.pacman.grid_x)**2 + 
                                (self.grid_y - self.pacman.grid_y)**2)
            
            if distance > 8:  # Target Pacman when far away
                return (self.pacman.grid_x, self.pacman.grid_y)
            else:  # Move to bottom-left corner when close
                return (1, len(self.level.level) - 2)
                
        # Default behavior (random movement)
        return self.get_random_target()
    
    def get_random_target(self):
        # Choose a random location for scatter mode or scared behavior
        random_x = random.randint(0, len(self.level.level[0]) - 1)
        random_y = random.randint(0, len(self.level.level) - 1)
        return (random_x, random_y)
        
    def choose_direction(self):
        if not self.is_aligned_with_grid():
            return self.direction
            
        # Can't reverse direction
        opposite_directions = {
            'right': 'left',
            'left': 'right',
            'up': 'down',
            'down': 'up'
        }
        
        # Get the possible directions (excluding walls and the opposite direction)
        possible_directions = []
        
        # Check each direction
        directions = ['right', 'up', 'left', 'down']
        for direction in directions:
            next_grid_x, next_grid_y = self.grid_x, self.grid_y
            
            if direction == 'right':
                next_grid_x += 1
            elif direction == 'left':
                next_grid_x -= 1
            elif direction == 'up':
                next_grid_y -= 1
            elif direction == 'down':
                next_grid_y += 1
                
            # Don't allow moving in the opposite direction
            if direction == opposite_directions.get(self.direction):
                continue
                
            if self.is_valid_move(next_grid_x, next_grid_y):
                possible_directions.append(direction)
        
        # If no valid directions (except the opposite), allow reversing
        if not possible_directions:
            opposite = opposite_directions.get(self.direction)
            next_grid_x, next_grid_y = self.grid_x, self.grid_y
            
            if opposite == 'right':
                next_grid_x += 1
            elif opposite == 'left':
                next_grid_x -= 1
            elif opposite == 'up':
                next_grid_y -= 1
            elif opposite == 'down':
                next_grid_y += 1
                
            if self.is_valid_move(next_grid_x, next_grid_y):
                return opposite
            return self.direction  # No valid moves, keep current direction
            
        # Choose the direction closest to the target
        target_x, target_y = self.get_target_tile()
        best_direction = None
        best_distance = float('inf')
        
        for direction in possible_directions:
            next_grid_x, next_grid_y = self.grid_x, self.grid_y
            
            if direction == 'right':
                next_grid_x += 1
            elif direction == 'left':
                next_grid_x -= 1
            elif direction == 'up':
                next_grid_y -= 1
            elif direction == 'down':
                next_grid_y += 1
                
            # Calculate the distance to the target
            distance = math.sqrt((next_grid_x - target_x)**2 + (next_grid_y - target_y)**2)
            
            # If this direction is better, save it
            if distance < best_distance:
                best_distance = distance
                best_direction = direction
                
        return best_direction or self.direction
    
    def move(self):
        # Update direction when aligned with grid
        if self.is_aligned_with_grid():
            self.direction = self.choose_direction()
        
        # Calculate next position
        next_pixel_x = self.pixel_x
        next_pixel_y = self.pixel_y
        
        # Adjust speed if vulnerable
        current_speed = self.speed / 2 if self.vulnerable else self.speed
        
        if self.direction == 'right':
            next_pixel_x += current_speed
        elif self.direction == 'left':
            next_pixel_x -= current_speed
        elif self.direction == 'up':
            next_pixel_y -= current_speed
        elif self.direction == 'down':
            next_pixel_y += current_speed
            
        # Calculate grid position
        next_grid_x = int(next_pixel_x // CELL_SIZE)
        next_grid_y = int(next_pixel_y // CELL_SIZE)
        
        # Check for edge cases with 'right' and 'down' directions
        if self.direction in ['right', 'down']:
            edge_x = int((next_pixel_x + (CELL_SIZE - 1)) // CELL_SIZE)
            edge_y = int((next_pixel_y + (CELL_SIZE - 1)) // CELL_SIZE)
            if not (self.is_valid_move(next_grid_x, next_grid_y) and 
                   self.is_valid_move(edge_x, edge_y)):
                # Snap to grid if we can't move
                self.pixel_x = self.grid_x * CELL_SIZE
                self.pixel_y = self.grid_y * CELL_SIZE
                return
        elif not self.is_valid_move(next_grid_x, next_grid_y):
            # Snap to grid if we can't move
            self.pixel_x = self.grid_x * CELL_SIZE
            self.pixel_y = self.grid_y * CELL_SIZE
            return
            
        # Update pixel position
        self.pixel_x = next_pixel_x
        self.pixel_y = next_pixel_y
        
        # Update grid position
        if self.grid_x != next_grid_x or self.grid_y != next_grid_y:
            self.grid_x = next_grid_x
            self.grid_y = next_grid_y
            
    def make_vulnerable(self):
        self.vulnerable = True
        self.vulnerability_timer = self.scared_time
        
    def update(self):
        # Move the ghost
        self.move()
        
        # Check collision with Pacman
        if self.check_collision_with_pacman():
            if self.vulnerable:
                self.returning_home = True
                self.vulnerable = False
                # Award points to pacman for eating ghost
                self.pacman.eat_ghost()
            else:
                self.pacman.dead = True  # Pacman is caught
                
        # Update vulnerability timer
        if self.vulnerable:
            self.vulnerability_timer -= 1
            if self.vulnerability_timer <= 0:
                self.vulnerable = False
                
        # Check if returned home
        if self.returning_home:
            if self.grid_x == self.home_position[0] and self.grid_y == self.home_position[1]:
                self.returning_home = False
                
        # Update animation
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 2:
            self.animation_frame = 0
            
    def check_collision_with_pacman(self):
        # Check if ghost and pacman are in the same grid cell
        return (self.grid_x == self.pacman.grid_x and 
                self.grid_y == self.pacman.grid_y)
    
    def draw(self, screen):
        # Calculate center of ghost
        center_x = self.pixel_x + CELL_SIZE // 2
        center_y = self.pixel_y + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        # Choose color based on state
        if self.vulnerable:
            color = 'blue'  # Blue when vulnerable
            if self.vulnerability_timer < 90 and self.animation_frame % 1 > 0.5:
                color = 'white'  # Flash white/blue when vulnerability is ending
        elif self.returning_home:
            color = 'white'  # White eyes only when returning home
        else:
            color = self.colors[self.ghost_type]
            
        # Draw the body
        if not self.returning_home:
            # Draw main body (semi-circle)
            pygame.draw.circle(screen, color, (center_x, center_y - 2), radius)
            
            # Draw bottom part (wavy)
            wave_height = abs(math.sin(self.animation_frame * math.pi)) * 3 + 2
            
            points = [
                (center_x - radius, center_y - 2),  # Bottom left of semi-circle
                (center_x - radius, center_y + wave_height),
                (center_x - radius + radius // 2, center_y - wave_height // 2),
                (center_x, center_y + wave_height),
                (center_x + radius // 2, center_y - wave_height // 2),
                (center_x + radius, center_y + wave_height),
                (center_x + radius, center_y - 2)  # Bottom right of semi-circle
            ]
            
            pygame.draw.polygon(screen, color, points)
            
        # Draw eyes (white circles)
        eye_radius = radius // 3
        eye_distance = radius // 2
        
        left_eye_pos = (center_x - eye_distance, center_y - eye_distance // 2)
        right_eye_pos = (center_x + eye_distance, center_y - eye_distance // 2)
        
        pygame.draw.circle(screen, 'white', left_eye_pos, eye_radius)
        pygame.draw.circle(screen, 'white', right_eye_pos, eye_radius)
        
        # Draw pupils (blue dots)
        pupil_radius = eye_radius // 2
        
        # Adjust pupil position based on direction
        pupil_offset_x, pupil_offset_y = 0, 0
        
        if self.direction == 'right':
            pupil_offset_x = pupil_radius
        elif self.direction == 'left':
            pupil_offset_x = -pupil_radius
        elif self.direction == 'up':
            pupil_offset_y = -pupil_radius
        elif self.direction == 'down':
            pupil_offset_y = pupil_radius
            
        left_pupil_pos = (left_eye_pos[0] + pupil_offset_x, left_eye_pos[1] + pupil_offset_y)
        right_pupil_pos = (right_eye_pos[0] + pupil_offset_x, right_eye_pos[1] + pupil_offset_y)
        
        pygame.draw.circle(screen, 'blue', left_pupil_pos, pupil_radius)
        pygame.draw.circle(screen, 'blue', right_pupil_pos, pupil_radius)