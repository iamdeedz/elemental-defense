from debug.logs import set_error_code, reset_error_code
set_error_code("0900")

from pygame import Vector2, Color
from pygame.draw import circle as draw_circle
from constants import calc_scaled_num


class Attack:
    def __init__(self, start_pos, target, dmg, colour, origin_tower_owner_id):
        self.vector = Vector2(start_pos)
        self.target = target
        self.dmg = dmg
        self.colour = colour
        self.origin_tower_owner_id = origin_tower_owner_id

    def update(self, balance):
        # Move
        self.vector.move_towards_ip(self.target.vector, calc_scaled_num(10))

        # Check if hit
        if self.vector.distance_to(self.target.vector) <= 2 and self.target.hp > 0:
            self.target.hp -= self.dmg
            if self.origin_tower_owner_id:
                return balance, True # tower is owned by someone else
            return balance + self.dmg, True # tower is owned by user so add money

        return balance, False

    def draw(self, screen):
        draw_circle(screen, Color(self.colour), (int(self.vector.x), int(self.vector.y)), calc_scaled_num(4))


reset_error_code()
