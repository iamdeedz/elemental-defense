import pygame as p
from gameplay.game_loop import game_loop
from ui.main_menu.main import main_menu
from constants import screen_width, screen_height, update_towers, version
from debug.logs import write_to_log


def main():
    p.init()
    screen = p.display.set_mode((screen_width, screen_height), p.NOFRAME)
    p.display.set_caption("Elemental Defense")
    clock = p.time.Clock()
    update_towers()

    write_to_log("Info", f"Starting Elemental Defense v{version}")

    level_id = main_menu(screen, clock)

    game_loop(screen, clock, level_id)


if __name__ == '__main__':
    main()
