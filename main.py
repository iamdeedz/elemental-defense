import pygame as p
from gameplay.game_loop import game_loop
from ui.main_menu.main import main_menu
from constants import screen_width, screen_height, update_towers, version
from debug.logs import write_to_log
from debug.crash_reporter import crash


def main():
    p.init()
    screen = p.display.set_mode((screen_width, screen_height), p.NOFRAME)
    p.display.set_caption("Elemental Defense")
    clock = p.time.Clock()
    update_towers()

    write_to_log("Info", f"Starting Elemental Defense v{version}")

    try:
        level_id = main_menu(screen, clock)
    except Exception as e:
        crash(e, "main_menu")
        return

    try:
        game_loop(screen, clock, level_id)
    except Exception as e:
        crash(e, "game_loop")


if __name__ == '__main__':
    main()
