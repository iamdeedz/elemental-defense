from pgaddons import Button
from constants import screen_width, screen_height, is_clicked
from pygame import Color, init as pygame_init
from pygame.mouse import get_pos as get_mouse_pos
pygame_init()

upgrade_dmg_button = Button(((screen_width - 300) // 2, screen_height - 150), (100, 100), Color("grey 75"), ["DMG +1", "10"], Color("black"))
upgrade_range_button = Button(((screen_width - 300) // 2 + 100, screen_height - 150), (100, 100), Color("grey 75"), ["Range", "+10", "10"], Color("black"))
upgrade_fire_rate_button = Button(((screen_width - 300) // 2 + 200, screen_height - 150), (100, 100), Color("grey 75"), ["Shot", "Cooldown", "-0.1s", "20"], Color("black"))
upgrade_dmg_button.on_click = lambda tower, balance: upgrade_dmg(tower, balance)
upgrade_range_button.on_click = lambda tower, balance: upgrade_range(tower, balance)
upgrade_fire_rate_button.on_click = lambda tower, balance: upgrade_fire_rate(tower, balance)

buttons = [upgrade_dmg_button, upgrade_range_button, upgrade_fire_rate_button]


def update_buttons(towers, balance):
    for button in buttons:
        if is_clicked(button):
            for tower in towers:
                balance = button.on_click(tower, balance)

    return balance


def draw_buttons(screen):
    for button in buttons:
        button.draw(screen)
