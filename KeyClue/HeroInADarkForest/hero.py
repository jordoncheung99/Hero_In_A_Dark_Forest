class Hero:
    health = 500

    def __init__(self):
        self.reset()

    def take_damage(self, damage):
        self.health -= damage

    def reset(self):
        self.health = 500
        self.x = 0
        self.y = 18
