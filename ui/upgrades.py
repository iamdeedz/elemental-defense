from constants import calc_new_pos, screen_width, screen_height, is_clicked
from pygame import Rect, Color
from pygame.draw import rect as draw_rect
from pygame.font import Font
from pygame.transform import scale as img_scale
from pgaddons import Button

font = Font(None, 75)

margin = calc_new_pos((50, 50))
upgrade_rect = Rect(margin, (screen_width // 3, screen_height - (margin[1] * 2)))

upgrades = ["dmg", "range", "fire_rate"]
upgrades_long = {"dmg": "Damage", "range": "Range", "fire_rate": "Fire Rate"}

are_upgrades_visible = False
buttons = []
for i, upgrade in enumerate(upgrades):
    button = Button((margin[0] * 2, upgrade_rect.height // 3 + (i * 100)), (upgrade_rect.width - (margin[0] * 4), 75),
                    Color("grey 75"), f"Upgrade {upgrades_long[upgrade].capitalize()}", Color("grey 25"))
    exec(f"button.on_click = lambda tower, balance: upgrade_{upgrade}(tower, balance)")
    buttons.append(button)


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
        tower.fire_rate -= 0.025
        return balance - 20
    return balance


def draw_upgrades(tower, screen):
    draw_rect(screen, Color("grey 50"), upgrade_rect, border_radius=round(upgrade_rect.width / 25.6))
    screen.blit(img_scale(tower.img, (100, 100)), (margin[0] * 2, margin[1] * 2))
    text = font.render(tower.name, True, Color("black"))
    screen.blit(text, (margin[0] * 5, margin[1] * 2))
    for button in buttons:
        button.draw(screen)


def update_upgrades(tower, balance):
    if not are_upgrades_visible:
        return balance, False

    if not is_clicked(upgrade_rect):
        return balance, False

    for button in buttons:
        if is_clicked(button):
            balance = button.on_click(tower, balance)

    return balance, True


def toggle_upgrades():
    global are_upgrades_visible
    are_upgrades_visible = not are_upgrades_visible
