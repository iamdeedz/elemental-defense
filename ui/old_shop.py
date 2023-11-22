from pgaddons import Button
from constants import all_towers, tower, tower_costs, is_clicked
from pygame import Color, init as pygame_init
from pygame.mouse import get_pos as get_mouse_pos


def can_buy_tower(text, balance):
    tower = text.split(" ")[0].lower()
    if tower_costs[tower] <= balance:
        return True


def place_tower(towers, balance, tower_type):
    mouse_pos = get_mouse_pos()
    towers.append(all_towers[tower_type](mouse_pos))
    balance -= tower_costs[tower_type]
    return balance


def update_shop(towers, balance):
    for button in buttons:
        if is_clicked(button):
            if button.on_click(button.text, balance):
                return button.text.split(" ")[0].lower()


def draw_shop(screen, balance):
    for button in buttons:
        button.draw(screen)


pygame_init()
buttons = []
for i, tower_type in enumerate(tower):
    tower_cost = tower_costs[tower_type]
    button = Button((25, 25 + (i * 90)), (100, 50), Color("grey 50"), f"{tower_type.capitalize()} ({tower_cost})",
                    (0, 0, 0))
    button.on_click = can_buy_tower
    buttons.append(button)
