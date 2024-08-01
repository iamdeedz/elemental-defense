from constants import calc_new_pos, screen_width, screen_height, is_clicked, tower_costs
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

# Upgrade buttons
buttons = []
for i, upgrade in enumerate(upgrades):
    button = Button((margin[0] * 2, upgrade_rect.height // 3 + (i * 100)), (upgrade_rect.width - (margin[0] * 4), 75),
                    Color("grey 75"), [f"Upgrade {upgrades_long[upgrade]}"], Color("grey 25"))
    exec(f"button.on_click = lambda tower, balance: upgrade_{upgrade}(tower, balance)")
    buttons.append(button)

# Sell button
button = Button((margin[0] * 2, upgrade_rect.height // 3 + (len(upgrades) * 100)), (upgrade_rect.width - (margin[0] * 4), 75),
                      Color("grey 75"), ["Sell"], Color("grey 25"))
button.on_click = lambda tower, balance, towers: sell_tower(tower, balance, towers)
buttons.append(button)


def upgrade_dmg(tower, balance):
    cost = 15 * tower.dmg
    if balance >= cost:
        tower.dmg += 1
        return balance - cost
    return balance


def upgrade_range(tower, balance):
    cost = (tower.range / 100) * 15
    if balance >= cost:
        tower.range += 20
        return balance - cost
    return balance


def upgrade_fire_rate(tower, balance):
    cost = round(20 / tower.fire_rate)
    if balance >= cost:
        tower.fire_rate -= 0.025
        return balance - cost
    return balance


def sell_tower(tower, balance, towers):
    tower.sell(towers)
    return balance + (tower_costs[tower.name] / 2)


def draw_upgrades(tower, screen):
    draw_rect(screen, Color("grey 50"), upgrade_rect, border_radius=round(upgrade_rect.width / 25.6))
    screen.blit(img_scale(tower.img, (100, 100)), (margin[0] * 2, margin[1] * 2))
    text = font.render(tower.name, True, Color("black"))
    screen.blit(text, (margin[0] * 5, margin[1] * 2))

    # Buffs
    buff_font = Font(None, 30)
    for buff_index, buff in enumerate(tower.buffs):
        buff_text = buff_font.render(f"{buff['name']}", True, Color("black"))
        screen.blit(buff_text, (margin[0] * 4, margin[1] * 1.5 + (buff_index * 100)))

    for button in buttons:
        button.draw(screen)


def update_upgrades(tower, balance, towers):
    global are_upgrades_visible

    if not are_upgrades_visible:
        return balance, False, False

    if not is_clicked(upgrade_rect):
        are_upgrades_visible = False
        return balance, False, False

    for button in buttons:
        if is_clicked(button):
            balance = button.on_click(tower, balance) if button.text[0] != "Sell" else button.on_click(tower, balance, towers)
            if button.text[0] == "Sell":
                are_upgrades_visible = False
                return balance, False, True

    return balance, True, False


def toggle_upgrades():
    global are_upgrades_visible
    are_upgrades_visible = not are_upgrades_visible
