from pygame import Vector2
from pygame.mouse import get_pos as get_mouse_pos
from time import time, perf_counter
from gameplay.towers.attack import Attack # NOQA
from constants import buffs


class Tower:
    def __init__(self, img, dmg, attack_range, fire_rate, pos, atk_pos, atk_colour):
        self.name = __name__
        self.base_range = attack_range
        self.base_dmg = dmg
        self.base_fire_rate = fire_rate
        self.img = img
        self.range = self.base_range
        self.dmg = self.base_dmg
        self.fire_rate = self.base_fire_rate
        self.vector = Vector2(pos)
        self.top_left = Vector2(pos[0] - (self.img.get_width() // 2), pos[1] - (self.img.get_height() // 2))

        self.last_shot = None
        self.attacks = []
        self.attack_pos = Vector2(self.top_left + Vector2(atk_pos))
        self.attack_colour = atk_colour

        self.buffs = []
        self.buff = None

        self.id = time() / 1000000000

    def draw(self, screen):
        center = (self.vector.x - (self.img.get_width() // 2), self.vector.y - (self.img.get_height() // 2))
        screen.blit(self.img, center)

        for attack in self.attacks:
            attack.draw(screen)

    def update(self, enemies, towers, balance):
        # Buffs
        for tower in towers:
            if self == tower or not tower.buff:
                continue
            if buffs[tower.buff] in self.buffs:
                continue

            if self.vector.distance_to(tower.vector) <= tower.range:
                self.buffs.append(buffs[tower.buff])
                exec(f"self.{buffs[tower.buff]['buff']} += (self.{buffs[tower.buff]['buff']} / 100) * {buffs[tower.buff]['percent']}")

            elif buffs[tower.buff] in self.buffs:
                self.buffs.remove(buffs[tower.buff])
                exec(f"self.{buffs[tower.buff]['buff']} = self.base_{buffs[tower.buff]['buff']}")

        stats_names = {"range": "base_range", "dmg": "base_dmg", "fire_rate": "base_fire_rate"}
        stats = {"range": self.range, "base_range": self.base_range, "dmg": self.dmg, "base_dmg": self.base_dmg, "fire_rate": self.fire_rate, "base_fire_rate": self.base_fire_rate}

        for stat_name, base_stat_name in stats_names.items():
            stat = stats[stat_name]
            base_stat = stats[base_stat_name]
            has_stat_buff = False
            if stat != base_stat:
                for buff in self.buffs:
                    if buff['buff'] == stat_name:
                        has_stat_buff = True
                        break

            if not has_stat_buff:
                exec(f"self.{stat_name} = self.{base_stat_name}")

        # Attacks
        for attack in self.attacks:
            balance, hit = attack.update(balance)
            if hit:
                self.attacks.remove(attack)
                continue

            attack_changed_target = False
            if attack.target.hp <= 0:
                for enemy in enemies:
                    if self.vector.distance_to(enemy.vector) <= self.range:
                        attack.target = enemy
                        attack_changed_target = True

                if not attack_changed_target:
                    self.attacks.remove(attack)

        # Attack enemies
        for enemy in enemies:
            if self.vector.distance_to(enemy.vector) <= self.range:
                if self.last_shot is None or perf_counter() - self.last_shot >= self.fire_rate:
                    self.attacks.append(Attack(self.attack_pos, enemy, self.dmg, self.attack_colour))
                    self.last_shot = perf_counter()

        return balance

    def sell(self, towers):
        for tower in towers:
            if self == tower or not self.buff:
                continue

            if self.vector.distance_to(tower.vector) <= self.range:
                tower.buffs.remove(buffs[self.buff])

    # The towers need a special is_clicked method because they don't have some necessary variables that the buttons
    # have.
    def is_clicked(self):
        mouse_pos = get_mouse_pos()
        x, y = self.vector.xy
        width, height = self.img.get_size()
        x -= width / 2
        y -= height / 2
        return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id
