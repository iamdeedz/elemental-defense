from gameplay.enemies.base_enemy import Enemy # NOQA
from constants import imgs, screen_width


class RedBall(Enemy):
    def __init__(self, spawn_delay=0):
        speed = 2 / 1920 * screen_width
        super().__init__(5, speed, imgs["red_ball"], spawn_delay)
        self.name = "Red Ball"


class BlueBall(Enemy):
    def __init__(self, spawn_delay=0):
        speed = 3.5 / 1920 * screen_width
        super().__init__(10, speed, imgs["blue_ball"], spawn_delay)
        self.name = "Blue Ball"


class YellowBall(Enemy):
    def __init__(self, spawn_delay=0):
        speed = 5 / 1920 * screen_width
        super().__init__(20, speed, imgs["yellow_ball"], spawn_delay)
        self.name = "Yellow Ball"
