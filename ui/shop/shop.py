from pgaddons import Button
from constants import elements, tower_costs, all_towers, is_clicked
from .shop_window import ShopWindow # NOQA
from pygame.mouse import get_pos as get_mouse_pos
from pygame import Color


class Shop:
    def __init__(self):
        self.windows = [ShopWindow(element) for element in elements]
        self.windows.insert(0, ShopWindow("closed"))
        self.current_window = self.windows[0]
        self.toggle_button = Button((0, 0), (100, 50), Color("grey 50"), "Shop", Color("white"))
        self.tower_being_placed = None

    def draw(self, screen):
        self.toggle_button.draw(screen)
        self.current_window.draw(screen)

    def update(self, towers, balance):
        if self.tower_being_placed:
            balance = self.place_tower(towers, balance, self.tower_being_placed)

        if is_clicked(self.toggle_button):
            self.toggle_button.on_click()

        if self.current_window != "closed":
            for button in self.current_window.buttons:
                if is_clicked(button):
                    if button.on_click(button.text, balance):
                        self.tower_being_placed = button.text.split(" ")[0].lower()

    def can_buy_tower(self, text, balance):
        tower = text.split(" ")[0].lower()
        if tower_costs[tower] <= balance:
            return True

    def place_tower(self, towers, balance, tower_type):
        mouse_pos = get_mouse_pos()
        towers.append(all_towers[tower_type](mouse_pos))
        balance -= tower_costs[tower_type]
        return balance, towers
