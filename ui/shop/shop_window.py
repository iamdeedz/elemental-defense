from pgaddons import Button
from pygame import Color
from constants import tower_types, elements
from .button_on_clicks import tower_button_on_click, back_button_on_click # NOQA


class ShopWindow:
    def __init__(self, name):
        self.name = name

        # Add buttons based on which window it is
        if self.name == "selection":
            self.buttons = [
                Button((0, 75 * (i + 1)), (150, 50), Color("grey 50"), f"{element.capitalize()}", Color("white"))
                for i, element in enumerate(elements)]

        elif self.name != "closed":
            self.buttons = [Button((0, 75 * (i + 1)), (250, 50), Color("grey 50"), f"{self.name} {tower_type.capitalize()} (100)", Color("white"))
                            for i, tower_type in enumerate(tower_types)]

            for button in self.buttons:
                button.on_click = tower_button_on_click

            # Add back button
            self.buttons.append(Button((0, 75 * (len(self.buttons) + 1)), (250, 50), Color("grey 50"), "Back", Color("white")))
            self.buttons[-1].on_click = back_button_on_click

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
