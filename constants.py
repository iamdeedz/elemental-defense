from pygame.transform import scale as img_scale
from pygame.image import load as img_load
from pygame.mouse import get_pos as get_mouse_pos
from screeninfo import get_monitors
from urllib.request import urlopen
from os import makedirs
from os.path import exists
from debug.logs import write_to_log
import io

version = "0.3.1 dev"
crash_reporter_active = False

screen_width = 700
screen_height = 420

server_manager_ip = "127.0.0.1"
server_manager_port = 1300

for monitor in get_monitors():
    if monitor.is_primary:
        screen_width = monitor.width
        screen_height = monitor.height
        break

write_to_log("Info", f"Screen Width: {screen_width}, Screen Height: {screen_height}")


def is_clicked(element):
    mouse_pos = get_mouse_pos()
    return element.x <= mouse_pos[0] <= element.x + element.width and element.y <= mouse_pos[1] <= element.y + element.height


def calc_scaled_tuple(tuple):
    return (tuple[0] / 1920) * screen_width, (tuple[1] / 1080) * screen_height


def calc_scaled_num(num, direction="horizontal"):
    match direction:
        case "horizontal":
            return num / 1920 * screen_width
        case "vertical":
            return num / 1080 * screen_height


fps = 60

# -------------------------------------- #

# Images
imgs = {}
imgs_to_load = ["red_ball", "blue_ball", "yellow_ball", "dart", "ice", "inferno", "hellfire", "pyro"]

level_ids = [-999]
backgrounds = {}
small_backgrounds = {}
medium_backgrounds = {}
background_name_to_id = {"test_bg": -999}
background_id_to_name = {-999: "Test Level"}
backgrounds_to_load = ["test_bg"]


img_folder_exists = exists("./imgs/")
if not img_folder_exists:
    # Images are not stored locally, get them from GitHub Page

    makedirs("./imgs/")

    write_to_log("Info", "The imgs folder doesn't exist. Getting images from GitHub Pages.")

    for img in imgs_to_load:
        img_url = f"https://iamdeedz.github.io/elemental-defense/imgs/{img}.png"
        img_str = urlopen(img_url).read()
        img_file = io.BytesIO(img_str)
        imgs[img] = img_scale(img_load(img_file), calc_scaled_tuple((75, 75)))

        with open(f"./imgs/{img}.png", "wb") as local_img_file:
            local_img_file.write(img_str)

    # Background
    for bg in backgrounds_to_load:
        bg_url = f"https://iamdeedz.github.io/elemental-defense/imgs/{bg}.png"
        bg_str = urlopen(bg_url).read()
        bg_file = io.BytesIO(bg_str)
        backgrounds[background_name_to_id[bg]] = img_scale(img_load(bg_file), (screen_width, screen_height))
        small_backgrounds[background_name_to_id[bg]] = img_scale(img_load(bg_file), calc_scaled_tuple((100, 56.25)))
        medium_backgrounds[background_name_to_id[bg]] = img_scale(img_load(bg_file), calc_scaled_tuple((250, 140.625)))

        with open("./imgs/test_bg.png", "wb") as local_bg_file:
            local_bg_file.write(bg_str)

else:
    # Images are stored locally
    write_to_log("Info", "The imgs folder exists.")

    for img in imgs_to_load + ["test_bg"]:
        if not exists(f"./imgs/{img}.png"):
            img_url = f"https://iamdeedz.github.io/elemental-defense/imgs/{img}.png"
            img_str = urlopen(img_url).read()
            img_file = io.BytesIO(img_str)
            imgs[img] = img_scale(img_load(img_file), calc_scaled_tuple((75, 75)))

            with open(f"./imgs/{img}.png", "wb") as local_img_file:
                local_img_file.write(img_str)

    for img in imgs_to_load:
        imgs[img] = img_scale(img_load(f"./imgs/{img}.png"), calc_scaled_tuple((75, 75)))

    # Background
    for bg in backgrounds_to_load:
        backgrounds[background_name_to_id[bg]] = img_scale(img_load(f"./imgs/{bg}.png"), (screen_width, screen_height))
        small_backgrounds[background_name_to_id[bg]] = img_scale(img_load(f"./imgs/{bg}.png"), calc_scaled_tuple((100, 56.25)))
        medium_backgrounds[background_name_to_id[bg]] = img_scale(img_load(f"./imgs/{bg}.png"), calc_scaled_tuple((250, 140.625)))


# -------------------------------------- #


# Towers
all_towers = {}
tower_costs = {"Dart": 100, "Ice": 150, "Inferno Beam": 150, "Hellfire Launcher": 200, "Pyro Nexus": 175}

elements = ["Grass", "Air", "Fire", "Water", "Rock", "Testing"]

towers_by_element = {
    "Grass": [],
    "Air": [],
    "Water": [],
    "Rock": [],
    "Fire": ["Inferno Beam", "Hellfire Launcher", "Pyro Nexus"],
    "Testing": ["Dart", "Ice"]
}

buffs = {"test": {"name": "Test Buff", "buff": "range", "percent": 25},
         "ice": {"name": "Ice Buff", "buff": "dmg", "percent": 25},
         "pyro": {"name": "Pyro Buff", "buff": "dmg", "percent": 25}}


def update_towers():
    global all_towers
    # This is a workaround to avoid circular imports
    from gameplay.towers.towers import Dart, Ice, Inferno, Hellfire, Pyro
    all_towers["Dart"] = Dart
    all_towers["Ice"] = Ice
    all_towers["Inferno Beam"] = Inferno
    all_towers["Hellfire Launcher"] = Hellfire
    all_towers["Pyro Nexus"] = Pyro
