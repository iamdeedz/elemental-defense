from .base_tower import Tower # NOQA
from constants import imgs


class Dart(Tower):
    def __init__(self, pos):
        super().__init__(imgs["dart"], 1, 250, 0.75, pos, (0, 0), "grey 50")
        self.name = "Dart Tower"


class Ice(Tower):
    def __init__(self, pos):
        super().__init__(imgs["ice"], 2, 300, 0.5, pos, (0, 0), "light blue")
        self.name = "Ice Tower"


class Fire(Tower):
    def __init__(self, pos):
        super().__init__(imgs["fire"], 2, 300, 0.5, pos, (imgs["fire"].get_width()//2, (imgs["fire"].get_height()//2)-26), "dark red")
        self.name = "Fire Tower"
