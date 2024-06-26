from pygame import Vector2, Color
from pygame.draw import circle as draw_circle


class Attack:
    def __init__(self, start_pos, target, dmg, colour):
        self.vector = Vector2(start_pos)
        self.target = target
        self.dmg = dmg
        self.colour = colour

    def update(self, balance):
        # Move
        self.vector.move_towards_ip(self.target.vector, 10)

        # Check if hit
        if self.vector.distance_to(self.target.vector) <= 2:
            self.target.hp -= self.dmg
            return balance + self.dmg, True

        return balance, False

    def draw(self, screen):
        draw_circle(screen, Color(self.colour), (int(self.vector.x), int(self.vector.y)), 5)
