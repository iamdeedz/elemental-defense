from debug.logs import write_to_log

write_to_log("Info", "Program Running")

from gameplay.game_loop import game_loop  # noqa: E402
from ui.main_menu.main import main_menu  # noqa: E402
from constants import screen_width, screen_height, update_towers, version, crash_reporter_active  # noqa: E402
from debug.crash_reporter import crash  # noqa: E402
import pygame as p  # noqa: E402


def main():
    p.init()
    screen = p.display.set_mode((screen_width, screen_height), p.NOFRAME)
    p.display.set_caption("Elemental Defense")
    clock = p.time.Clock()
    update_towers()
    write_to_log("Info", f"Starting Elemental Defense v{version}")

    if crash_reporter_active:
        try:
            level_id = main_menu(screen, clock)
        except Exception as e:
            crash(e, "main_menu")
            return

        try:
            game_loop(screen, clock, level_id)
        except Exception as e:
            crash(e, "game_loop")

    else:
        level_id = main_menu(screen, clock)
        game_loop(screen, clock, level_id)


if __name__ == '__main__':
    main()
