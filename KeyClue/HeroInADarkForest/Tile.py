class Tile:
    def __init__(self, char, desc, wall, events):
        self.char = char
        self.description = desc
        self.wall = wall
        self.event = events

    def print(self):
        if self.char == 1:
            return "."
        return self.char

    def set_desc(self, desc):
        self.description = desc

    def set_tile(self, desc, char, wall):
        self.description = desc
        self.char = char
        self.wall = wall
