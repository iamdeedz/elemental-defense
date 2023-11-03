from pgaddons import Button
from constants import screen_width, screen_height
from pygame import Color, init as pygame_init
from pygame.mouse import get_pos as get_mouse_pos
pygame_init()


def upgrade_dmg(tower, balance):
    if balance >= 10:
        tower.dmg += 1
        return balance - 10
    return balance


def upgrade_range(tower, balance):
    if balance >= 10:
        tower.range += 10
        return balance - 10
    return balance


def upgrade_fire_rate(tower, balance):
    if balance >= 20:
        tower.fire_rate -= 0.1
        return balance - 20
    return balance


upgrade_dmg_button = Button(((screen_width - 300) // 2, screen_height - 150), (100, 100), Color("grey 75"), ["DMG +1", "10"], Color("black"))
upgrade_range_button = Button(((screen_width - 300) // 2 + 100, screen_height - 150), (100, 100), Color("grey 75"), ["Range", "+10", "10"], Color("black"))
upgrade_fire_rate_button = Button(((screen_width - 300) // 2 + 200, screen_height - 150), (100, 100), Color("grey 75"), ["Shot", "Cooldown", "-0.1s", "20"], Color("black"))
upgrade_dmg_button.on_click = lambda tower, balance: upgrade_dmg(tower, balance)
upgrade_range_button.on_click = lambda tower, balance: upgrade_range(tower, balance)
upgrade_fire_rate_button.on_click = lambda tower, balance: upgrade_fire_rate(tower, balance)

buttons = [upgrade_dmg_button, upgrade_range_button, upgrade_fire_rate_button]


def is_clicked(element):
    mouse_pos = get_mouse_pos()
    return element.x <= mouse_pos[0] <= element.x + element.width and element.y <= mouse_pos[1] <= element.y + element.height


def update_buttons(towers, balance):
    for button in buttons:
        if is_clicked(button):
            for tower in towers:
                balance = button.on_click(tower, balance)

    return balance


def draw_buttons(screen):
    for button in buttons:
        button.draw(screen)
