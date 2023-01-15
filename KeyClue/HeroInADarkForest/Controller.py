from HeroInADarkForest import map
from HeroInADarkForest import item_handler
from HeroInADarkForest import utils
from HeroInADarkForest import event_handler

class HeroController:

    def __init__(self):
        self.world = map.Map()
        self.itemHandler = item_handler.ItemHandler()
        self.eventHandler = event_handler.EventHandler(self.itemHandler, self.world)

    def run_game(self):
        while True:
            test = utils.Utils()
            # utils.Utils.test_func()
            self.world.printUI()
            self.world.printMap()
            command = test.get_user_input()
            # command = utils.get_user_input()
            self.parse_command(command)

    def display(self):
        self.world.printUI()
        self.world.printMap()

    def step(self, command):
        if command == "restart":
            self.restart_game()
            self.display()
            return
        if self.eventHandler.in_battle():
            self.eventHandler.battle(command)
            # No longer in battle = display map
            if self.eventHandler.check_reset():
                self.restart_game()
            if not self.eventHandler.in_battle():
                self.display()
        else:
            self.parse_command(command)
            self.display()


    def parse_command(self, string):
        if self.parse_movement(string):
            return
        if self.parse_pickup(string):
            return
        if self.parse_items(string):
            return
        if self.parse_use_item(string):
            return
        if self.parse_help(string):
            return
        if string == "breakmefromthesechains":
            self.eventHandler.insight()
            return
        utils.display_print(string + " is not a valid command")

    def parse_help(self, string):
        if string != "help":
            return False
        string = "You are a hero in a lost forest, you set out to free these lands from the evil beast and return sun to these lands"
        string += "\ntype up, u, n, north to move up"
        string += "\ntype down, d, s, south to move down"
        string += "\ntype left, l, e, east to move left"
        string += "\ntype right, r, w, west to move right"
        string += "\ntype use to use an item, then type its name (spaces and punctuation matters!)"
        string += "\ntype items to see what items you have"
        string += "\ntype pickup to pick up an item"
        string += "\ntype restart to restart the game"
        utils.display_print(string)
        return True

    def parse_movement(self, string):
        died = False
        valid = False
        if string == "up" or string == "n" or string == "u" or string == "north":
            died = self.eventHandler.movement_command(1)
            valid = True
        elif string == "down" or string == "s" or string == "d" or string == "south":
            died = self.eventHandler.movement_command(2)
            valid = True
        elif string == "left" or string == "w" or string == "l" or string == "west":
            died = self.eventHandler.movement_command(3)
            valid = True
        elif string == "right" or string == "e" or string == "r" or string == "east":
            died = self.eventHandler.movement_command(4)
            valid = True
        if died:
            print("You Died")
            self.restart_game()
        return valid

    def parse_pickup(self, string):
        if string != "pickup":
            return False
        # get x and y
        x, y = self.world.get_current_pos()
        item_picked, desc = self.itemHandler.pick_up(x, y)
        if item_picked:
            self.world.set_desc(x, y, desc)
        return True

    def parse_use_item(self, string):
        if not string.startswith("use"):
            return False
        has_items = self.itemHandler.has_items()
        if not has_items:
            utils.display_print("You have no items to use")
            return True
        split = string.split(" ", 1)
        item_name = split[1]
        print(item_name)
        x, y = self.world.get_current_pos()
        self.eventHandler.use_item(item_name, x, y)
        return True

    def parse_items(self, string):
        if string != "items":
            return False
        self.itemHandler.display_owned_items()
        return True

    def restart_game(self):
        self.world.reset()
        self.itemHandler = item_handler.ItemHandler()
        self.eventHandler = event_handler.EventHandler(self.itemHandler, self.world)

if __name__ == '__main__':
    hc = HeroController()
    hc.run_game()
