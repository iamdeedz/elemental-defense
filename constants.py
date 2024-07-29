from pygame.transform import scale as img_scale
from pygame.image import load as img_load
from pygame.mouse import get_pos as get_mouse_pos
from screeninfo import get_monitors
from urllib.request import urlopen
import io

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
imgs_to_load = ["red_ball", "blue_ball", "yellow_ball", "dart", "ice", "inferno", "hellfire"]
for img in imgs_to_load:
    imgUrl = f"https://iamdeedz.github.io/elemental-defense/imgs/{img}.png"
    imgStr = urlopen(imgUrl).read()
    imgFile = io.BytesIO(imgStr)
    imgs[img] = img_scale(img_load(imgFile), (calc_new_pos((75, 75))))

bgUrl = "https://iamdeedz.github.io/elemental-defense/imgs/test_bg.png"
bgStr = urlopen(bgUrl).read()
bgFile = io.BytesIO(bgStr)
bg = img_scale(img_load(bgFile), (screen_width, screen_height))

all_towers = {}
tower_costs = {"Dart": 100, "Ice": 150, "Inferno Beam": 150}

elements = ["Grass", "Air", "Fire", "Water", "Rock", "Testing"]

towers_by_element = {
    "Grass": [],
    "Air": [],
    "Water": [],
    "Rock": [],
    "Fire": ["Inferno Beam"],
    "Testing": ["Dart", "Ice"]
}

buffs = {"test": "Test Buff", "ice": "Ice Buff"}


def update_towers():
    global all_towers
    # This is a workaround to avoid circular imports
    from gameplay.towers.towers import Dart, Ice, Inferno
    all_towers["Dart"] = Dart
    all_towers["Ice"] = Ice
    all_towers["Inferno Beam"] = Inferno
