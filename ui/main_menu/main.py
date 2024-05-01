import pygame as p
from constants import screen_width, screen_height, fps, calc_new_pos, is_clicked
from .page import Page # NOQA


def main_menu(screen, clock):
    current_page = "start"
    pages = [Page("main"), Page("play", parent="main")]
    page_keys = {page.name: i for i, page in enumerate(pages)}

    while True:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                quit()

            if event.type == p.MOUSEBUTTONDOWN or event.type == p.KEYDOWN:
                if current_page == "start":
                    current_page = pages[page_keys["main"]]

                else:
                    for button in current_page.buttons:
                        if is_clicked(button):
                            if button.on_click:
                                return_value = button.on_click()
                                if return_value == -999:
                                    return
                                elif return_value == "back":
                                    current_page = pages[page_keys[current_page.parent]]
                                else:
                                    current_page = pages[page_keys[return_value]]

        screen.fill(p.Color("grey 25"))

        if current_page == "start":
            font = p.font.Font(None, 100)
            text = font.render("Elemental Defense", True, p.Color("white"))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, (screen_height // 2 - text.get_height() // 2) - calc_new_pos(125, direction="vertical")))
            font = p.font.Font(None, 50)
            text = font.render("Click anywhere to start", True, p.Color("white"))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, (screen_height // 2 - text.get_height() // 2) + calc_new_pos(75, direction="vertical")))

        else:
            pages[pages.index(current_page)].draw(screen)

        p.display.update()
        clock.tick(fps)
