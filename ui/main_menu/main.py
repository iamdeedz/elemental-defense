import pygame as p
from constants import screen_width, screen_height, fps
# from pages import


def main_menu(screen, clock):
    while True:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                quit()

            if event.type == p.MOUSEBUTTONDOWN or event.type == p.KEYDOWN:
                return

        screen.fill(p.Color("black"))

        font = p.font.Font(None, 50)
        text = font.render("Press Any Button to Start!", True, p.Color("white"))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2))

        p.display.update()
        clock.tick(fps)
