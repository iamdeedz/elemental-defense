import pgaddons


class Page:
    def __init__(self, parent):
        self.parent = parent
        self.children = []

    def draw(self, screen):
        pass
