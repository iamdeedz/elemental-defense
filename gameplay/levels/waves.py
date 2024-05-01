from gameplay.enemies.enemies import RedBall, BlueBall, YellowBall # NOQA
from gameplay.spawn_handler import SpawnHandler # NOQA


class Wave:
    def __init__(self, number, enemies):
        self.number = number
        self.enemies = enemies
        self.alive_enemies = []
        self.spawn_handler = SpawnHandler(enemies)

    def update(self):
        if len(self.enemies) == 0 and len(self.alive_enemies) == 0:
            return True
        self.spawn_handler.update()
        self.alive_enemies += self.spawn_handler.enemies_to_spawn
        for enemy in self.enemies:
            if enemy in self.alive_enemies:
                self.enemies.remove(enemy)


waves = [
    Wave(1, [RedBall()]),
    Wave(2, [RedBall(), RedBall()]),
    Wave(3, [RedBall(), RedBall(), RedBall()]),
    Wave(4, [RedBall(), RedBall(), RedBall(), RedBall()]),
    Wave(5, [BlueBall(), BlueBall(), BlueBall(), RedBall(), RedBall()]),
    Wave(6, [BlueBall(), BlueBall(), BlueBall(), RedBall(), RedBall(), RedBall()]),
    Wave(7, [BlueBall(), BlueBall(), BlueBall(), BlueBall(), RedBall(), RedBall(), RedBall()]),
    Wave(8, [YellowBall(), YellowBall(), BlueBall(), BlueBall(), RedBall(), RedBall(), RedBall(), RedBall()]),
    Wave(9, [YellowBall(), YellowBall(), YellowBall(), BlueBall(), BlueBall(), BlueBall(), RedBall(), RedBall(), RedBall()]),
    Wave(10, [YellowBall(), YellowBall(), YellowBall(), YellowBall(), BlueBall(), BlueBall(), BlueBall(), RedBall(), RedBall(), RedBall()]),
]
