import pygame

class Pacman:
    def __init__(self, start_x, start_y, level):
        self.x = start_x
        self.y = start_y
        self.level = level
        self.direction = 'right'
        self.score = 0
        self.lives = 3
        self.dead = False
    
    def handle_keypress(self, event):
        if event.key == pygame.K_RIGHT:
            if self.is_valid_move(self.x + 1, self.y):
                self.x += 1
                self.direction = 'right'
            else:
                self.direction = None
        elif event.key == pygame.K_LEFT:
            if self.is_valid_move(self.x - 1, self.y):
                self.x -= 1
                self.direction = 'left'
            else:
                self.direction = None
        elif event.key == pygame.K_UP:
            if self.is_valid_move(self.x, self.y - 1):
                self.y -= 1
                self.direction = 'up'
            else:
                self.direction = None
        elif event.key == pygame.K_DOWN:
            if self.is_valid_move(self.x, self.y + 1):
                self.y += 1
                self.direction = 'down'
            else:
                self.direction = None
    
    def is_valid_move(self, x, y):
        pass
    



    
