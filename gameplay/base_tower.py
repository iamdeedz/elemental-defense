from pygame import Vector2
from time import perf_counter
from .attack import Attack # NOQA


class Tower:
    def __init__(self, img, dmg, attack_range, fire_rate, pos):
        self.range = attack_range
        self.dmg = dmg
        self.fire_rate = fire_rate
        self.img = img
        self.vector = Vector2(pos)
        self.last_shot = None
        self.attacks = []

    def draw(self, screen):
        for attack in self.attacks:
            attack.draw(screen)

        center = (self.vector.x - (self.img.get_width() // 2), self.vector.y - (self.img.get_height() // 2))
        screen.blit(self.img, center)

    def update(self, enemies):
        for attack in self.attacks:
            if attack.target.hp <= 0:
                self.attacks.remove(attack)
                continue

            hit = attack.update()
            if hit:
                self.attacks.remove(attack)

        for enemy in enemies:
            if self.vector.distance_to(enemy.vector) <= self.range:
                if self.last_shot is None or perf_counter() - self.last_shot >= self.fire_rate:
                    self.attacks.append(Attack(self.vector, enemy, self.dmg))
                    self.last_shot = perf_counter()
