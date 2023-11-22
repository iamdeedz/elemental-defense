from pgaddons import Button
from constants import elements, tower_costs, all_towers, is_clicked
from .shop_window import ShopWindow # NOQA
from .button_on_clicks import toggle_shop # NOQA
from pygame.mouse import get_pos as get_mouse_pos
from pygame import Color


class Shop:
    def __init__(self):
        self.windows = [ShopWindow(name) for name in ["closed", "selection"] + elements]
        self.window_keys = {window.name: i for i, window in enumerate(self.windows)}
        self.current_window = self.windows[0]
        self.toggle_button = Button((0, 0), (200, 50), Color("grey 50"), "Toggle Shop", Color("white"))
        self.toggle_button.on_click = toggle_shop
        self.tower_being_placed = None

    def draw(self, screen):
        self.toggle_button.draw(screen)
        self.current_window.draw(screen)

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
                        self.tower_being_placed = button.text.split(" (")[0].lower()

        if self.tower_being_placed and should_tower_place:
            balance = self.place_tower(towers, balance, self.tower_being_placed)
            self.tower_being_placed = None

        return balance

    def place_tower(self, towers, balance, tower_type):
        mouse_pos = get_mouse_pos()
        towers.append(all_towers[tower_type](mouse_pos))
        balance -= tower_costs[tower_type]
        return balance
