from HeroInADarkForest import utils
from HeroInADarkForest import battle
import math


class RemoteTile:
    def __init__(self, event_id, x, y, char, desc, wall):
        self.event_id = event_id
        self.x = x
        self.y = y
        self.char = char
        self.desc = desc
        self.wall = wall

class EventHandler:
    remote_tile_json_path = "jsons/remote_tile.json"
    use_event_json_path = "jsons/use_event.json"
    move_events_json_path = "./jsons/move_event.json"
    use_item_event_json_path ="./jsons/use_items.json"
    jab_path = "./jsons/jab.json"
    remote_tiles = []
    use_events = []
    move_events = []
    use_item_event = []
    jab_tiles = []
    battle_handler = battle.BattleSystem()

    def __init__(self, item_handler, world):
        self.item_handler = item_handler
        self.world = world
        self.reset()
        self.eyesWideOpen = False
        self.jab_tiles = utils.read_json(self.jab_path)

    def read_use_item_events(self):
        self.use_item_event = utils.read_json(self.use_item_event_json_path)

    def read_remote_tiles(self):
        data = utils.read_json(self.remote_tile_json_path)
        for i in range(len(data)):
            rt = data[i]
            tile = RemoteTile(rt["id"], rt["x"], rt["y"], rt["char"], rt["desc"], rt["wall"])
            self.remote_tiles.append(tile)

    def read_use_events(self):
        self.use_events = utils.read_json(self.use_event_json_path)

    def read_move_events(self):
        self.move_events = utils.read_json(self.move_events_json_path)

    def use_item(self, item_name, x, y):
        use_id = -1
        #Check if you own the item
        even_an_item = False
        for i in self.item_handler.items:
            if i.name.lower() == item_name:
                even_an_item = True
                break
        if not even_an_item:
            utils.display_print("You don't own " + item_name)
            return
        for i in range(len(self.use_events)):
            event = self.use_events[i]
            if event["x"] != x or event["y"] != y or event["item"] != item_name:
                continue
            use_id = event["use_id"]
            utils.display_print(event["message"])
            # Remote tile event
            if event["remote_tile_id"] != -1:
                self.remote_tile_event(event["remote_tile_id"])

            if event["remote_item_id"] != -1:
                self.get_item_event(event["remote_item_id"])

            # Special one off case for mr rock
            if event["movement_id"] != 0:
                for me in self.move_events:
                    if me["enemy_id"] == -2:
                        self.move_events.remove(me)
            # Remove the item
            if event["consumed"]:
                self.item_handler.remove_item(item_name)
            break

        # Remove all similar events
        if use_id != -1:
            # Have to iterate backwards due to array changing size shenanigans
            length = len(self.use_events)
            for i in range(length):
                index = length - i - 1
                if self.use_events[index]["use_id"] == use_id:
                    self.use_events.pop(index)
            return

        # No event/item matches
        utils.display_print("You can't use " + item_name + " here")
        return

    def remote_tile_event(self, event_id):
        for tile in self.remote_tiles:
            if tile.event_id != event_id:
                continue
            # Set tile
            self.world.set_tile(tile.x, tile.y, tile.desc, tile.char, tile.wall)

    def movement_command(self, direction):
        moved = self.world.movement_command(direction)
        if not moved:
            return

        return self.movement_event()
        # Check if a events happens here

    def end_game(self):
        ending = 0
        utils.display_print("The beast has been slain, now you seek to restore the sun...")
        utils.display_print("You stand upon the pedestal that dragon guarded, its power long since faded...")
        for i in self.item_handler.items:
            if i.name.lower() == "fire stone":
                ending = 1
                utils.display_print("You place the firestone upon the pedestal")
                utils.display_print("It glows with a dim light, perhaps if it was restored to its former power it "
                                    "could do more")
                utils.display_print("For another 100 years the sun shall last, another hero could finish what you "
                                    "started")
                break
            elif i.name.lower() == "sun stone":
                utils.display_print("You place the sunstone upon the pedestal")
                utils.display_print("As the bright light engulfs the cave you hear a voice")
                utils.display_print("\"Proclaim to the gods \'BreakMeFromTheseChains\'\"")
                ending = 2
                break
        if ending == 0:
            utils.display_print("You lack any item to fuel this mechanism, you can only offer your life.")
            utils.display_print("The sun glows dim for another hero to take up the trial")
        print("you ended the game: ", ending)
        self.world.hero.take_damage(999)

    def movement_event(self):
        x, y = self.world.get_current_pos()
        # Check if its the end of the game
        if self.eyesWideOpen:
            jab_x = math.floor(x / 3)
            jab_y = math.floor(y / 3)
            utils.display_print("This area glows of " + str(self.jab_tiles[jab_x + jab_y * 7]["colour"]))


        if x == 0 and y == 20:
            self.end_game()
            return True

        for event in self.move_events:
            if event["x"] == x and event["y"] == y:
                # Event has been triggered
                if event["trap"] != 0:
                    self.world.hero.take_damage(event["trap"])
                    self.move_events.remove(event)
                    return False
                else:
                    # Battle time
                    self.move_events.remove(event)
                    return self.battle_handler.start_battle(self.item_handler.get_items(), self.world.hero, event["enemy_id"])

    def get_item_event(self, item_id):
        for e in self.use_item_event:
            if e["id"] == item_id:
                self.item_handler.add_item(e["desc"], e["name"])
                return

    def reset(self):
        self.read_use_events()
        self.read_remote_tiles()
        self.read_move_events()
        self.read_use_item_events()
        self.battle_handler.restart()

    def in_battle(self):
        return self.battle_handler.in_battle

    def battle(self, command):
        self.battle_handler.step_battle(command)

    def check_reset(self):
        return self.battle_handler.dead

    def insight(self):
        self.eyesWideOpen = True


