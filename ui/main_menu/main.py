from math import floor
import pygame as p
from debugpy.common.timestamp import current

from constants import screen_width, screen_height, fps, is_clicked, calc_scaled_num
from .page import Page # NOQA


def main_menu(screen, clock):
    current_page = "title"
    pages = [Page("home"),
             Page("play", parent="home"), Page("settings", parent="home"),
             Page("singleplayer", parent="play"), Page("multiplayer", parent="play")]
    page_keys = {page.name: i for i, page in enumerate(pages)}
    print(page_keys)

    while True:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                quit()

            # If on title page and any button is pressed, go to main menu
            if current_page == "start" and (event.type == p.MOUSEBUTTONDOWN or event.type == p.KEYDOWN):
                current_page = pages[page_keys["main"]]

            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in current_page.buttons:
                        if is_clicked(button):

                            # On the play page, the singleplayer and back buttons overlap and this needs special logic
                            if current_page.name != "play":
                                pass

                            # current_page.buttons[-1] is the back button
                            elif button.text == "Single Player" and is_clicked(current_page.buttons[-1]):
                                continue

                            if button.on_click:
                                return_value = button.on_click()
                                if return_value[0] == "level":
                                    return return_value[1]

                                elif return_value == "back":
                                    current_page = pages[page_keys[current_page.parent]]

                                else:
                                    current_page = pages[page_keys[return_value]]

        screen.fill(p.Color("grey 25"))

        if current_page == "title":
            font = p.font.Font(None, floor(calc_scaled_num(100)))
            text = font.render("Elemental Defense", True, p.Color("white"))
            screen.blit(text, (screen_width // 2 - calc_scaled_num(text.get_width() // 2), (screen_height // 2 - calc_scaled_num(text.get_height() // 2, direction="vertical") - calc_scaled_num(125, direction="vertical"))))
            font = p.font.Font(None, floor(calc_scaled_num(50)))
            text = font.render("Click anywhere to start", True, p.Color("white"))
            screen.blit(text, (screen_width // 2 - calc_scaled_num(text.get_width() // 2), (screen_height // 2 - calc_scaled_num(text.get_height() // 2, direction="vertical") + calc_scaled_num(75, direction="vertical"))))

        else:
            pages[pages.index(current_page)].draw(screen)
            if current_page == "play":
                p.draw.line(screen, "grey 50", (screen_width//2, 0), (screen_width//2, screen_height), 5)

        p.display.update()
        clock.tick(fps)
