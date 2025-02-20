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
        
        self.colors = {
            'blinky': 'red',
            'pinky': 'pink',
            'inky': 'cyan',
            'clyde': 'orange'
        }