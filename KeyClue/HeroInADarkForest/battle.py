from HeroInADarkForest import utils
import random
import math

class BattleSystem:
    battle_json_path = "./jsons/battle_items.json"
    enemy_json_path = "./jsons/enemy.json"

    def __init__(self):
        self.restart()

    def restart(self):
        self.defense_message = []
        self.defense_items = []
        self.attack_items = []
        self.current_items = []
        self.def_stat = 0
        self.enemies = []
        self.read_battle_items()
        self.read_enemy_json()
        self.in_battle = False
        self.dead = False



    def read_battle_items(self):
        data = utils.read_json(self.battle_json_path)
        for d in data:
            if d["atk"] != 0:
                self.attack_items.append(d)
            else:
                self.defense_items.append(d)

    def read_enemy_json(self):
        self.enemies = utils.read_json(self.enemy_json_path)

    def load_def_items(self, items):
        self.def_stat = 21
        return
        self.def_stat = 0
        self.defense_message = []
        print("hello")
        print(items)
        print("stop")
        for i in items:
            i_name = i.name.lower()
            for d in self.defense_items:
                print(i_name, " -- ", d["name"])
                if d["name"] == i_name:
                    self.def_stat += d["def"]
                    self.defense_message = self.defense_message + d["message"]

    def load_atk_items(self, items):
        self.current_items = []
        # Always add in the fists
        self.current_items.append(self.attack_items[0])

        for i in items:
            for a in self.attack_items:
                if a["name"].lower() == i.name.lower():
                    self.current_items.append(a)

    def load_enemy(self, enemy_id):
        for e in self.enemies:
            if e["enemy_id"] == enemy_id:
                return e
        print("Error has occurred! Could not find enemy of this id", enemy_id)
        exit(1)

    def enemy_attack(self, order, max_order, enemy, hero):
        damage = enemy["attack_pattern"][order]
        # Defence calculation
        print("def ", self.def_stat)
        if self.def_stat != 0:
            damage -= self.def_stat
            damage = max(damage, 0)
            # ran = random.randrange(0, len(self.defense_message))
            # utils.display_print(self.defense_message[ran])

        hero.take_damage(damage)
        utils.display_print(enemy["messages"][order])
        order += 1
        if order >= max_order:
            order = 0
        return order

    def start_battle(self, items, hero, enemy_id):
        self.load_def_items(items)
        self.load_atk_items(items)
        self.enemy = self.load_enemy(enemy_id)

        self.hero = hero
        self.e_health = self.enemy["health"]
        self.attack_order = 0
        self.max_attack_order = len(self.enemy["attack_pattern"])
        self.in_battle = True
        self.display_header()

    def display_header(self):
        display_string = "Health: " + str(self.hero.health) + " " + str(self.enemy["name"]) + " : " + str(self.e_health)
        utils.display_print(display_string)
        utils.display_print("What would you like to attack with?")
        if len(self.current_items) == 0:
            print("Something went wrong there are no items to fight with!")
            exit(1)
        for item in self.current_items:
            utils.display_print(" - " + item["name"])

    def step_battle(self, option):
        name = option
        item_found = False
        for item in self.current_items:
            if item["name"] == name:
                rng = random.randrange(0, len(item["message"]))
                atk, messages = item["atk"], item["message"][rng]
                item_found = True

        if not item_found:
            utils.display_print(name + " is not a valid attack")
            return



        utils.display_print(messages)
        self.e_health -= atk
        if self.e_health <= 0:
            utils.display_print("You have slain " + self.enemy["name"] + "!")
            if self.enemy["name"] == "dragon":
                utils.display_print("You hear tales of how valuable dragon scale and hide are... perhaps you should "
                                    "take some")
            self.dead = False
            self.in_battle = False
            return

        self.attack_order = self.enemy_attack(self.attack_order, self.max_attack_order, self.enemy, self.hero)
        if self.hero.health <= 0:
            utils.display_print("You have died!")
            self.dead = True
            self.in_battle = False
            return

        self.display_header()
