from time import perf_counter


class SpawnHandler:
    def __init__(self, enemies):
        self.enemies = enemies
        self.enemies_to_spawn = []
        self.enemies_spawned = []
        self.start_time = perf_counter()

    def update(self):
        self.enemies_to_spawn = []
        current_time = perf_counter()
        elapsed_time = current_time - self.start_time
        for enemy in self.enemies:
            if enemy in self.enemies_spawned:
                continue

            if elapsed_time >= enemy.spawn_delay:
                self.enemies_to_spawn.append(enemy)
                self.enemies_spawned.append(enemy)
