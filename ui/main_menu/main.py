import pygame as p
from pgaddons import Button
from math import floor
from constants import screen_width, screen_height, fps, is_clicked, calc_scaled_tuple, calc_scaled_num, server_manager_ip, server_manager_port, small_backgrounds, background_id_to_name
from .page import Page # NOQA
from .page_buttons import buttons_by_page # NOQA
from .button_on_clicks import button_on_clicks # NOQA
from pymultiplayer import get_servers
from asyncio import run as async_run
from random import shuffle

# -------------------------------------- #

class ServerDisplay:
    def __init__(self, index, level_id, port):
        self.rect = p.Rect(calc_scaled_tuple((150, 225 + (calc_scaled_num(100, "vertical") * index))),
                          (screen_width - (calc_scaled_num(150) * 2), calc_scaled_num(90, "vertical")))

        self.image = small_backgrounds[level_id]

        self.font = p.font.Font(None, floor(calc_scaled_num(40)))
        self.level_name = self.font.render(background_id_to_name[level_id], True, "white")

        self.join_button = Button((self.rect.right - calc_scaled_num(30) - calc_scaled_num(100), self.rect.top + calc_scaled_num(16.875, "vertical")),
                             (calc_scaled_num(100), self.rect.height - (calc_scaled_num(16.875, "vertical")*2)),
                                  "grey 50", "Join", "white", font=self.font, border_radius=round(calc_scaled_num(17.5)))
        self.join_button.on_click = button_on_clicks["Join"]
        self.join_button.port = port

    def draw(self, screen):
        # Rect
        p.draw.rect(screen, p.Color("grey 25"), self.rect, border_radius=round(calc_scaled_num(17.5)))

        # Level Preview
        screen.blit(self.image,
                    (self.rect.left + calc_scaled_num(30), self.rect.top + calc_scaled_num(16.875, "vertical")))

        # Level Name
        screen.blit(self.level_name, (self.rect.left + calc_scaled_num(30) + calc_scaled_num(100) + calc_scaled_num(20),
                                 self.rect.top + calc_scaled_num(16.875, "vertical")))

        # Join Button
        self.join_button.draw(screen)


multiplayer_page_joining = True
server_displays = []

def update_servers():
    #all_servers_response = async_run(get_servers(server_manager_ip, server_manager_port))

    # Hardcoded Test Response
    all_servers = [
        {"port": 1301, "parameters": {"level_id": -999}},
        {"port": 1303, "parameters": {"level_id": -999}},
        {"port": 1305, "parameters": {"level_id": -999}},
        {"port": 1307, "parameters": {"level_id": -999}},
        {"port": 1309, "parameters": {"level_id": -999}},
    ]

    #all_servers = all_servers_response["content"]

    shuffle(all_servers)

    for i, server in enumerate(all_servers):
        level_id = server["parameters"]["level_id"]
        port = server["port"]
        server_displays.append(ServerDisplay(i, level_id, port))


def draw_multiplayer(screen):
    # Rect
    margin = calc_scaled_tuple((100, 100))
    servers_rect = p.Rect(margin, (screen_width-(margin[0]*2), screen_height-(margin[1]*2)))
    p.draw.rect(screen, p.Color("grey 50"), servers_rect, border_radius=round(servers_rect.width / calc_scaled_num(25.6)))

    if multiplayer_page_joining:
        # List all servers:
        for server_display in server_displays:
            server_display.draw(screen)

    # Draw Buttons
    [button.draw(screen) for button in buttons_by_page["multiplayer"]]

# {"port", "parameters"}

multiplayer_page = Page("multiplayer", parent="play")
multiplayer_page.draw = draw_multiplayer

# -------------------------------------- #

def main_menu(screen, clock):
    global multiplayer_page_joining

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

                    # Multiplayer page has buttons that are not included in its page buttons so we must add those to the list
                    if current_page.name == "multiplayer":
                        page_buttons = current_page.buttons.copy()
                        for server_display in server_displays:
                            page_buttons.append(server_display.join_button)

                    # Otherwise just use the page's buttons as normal
                    else:
                        page_buttons = current_page.buttons


                    for button in page_buttons:
                        if is_clicked(button):

                            # On the play page, the singleplayer and back buttons overlap and this needs special logic
                            if current_page.name != "play":
                                pass

                            # current_page.buttons[-1] is the back button
                            elif button.text == "Single Player" and is_clicked(current_page.buttons[-1]):
                                continue

                            if button.on_click:
                                if button.text == "Join":
                                    return_value = button.on_click(button)

                                else:
                                    return_value = button.on_click()

                                if not return_value:
                                    continue

                                # When a level or join button is clicked it returns two variables and so this has to be handled separate to the rest of the buttons
                                if return_value[0] == "level" or return_value[0] == "join":
                                    return return_value

                                match return_value:
                                    case "back":
                                        current_page = pages[page_keys[current_page.parent]]

                                    case "create server menu":
                                        multiplayer_page_joining = not multiplayer_page_joining

                                    case "multiplayer":
                                        update_servers()
                                        current_page = pages[page_keys["multiplayer"]]

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
