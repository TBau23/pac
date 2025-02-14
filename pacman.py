class Pacman:
    def __init__(self, start_x, start_y, level):
        self.x = start_x
        self.y = start_y
        self.level = level
        self.direction = None
        self.score = 0
        self.lives = 3
        self.dead = False
    
    def move(self, direction):
        pass
