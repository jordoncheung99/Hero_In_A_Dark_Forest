from HeroInADarkForest import Tile
from HeroInADarkForest import hero
from HeroInADarkForest import utils

class Map:
    size_x = 21
    size_y = 21
    world = []
    hero = hero.Hero()
    debug = False
    tile_json_path = "jsons/tiles.json"
    sight_range = 2

    def __init__(self):
        self.reset()

    def create_map(self):
        # initialize map
        row = []
        for i in range(0, self.size_x):
            for j in range(0, self.size_y):
                row.append(Tile.Tile(0, "hello", False, None))
            self.world.append(row)
            row = []
        self.read_map()

    def printUI(self):
        string = "You are at " + str(self.hero.x) + ", " + str(self.hero.y)
        string += " health: " + str(self.hero.health) + " enter help for instruction"
        utils.display_print(string)

    def printMap(self):

        # for local map only
        min_x = -self.sight_range
        max_x = self.sight_range + 1
        min_y = -self.sight_range
        max_y = self.sight_range + 1

        # Calculate the x sight range
        # -1 for array shenanigans
        if self.hero.x + self.sight_range > self.size_x-1:
            diff = self.size_x-1 - (self.hero.x + self.sight_range)
            min_x += diff
            max_x += diff

        if self.hero.x - self.sight_range < 0:
            diff = (self.hero.x - self.sight_range)
            min_x -= diff
            max_x -= diff

        if self.hero.y + self.sight_range > self.size_y-1:
            diff = self.size_y-1 - (self.hero.y + self.sight_range)
            min_y += diff
            max_y += diff

        if self.hero.y - self.sight_range < 0:
            diff = (self.hero.y - self.sight_range)
            min_y -= diff
            max_y -= diff

        utils.display_print("```")
        for j in range(self.hero.y + min_y, self.hero.y + max_y):
            row = ""
            for i in range(self.hero.x + min_x, self.hero.x + max_x):
                char = self.world[i][j].print()
                if self.hero.x == i and self.hero.y == j:
                    char = "H"
                row = row + str(char) + " "
            utils.display_print(row)
        utils.display_print("```")
        # for displaying the whole map
        # for j in range(0, self.size_y):
        #     row = ""
        #     for i in range(0, self.size_x):
        #         char = self.world[i][j].print()
        #         if self.hero.x == i and self.hero.y == j:
        #             char = "H"
        #         row = row + str(char) + " "
        #     print(row)

    def movement_command(self, direction):
        x, y = self.get_next_pos(direction, self.hero.x, self.hero.y)

        # Check if out of bounds
        x_bound = x >= self.size_x or x < 0
        y_bound = y >= self.size_y or y < 0
        if x_bound or y_bound:
            print("You still need to do things here")
            return False

        if self.debug:
            print(self.hero.health)
            print("going", direction)
            print(x, y)
            print(self.hero.x, self.hero.y)

        # Check If the tile can be entered
        if self.world[x][y].wall:
            utils.display_print(self.world[x][y].description)
            return False

        # Move hero
        self.hero.x = x
        self.hero.y = y
        utils.display_print(self.world[x][y].description)
        return True


    def get_next_pos(self, direction, x, y):
        # 1 up
        # 2 down
        # 3 left
        # 4 right
        if direction == 1:
            y -= 1
        elif direction == 2:
            y += 1
        elif direction == 3:
            x -= 1
        elif direction == 4:
            x += 1
        return x, y

    def read_map(self):
        data = utils.read_json(self.tile_json_path)
        for tile in data:
            actual_tile = Tile.Tile(tile["char"], tile["desc"], tile["wall"], tile["event_id"])
            self.world[tile["x"]][tile["y"]] = actual_tile

    def get_current_pos(self):
        if self.debug:
            print(self.hero.x, self.hero.y)
        return self.hero.x, self.hero.y

    def set_desc(self, x, y, desc):
        self.world[x][y].set_desc(desc)

    def set_tile(self, x, y, desc, char, wall):
        self.world[x][y].set_tile(desc, char, wall)

    def reset(self):
        self.create_map()
        self.hero.reset()
