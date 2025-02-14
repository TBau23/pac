# Key
# S = Start
# . = Dot
# P = Powerup
# W = Wall
class Level:
    def __init__(self, level_file):
        self.level = self.load_level(level_file)
        self.dots = {}
        self.powerups = {}

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
            

l = Level('levels/level1.txt')