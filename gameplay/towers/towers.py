from debug.logs import set_error_code, reset_error_code
set_error_code("0800")

from gameplay.towers.base_tower import Tower # NOQA
from constants import imgs, calc_scaled_num, calc_scaled_tuple


class Dart(Tower):
    def __init__(self, pos, tower_id=None, owner_id=None):
        super().__init__(imgs["dart"], 2, calc_scaled_num(250), 0.5, pos, (0, 0), "grey 50", tower_id, owner_id)
        self.name = "Dart"
        self.buff = "test"


class Ice(Tower):
    def __init__(self, pos, tower_id=None, owner_id=None):
        super().__init__(imgs["ice"], 2, calc_scaled_num(300), 0.5, pos, (0, 0), "light blue", tower_id, owner_id)
        self.name = "Ice"
        self.buff = "ice"


class Inferno(Tower):
    def __init__(self, pos, tower_id=None, owner_id=None):
        super().__init__(imgs["inferno"], 3, calc_scaled_num(400), 0.5, pos, calc_scaled_tuple(
            (imgs["inferno"].get_width() // 2, 12)), "dark red", tower_id, owner_id)
        self.name = "Inferno Beam"


class Hellfire(Tower):
    def __init__(self, pos, tower_id=None, owner_id=None):
        super().__init__(imgs["hellfire"], 4, calc_scaled_num(300), 0.75, pos, calc_scaled_tuple((imgs["hellfire"].get_width() // 2, 10)), "dark red", tower_id, owner_id)
        self.name = "Hellfire Launcher"


class Pyro(Tower):
    def __init__(self, pos, tower_id=None, owner_id=None):
        super().__init__(imgs["pyro"], 2, calc_scaled_num(500), 1, pos, calc_scaled_tuple((imgs["pyro"].get_width() // 2, 6)), "orange", tower_id, owner_id)
        self.name = "Pyro Nexus"
        self.buff = "pyro"

reset_error_code()
