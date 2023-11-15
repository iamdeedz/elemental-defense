from pygame.transform import scale as img_scale
from pygame.image import load as img_load
from pygame.mouse import get_pos as get_mouse_pos
from screeninfo import get_monitors

screen_width = 720
screen_height = 405

for monitor in get_monitors():
    if monitor.is_primary:
        screen_width = monitor.width
        screen_height = monitor.height
        break


def is_clicked(element):
    mouse_pos = get_mouse_pos()
    return element.x <= mouse_pos[0] <= element.x + element.width and element.y <= mouse_pos[1] <= element.y + element.height


def calc_new_pos(pos: tuple | list | int | float, direction=""):
    if type(pos) in (int, float):
        if direction == "horizontal":
            return (pos / 1920) * screen_width

        elif direction == "vertical":
            return (pos / 1080) * screen_height

        else:
            raise ValueError("Invalid direction")

    else:
        return (pos[0] / 1920) * screen_width, (pos[1] / 1080) * screen_height


fps = 60

imgs = {}
imgs_to_load = ["red_ball", "blue_ball", "yellow_ball", "dart", "ice", "fire"]
for img in imgs_to_load:
    imgs[img] = img_scale(img_load(f"imgs/{img}.png"), (calc_new_pos((50, 50))))

bg = img_scale(img_load("imgs/test_bg.png"), (screen_width, screen_height))

all_towers = {}
tower = ["dart", "ice", "fire"]
tower_costs = {"dart": 100, "ice": 150, "fire": 150}

elements = ["Grass", "Air", "Fire", "Water", "Rock"]
tower_types = ["Guardian", "Tower", "Cannon", "Catapult", "Castle"]

all_tower_combos = []
for element in elements:
    for tower_type in tower_types:
        all_tower_combos.append(f"{element} {tower_type}")


def update_towers():
    global all_towers
    # This is a workaround to avoid circular imports
    from gameplay.towers import Dart, Ice, Fire
    all_towers["dart"] = Dart
    all_towers["ice"] = Ice
    all_towers["fire"] = Fire
