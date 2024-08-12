from pygame.transform import scale as img_scale
from pygame.image import load as img_load
from pygame.mouse import get_pos as get_mouse_pos
from screeninfo import get_monitors
from urllib.request import urlopen
from os import makedirs
from os.path import exists
import io

version = 0.2

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


# Images
imgs = {}
imgs_to_load = ["red_ball", "blue_ball", "yellow_ball", "dart", "ice", "inferno", "hellfire"]

imgs_exist = exists("./imgs/")
if not imgs_exist:
    makedirs("./imgs/")

if imgs_exist:
    # Images are stored locally
    for img in imgs_to_load:
        imgs[img] = img_scale(img_load(f"./imgs/{img}.png"), (calc_new_pos((75, 75))))

    # Background
    bg = img_scale(img_load("./imgs/test_bg.png"), (screen_width, screen_height))

else:
    # Images are not stored locally, get them from GitHub Page
    for img in imgs_to_load:
        imgUrl = f"https://iamdeedz.github.io/elemental-defense/imgs/{img}.png"
        imgStr = urlopen(imgUrl).read()
        imgFile = io.BytesIO(imgStr)
        imgs[img] = img_scale(img_load(imgFile), (calc_new_pos((75, 75))))

        with open(f"./imgs/{img}.png", "wb") as localImgFile:
            localImgFile.write(imgStr)

    # Background
    bgUrl = "https://iamdeedz.github.io/elemental-defense/imgs/test_bg.png"
    bgStr = urlopen(bgUrl).read()
    bgFile = io.BytesIO(bgStr)
    bg = img_scale(img_load(bgFile), (screen_width, screen_height))

    with open("./imgs/test_bg.png", "wb") as localBgFile:
        localBgFile.write(bgStr)


# Towers
all_towers = {}
tower_costs = {"Dart": 100, "Ice": 150, "Inferno Beam": 150, "Hellfire Launcher": 200}

elements = ["Grass", "Air", "Fire", "Water", "Rock", "Testing"]

towers_by_element = {
    "Grass": [],
    "Air": [],
    "Water": [],
    "Rock": [],
    "Fire": ["Inferno Beam", "Hellfire Launcher"],
    "Testing": ["Dart", "Ice"]
}

buffs = {"test": {"name": "Test Buff", "buff": "range", "percent": 25},
         "ice": {"name": "Ice Buff", "buff": "dmg", "percent": 25}}


def update_towers():
    global all_towers
    # This is a workaround to avoid circular imports
    from gameplay.towers.towers import Dart, Ice, Inferno, Hellfire
    all_towers["Dart"] = Dart
    all_towers["Ice"] = Ice
    all_towers["Inferno Beam"] = Inferno
    all_towers["Hellfire Launcher"] = Hellfire


class Pos:
    def __init__(self, x, y):
        self.x = (x / 1920) * screen_width
        self.y = (y / 1080) * screen_height
