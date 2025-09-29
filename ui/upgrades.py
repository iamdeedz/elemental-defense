from math import floor
from constants import screen_width, screen_height, is_clicked, tower_costs, calc_scaled_tuple, calc_scaled_num, font_path
from pygame import Rect, Color, Surface, SRCALPHA
from pygame.draw import rect as draw_rect, circle as draw_circle
from pygame.font import Font
from pygame.transform import scale as img_scale
from pgaddons import Button

font = Font(font_path, floor(calc_scaled_num(75)))

margin = (50, 50)
upgrade_rect = Rect(calc_scaled_tuple(margin), (screen_width // 3, screen_height - calc_scaled_num(margin[1] * 2)))

upgrades = ["dmg", "range", "fire_rate"]
upgrades_s_to_l = {"dmg": "Damage", "range": "Range", "fire_rate": "Fire Rate"}
upgrades_l_to_s = {"Damage": "dmg", "Range": "range", "Fire Rate": "fire_rate"}
costs = {"dmg": 65, "range": 50, "fire_rate": 80}

are_upgrades_visible = False

# Upgrade buttons
buttons = []
for i, upgrade in enumerate(upgrades):
    button = Button((calc_scaled_num(margin[0] * 2), upgrade_rect.height // 3 + calc_scaled_num(i * 100, direction="vertical")), (upgrade_rect.width - calc_scaled_num((margin[0] * 4)), calc_scaled_num(75, direction="vertical")),
                    Color("grey 75"), [f"Upgrade {upgrades_s_to_l[upgrade]} ({costs[upgrade]})"], Color("grey 25"), font=Font(font_path, floor(calc_scaled_num(30))))
    exec(f"button.on_click = lambda tower, balance: upgrade_{upgrade}(tower, balance)")
    buttons.append(button)

# Sell button
button = Button((calc_scaled_num(margin[0] * 2), upgrade_rect.height // 3 + calc_scaled_num(len(upgrades) * 100, direction="vertical")), (upgrade_rect.width - calc_scaled_num(margin[0] * 4), calc_scaled_num(75, direction="vertical")),
                Color("grey 75"), ["Sell"], Color("grey 25"), font=Font(font_path, floor(calc_scaled_num(30))))
button.on_click = lambda tower, balance, towers: sell_tower(tower, balance, towers)
buttons.append(button)


def upgrade_button_texts():
    for button in buttons:
        if button.text == "Sell":
            continue

        prev_button_text = button.text.copy()
        button.text = prev_button_text[0].split("(") + f"({costs[upgrades_l_to_s[prev_button_text[0].split(' ')[1]]]}"


def upgrade_dmg(tower, balance):
    if balance >= costs["dmg"]:
        tower.base_dmg += 1
        return_value = balance - costs["dmg"]
        costs["dmg"] += 15
        upgrade_button_texts()
        return return_value

    return balance


def upgrade_range(tower, balance):
    if balance >= costs["range"]:
        tower.base_range += 20
        return_value = balance - costs["range"]
        costs["range"] += 15
        upgrade_button_texts()
        return return_value

    return balance


def upgrade_fire_rate(tower, balance):
    if balance >= costs["fire_rate"]:
        tower.base_fire_rate -= 0.025
        return_value = balance - costs["fire_rate"]
        costs["fire_rate"] += 15
        upgrade_button_texts()
        return return_value

    return balance


def sell_tower(tower, balance, towers):
    tower.sell(towers)
    return balance + (tower_costs[tower.name] / 2)


def draw_upgrades(tower, screen):
    # Draw Tower Range
    surface = Surface((screen_width, screen_height), SRCALPHA)
    draw_circle(surface, (0, 0, 0, 50), tower.vector.xy, tower.range)
    screen.blit(surface, (0, 0))

    # Rect
    draw_rect(screen, Color("grey 50"), upgrade_rect, border_radius=round(upgrade_rect.width / calc_scaled_num(25.6)))
    screen.blit(img_scale(tower.img, calc_scaled_tuple((100, 100))), calc_scaled_tuple((margin[0] * 2, margin[1] * 2)))
    text = font.render(tower.name, True, Color("black"))
    screen.blit(text, calc_scaled_tuple((margin[0] * 5, margin[1] * 2)))

    # Buffs
    buff_font = Font(font_path, floor(calc_scaled_num(30)))
    for buff_index, buff in enumerate(tower.buffs):
        buff_text = buff_font.render(f"{buff['name']}", True, Color("black"))
        screen.blit(buff_text, calc_scaled_tuple((margin[0] * 4, margin[1] * 1.5 + (buff_index * 100))))

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
