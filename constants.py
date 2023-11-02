from pygame.transform import scale as img_scale
from pygame.image import load as img_load
from screeninfo import get_monitors

screen_width = 720
screen_height = 405

for monitor in get_monitors():
    if monitor.is_primary:
        screen_width = monitor.width
        screen_height = monitor.height
        break


def calc_new_pos(pos):
    return (pos[0] / 1920) * screen_width, (pos[1] / 1080) * screen_height


fps = 60

imgs = {}
imgs_to_load = ["ball", "dart"]
for img in imgs_to_load:
    imgs[img] = img_scale(img_load(f"imgs/{img}.png"), (calc_new_pos((55, 56))))

bg = img_scale(img_load("imgs/test_bg.png"), (screen_width, screen_height))
