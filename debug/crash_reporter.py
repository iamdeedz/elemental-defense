import pygame as p
from logs import write_to_log


def crash(error):
    report_crash(error)
    try:
        crash_display()

    except Exception as e:
        write_to_log("Error", f"Crash Display Failed: {e}")


def report_crash(error):
    write_to_log("Error", f"Game Crashed: {error}")


# TODO: Display a window with pygame saying that the game crashed and that the error has been saved in a log file.
def crash_display():
    pass
