from math import floor

from pgaddons import Button
from constants import elements, tower_costs, all_towers, is_clicked, screen_width, screen_height, calc_scaled_tuple, \
    calc_scaled_num, nunito_path
from .shop_window import ShopWindow # NOQA
from .button_on_clicks import toggle_shop # NOQA
from pygame import Color, Surface, SRCALPHA
from pygame.mouse import get_pos as get_mouse_pos
from pygame.draw import circle


class Shop:
    def __init__(self):
        self.windows = [ShopWindow(name) for name in ["closed", "selection"] + elements]
        self.window_keys = {window.name: i for i, window in enumerate(self.windows)}
        self.current_window = self.windows[0]
        self.toggle_button = Button((0, 0), calc_scaled_tuple((200, 50)), Color("grey 50"), "Toggle Shop", Color("white"), font_size=floor(calc_scaled_num(30)), font=nunito_path)
        self.toggle_button.on_click = toggle_shop
        self.tower_being_placed = None
        self.element_being_placed = None

        self.range_circle = None

    def draw(self, screen):
        self.toggle_button.draw(screen)
        self.current_window.draw(screen)

        if self.range_circle:
            surface = Surface((screen_width, screen_height), SRCALPHA)
            circle(surface, (0, 0, 0, 50), get_mouse_pos(), self.range_circle)
            screen.blit(surface, (0, 0))

    def update(self, towers, balance):
        should_tower_place = True

        # Check if any of tower is clicked (indicating the player wants to upgrade a tower)
        for tower in towers:
            if tower.is_clicked():
                should_tower_place = False
                self.tower_being_placed = None

        if is_clicked(self.toggle_button):
            self.toggle_button.on_click(self)

        # If the shop is open, check if any of the buttons were clicked
        if self.current_window != "closed":
            for button in self.current_window.buttons:

                if is_clicked(button):

                    # If the current window is the selection window, go to the window of the element that was clicked
                    if self.current_window.name == "selection":
                        self.current_window = self.windows[self.window_keys[button.text]]

                    # If the current window is not the selection window, check if the button is the back button
                    elif button.text == "Back":
                        self.current_window = self.windows[1]

                    # Otherwise, place the tower
                    elif button.on_click(button, balance):
                        should_tower_place = False
                        tower = button.text.split(" (")[0]
                        self.tower_being_placed = tower
                        self.range_circle = all_towers[self.tower_being_placed]((0, 0)).range

        if self.tower_being_placed and should_tower_place:
            balance = self.place_tower(towers, balance, self.tower_being_placed)
            self.tower_being_placed = self.range_circle = None

        return balance

    def place_tower(self, towers, balance, tower):
        mouse_pos = get_mouse_pos()
        tower = all_towers[tower](mouse_pos)
        towers.append(tower)
        balance -= tower_costs[tower.name]
        return balance
