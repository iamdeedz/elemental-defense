from gameplay.enemies.base_enemy import Enemy # NOQA
from constants import imgs


class RedBall(Enemy):
    def __init__(self, spawn_delay=0):
        super().__init__(5, 2, imgs["red_ball"], spawn_delay)
        self.name = "Red Ball"


class BlueBall(Enemy):
    def __init__(self, spawn_delay=0):
        super().__init__(10, 3.5, imgs["blue_ball"], spawn_delay)
        self.name = "Blue Ball"


class YellowBall(Enemy):
    def __init__(self, spawn_delay=0):
        super().__init__(20, 5, imgs["yellow_ball"], spawn_delay)
        self.name = "Yellow Ball"
