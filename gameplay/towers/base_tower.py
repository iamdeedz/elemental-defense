from pygame import Vector2
from pygame.mouse import get_pos as get_mouse_pos
from time import time, perf_counter
from gameplay.towers.attack import Attack # NOQA
from constants import buffs


class Tower:
    def __init__(self, img, dmg, attack_range, fire_rate, pos, atk_pos, atk_colour):
        self.name = __name__
        self.range = attack_range
        self.dmg = dmg
        self.fire_rate = fire_rate
        self.img = img
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
        for attack in self.attacks:
            attack.draw(screen)

        center = (self.vector.x - (self.img.get_width() // 2), self.vector.y - (self.img.get_height() // 2))
        screen.blit(self.img, center)

    def update(self, enemies, towers, balance):
        # Buffs
        for tower in towers:
            if self == tower or not tower.buff:
                continue
            if buffs[tower.buff] in self.buffs:
                continue

            if self.vector.distance_to(tower.vector) <= tower.range:
                self.buffs.append(buffs[tower.buff])
            else:
                self.buffs.remove(buffs[tower.buff])

        # Attacks
        for attack in self.attacks:
            if attack.target.hp <= 0:
                self.attacks.remove(attack)
                continue

            balance, hit = attack.update(balance)
            if hit:
                self.attacks.remove(attack)

        # Attack enemies
        for enemy in enemies:
            if self.vector.distance_to(enemy.vector) <= self.range:
                if self.last_shot is None or perf_counter() - self.last_shot >= self.fire_rate:
                    self.attacks.append(Attack(self.attack_pos, enemy, self.dmg, self.attack_colour))
                    self.last_shot = perf_counter()

        return balance

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
