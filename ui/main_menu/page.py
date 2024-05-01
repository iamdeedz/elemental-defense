from .page_buttons import buttons_by_page # NOQA
from .button_on_clicks import button_on_clicks # NOQA


class Page:
    def __init__(self, name, parent="start"):
        self.name = name
        self.parent = parent
        self.buttons = buttons_by_page[name]

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def __eq__(self, other):
        if isinstance(other, Page):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Page({self.name})"
