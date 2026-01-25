from debug.logs import set_error_code, reset_error_code
set_error_code("2100")

from constants import tower_costs


def toggle_shop(shop):
    if shop.current_window == "closed":
        shop.current_window = shop.windows[1]
    else:
        shop.current_window = shop.windows[0]


def tower_button_on_click(button, balance):
    tower = button.text.split(" (")[0]
    if tower_costs[tower] <= balance:
        return True, tower


def back_button_on_click(shop):
    shop.current_window = shop.windows[1]


reset_error_code()
