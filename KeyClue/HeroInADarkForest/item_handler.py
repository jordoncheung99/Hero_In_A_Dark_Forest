from HeroInADarkForest import utils

class GroundItem:
    def __init__(self, x, y, desc, set_desc, id_num, name, false_item):
        self.x = x
        self.y = y
        self.desc = desc
        self.set_desc = set_desc
        self.id_num = id_num
        self.name = name
        self.has = False
        self.false_item = false_item


class Item:
    def __init__(self, desc, name):
        self.desc = desc
        self.name = name


class ItemHandler:
    items = []
    # Store ground items
    ground_items = []
    item_json_path = "jsons/ground_items.json"

    def __init__(self):
        self.reset()

    def read_items(self):
        data = utils.read_json(self.item_json_path)

        for i in data:
            it = GroundItem(i["x"], i["y"], i["desc"], i["set_desc"], i["id"], i["name"], i["false_item"])
            self.ground_items.append(it)

    def pick_up(self, x, y):
        # Check item in list
        for i in range(len(self.ground_items)):
            ground_item = self.ground_items[i]
            print(ground_item.name)
            # Check if the item is at the right coordinates
            if x != ground_item.x or y != ground_item.y:
                continue
            # Check if it's a false item
            if ground_item.false_item:
                utils.display_print(ground_item.desc)
                return False, ""
            # displaying getting description
            utils.display_print(ground_item.desc)
            # Pick up item
            self.items.append(Item(ground_item.desc, ground_item.name))
            # Remove item
            self.ground_items.remove(ground_item)
            return True, ground_item.set_desc
        # No items match this tile display message
        utils.display_print("There's nothing important for me to pickup")
        return False, ""

    def display_owned_items(self):
        length = len(self.items)
        if length == 0:
            utils.display_print("none")
            return False

        for i in range(length):
            item = self.items[i]
            utils.display_print(item.name)
            utils.display_print(" - " + item.desc)
        return True

    def remove_item(self, item_name):
        length = len(self.items)
        for i in range(length):
            item = self.items[i]
            name = item.name
            name = name.lower()
            if name == item_name:
                self.items.pop(i)
                return

    def get_items(self):
        return self.items

    def add_item(self, desc, name):
        self.items.append(Item(desc, name))

    def reset(self):
        self.ground_items = []
        self.items = []
        self.read_items()


    def has_items(self):
        if len(self.items) != 0:
            return True
        return False
