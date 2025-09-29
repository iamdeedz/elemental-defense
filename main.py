from pygame import init as pygame_init
pygame_init()

from debug.logs import write_to_log, check_log_length

check_log_length()
write_to_log("Info", "Program Running")

from gameplay.game_loop import game_loop  # noqa: E402
from gameplay.multiplayer_game_loop import start_multiplayer # noqa: E402
from ui.main_menu.main import main_menu  # noqa: E402
from constants import screen_width, screen_height, update_towers, version, crash_reporter_active  # noqa: E402
from debug.crash_reporter import crash  # noqa: E402
import pygame as p  # noqa: E402


def main():
    screen = p.display.set_mode((screen_width, screen_height), p.NOFRAME)
    p.display.set_caption("Elemental Defense")
    clock = p.time.Clock()
    update_towers()
    write_to_log("Info", f"Starting Elemental Defense v{version}")

    if crash_reporter_active:
        try:
            return_value = main_menu(screen, clock)
        except Exception as e:
            crash(e, "main_menu")
            return

        if return_value[0] == "level":
            try:
                game_loop(screen, clock, return_value[1])
            except Exception as e:
                crash(e, "game_loop")

        elif return_value[0] == "join":
            try:
                # return_value[1] is the level id and return_value[2] is the server port
                start_multiplayer(screen, clock, return_value[1], return_value[2])
            except Exception as e:
                crash(e, "multiplayer_client")

    else:
        return_value = main_menu(screen, clock)

        if return_value[0] == "level":
            game_loop(screen, clock, return_value[1])

        elif return_value[0] == "join":
            start_multiplayer(screen, clock, return_value[1], return_value[2])


if __name__ == '__main__':
    main()
