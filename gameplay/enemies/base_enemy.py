from pygame import Vector2
from gameplay.levels.path import waypoints


class Enemy:
    def __init__(self, hp, speed, img, spawn_delay=0):
        self.name = __name__
        self.hp = hp
        self.speed = speed
        self.img = img
        self.vector = Vector2(waypoints[0])
        self.prev_waypoint = waypoints[0]
        self.next_waypoint = waypoints[waypoints.index(self.vector.xy) + 1]
        self.spawn_delay = spawn_delay

    def move(self):
        if self.hp <= 0:
            return True, False

        if self.vector.distance_to(self.next_waypoint) < 2:
            self.prev_waypoint = self.next_waypoint

        try:
            self.next_waypoint = waypoints[waypoints.index(self.prev_waypoint) + 1]
        except IndexError:
            return False, True

        self.vector.move_towards_ip(self.next_waypoint, self.speed)
        return False, False

    def draw(self, screen):
        center = (self.vector.x - (self.img.get_width() // 2), self.vector.y - (self.img.get_height() // 2))
        screen.blit(self.img, center)
