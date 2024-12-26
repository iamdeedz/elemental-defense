import pygame as p
from math import floor
from constants import screen_width, screen_height, fps, is_clicked, calc_scaled_tuple, calc_scaled_num, server_manager_ip, server_manager_port
from .page import Page # NOQA
from .page_buttons import buttons_by_page # NOQA
from pymultiplayer import get_servers
from asyncio import run as async_run
from random import shuffle

# -------------------------------------- #

multiplayer_page_joining = True

def draw_multiplayer(screen):
    # Rect
    margin = calc_scaled_tuple((100, 100))
    servers_rect = p.Rect(margin, (screen_width-(margin[0]*2), screen_height-(margin[1]*2)))
    p.draw.rect(screen, p.Color("grey 50"), servers_rect, border_radius=round(servers_rect.width / calc_scaled_num(25.6)))

    if multiplayer_page_joining:
        # List all servers:
        #all_servers = async_run(get_servers(server_manager_ip, server_manager_port))
        all_servers = [
            {"port": 1301, "parameters": {"level": -999}},
            {"port": 1303, "parameters": {"level": -999}},
            {"port": 1305, "parameters": {"level": -999}}
        ]
        shuffle(all_servers)
        for i, server in enumerate(all_servers):
            rect = p.Rect(calc_scaled_tuple((150, 225 + (calc_scaled_num(100, "vertical") * i))),
                          (screen_width - (calc_scaled_num(150) * 2), calc_scaled_num(90, "vertical")))
            screen.blit()
            p.draw.rect(screen, p.Color("grey 25"), rect, border_radius=round(calc_scaled_num(17.5)))

    # Draw Buttons
    [button.draw(screen) for button in buttons_by_page["multiplayer"]]

# {"port", "parameters"}

multiplayer_page = Page("multiplayer", parent="play")
multiplayer_page.draw = draw_multiplayer

# -------------------------------------- #

def main_menu(screen, clock):
    current_page = "title"
    pages = [Page("home"),
             Page("play", parent="home"), Page("settings", parent="home"),
             Page("singleplayer", parent="play"), multiplayer_page]
    page_keys = {page.name: i for i, page in enumerate(pages)}

    while True:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                quit()

            # If on title page and any button is pressed, go to main menu
            if current_page == "title" and (event.type == p.MOUSEBUTTONDOWN or event.type == p.KEYDOWN):
                current_page = pages[page_keys["home"]]

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

                                # When a level button is clicked it returns two variables and so this has to be handled separate to the rest of the buttons
                                if return_value[0] == "level":
                                    return return_value[1]

                                match return_value:
                                    case "back":
                                        current_page = pages[page_keys[current_page.parent]]

                                    case "create server menu":
                                        global multiplayer_page_joining
                                        multiplayer_page_joining = not multiplayer_page_joining

                                    case _:
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
