import pygame
from constants import CELL_SIZE
# Key
# S = Start
# . = Dot
# P = Powerup
# W = Wall
class Level:
    def __init__(self, level_file):
        self.dots = {}
        self.powerups = {}
        self.level = self.load_level(level_file)

    def load_level(self, level_file):
        level = []
        with open(level_file, 'r') as file:
            lines = file.readlines()
            line_length = len(lines[0].strip())
            for y, line in enumerate(lines):
                stripped_line = line.strip()
                if stripped_line:  
                    if len(stripped_line) != line_length:
                        raise ValueError(f"Line length mismatch: {len(stripped_line)} != {line_length}")
                    row = []
                    for x, char in enumerate(stripped_line):
                        if char == '.':
                            self.dots[(x, y)] = True
                        elif char == 'P':
                            self.powerups[(x, y)] = True
                        row.append(char)
                    level.append(row)
        return level

    # will be called every frame
    def draw(self, screen):
        for y, row in enumerate(self.level):
            for x, char in enumerate(row):
                if char == 'W':
                    pygame.draw.rect(screen, 'blue',(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        for (x, y) in self.dots:
            pygame.draw.circle(screen, 'yellow', (x * CELL_SIZE + CELL_SIZE / 2, y * CELL_SIZE + CELL_SIZE / 2), CELL_SIZE / 10)
        
        for (x, y) in self.powerups:
            pygame.draw.circle(screen, 'red', (x * CELL_SIZE + CELL_SIZE / 2, y * CELL_SIZE + CELL_SIZE / 2), CELL_SIZE / 6)


    def is_wall(self, x, y):
        return self.level[y][x] == 'W'
    
    def collect_dot(self, x, y):
        if (x, y) in self.dots:
            del self.dots[(x, y)]
            return True
        return False
    
    def collect_powerup(self, x, y):
        if (x, y) in self.powerups:
            del self.powerups[(x, y)]
            return True
        return False
