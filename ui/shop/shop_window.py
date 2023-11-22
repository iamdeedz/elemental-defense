from pgaddons import Button
from pygame import Color
from constants import tower_types


class ShopWindow:
    def __init__(self, name):
        self.name = name
        if name != "closed":
            self.buttons = [Button((0, 75 * i), (250, 50), Color("grey 50"), f"{self.name} {tower_type.capitalize()} (100)", Color("white")) for i, tower_type in enumerate(tower_types)]

    def draw(self, screen):
        [button.draw(screen) for button in self.buttons] if self.name != "closed" else None

    def __eq__(self, other):
        if isinstance(other, ShopWindow):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"ShopWindow({self.name})"
