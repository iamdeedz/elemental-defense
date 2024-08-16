import pygame as p
from constants import screen_width, screen_height, Pos
from .logs import write_to_log # NOQA


def crash(error, where):
    report_crash(error, where)
    try:
        crash_display()

    except Exception as e:
        write_to_log("Error", f"Crash Display Failed: {e}")


def report_crash(error, where):
    write_to_log("Error", f"Game Crashed during {where}: {error}")


def crash_display():
    p.init()
    fps = 30
    screen = p.display.set_mode((screen_width, screen_height), p.NOFRAME)
    p.display.set_caption("Elemental Defense")
    clock = p.time.Clock()

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.MOUSEBUTTONDOWN or event.type == p.KEYDOWN:
                running = False

        screen.fill(p.Color("black"))

        font = p.font.Font(None, 45)
        text = font.render("Sorry. Elemental Defense has crashed. The error has been saved into a log. Press any "
                           "button to exit.", True, p.Color("white"))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

        p.display.update()
        clock.tick(fps)
