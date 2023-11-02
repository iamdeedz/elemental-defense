from time import perf_counter


class SpawnHandler:
    def __init__(self, enemies):
        self.enemies = enemies
        self.enemies_to_spawn = []
        self.index = 0
        self.start_time = perf_counter()

    def update(self):
        self.enemies_to_spawn = []
        current_time = perf_counter()
        elapsed_time = current_time - self.start_time
        for enemy in self.enemies[self.index:]:
            if elapsed_time >= enemy.spawn_delay:
                self.index += 1
                self.enemies_to_spawn.append(enemy)
