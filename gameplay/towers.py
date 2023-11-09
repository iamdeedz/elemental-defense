from .base_tower import Tower # NOQA
from constants import imgs


class Dart(Tower):
    def __init__(self, pos):
        super().__init__(imgs["dart"], 1, 250, 0.75, pos)
        self.name = "Dart Tower"


class Ice(Tower):
    def __init__(self, pos):
        super().__init__(imgs["dart"], 2, 300, 0.5, pos)
        self.name = "Ice Tower"
