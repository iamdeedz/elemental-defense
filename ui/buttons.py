from pgaddons import Button
from constants import screen_width, screen_height
from pygame import Color, init as pygame_init
from pygame.mouse import get_pos as get_mouse_pos
pygame_init()


def upgrade_dmg(tower):
    tower.dmg += 1


def upgrade_range(tower):
    tower.range += 10


def upgrade_fire_rate(tower):
    tower.fire_rate -= 0.1


upgrade_dmg_button = Button(((screen_width - 300) // 2, screen_height - 150), (100, 100), Color("grey 75"), "DMG +1", Color("black"))
upgrade_range_button = Button(((screen_width - 300) // 2 + 100, screen_height - 150), (100, 100), Color("grey 75"), ["Range", "+10"], Color("black"))
upgrade_fire_rate_button = Button(((screen_width - 300) // 2 + 200, screen_height - 150), (100, 100), Color("grey 75"), ["Shot", "Cooldown", "-0.1s"], Color("black"))
upgrade_dmg_button.on_click = lambda tower: upgrade_dmg(tower)
upgrade_range_button.on_click = lambda tower: upgrade_range(tower)
upgrade_fire_rate_button.on_click = lambda tower: upgrade_fire_rate(tower)

buttons = [upgrade_dmg_button, upgrade_range_button, upgrade_fire_rate_button]


def is_clicked(element):
    mouse_pos = get_mouse_pos()
    return element.x <= mouse_pos[0] <= element.x + element.width and element.y <= mouse_pos[1] <= element.y + element.height


def update_buttons(towers):
    for button in buttons:
        if is_clicked(button):
            for tower in towers:
                button.on_click(tower)


def draw_buttons(screen):
    for button in buttons:
        button.draw(screen)
