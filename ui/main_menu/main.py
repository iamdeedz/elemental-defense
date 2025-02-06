import pygame as p
from pgaddons import Button
from math import floor
from constants import screen_width, screen_height, fps, is_clicked, calc_scaled_tuple, calc_scaled_num, \
    server_manager_ip, server_manager_port, small_backgrounds, background_id_to_name, level_ids, medium_backgrounds
from debug.logs import write_to_log
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
        self.join_button.level_id = level_id

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
    write_to_log("Info", "Updating server list")
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


# Multiplayer Page Objects
multiplayer_margin = calc_scaled_tuple((100, 100))
multiplayer_servers_rect = p.Rect(multiplayer_margin, (screen_width - (multiplayer_margin[0] * 2), screen_height - (multiplayer_margin[1] * 2)))

multiplayer_selected_level_id = level_ids[0]

# Get create server button to use as an anchor for positioning
create_server_button = buttons_by_page["multiplayer"][1]

# Level Preview
level_preview_size = medium_backgrounds[multiplayer_selected_level_id].get_size()
level_preview_rect = p.Surface(level_preview_size, p.SRCALPHA)

p.draw.rect(level_preview_rect, (255, 255, 255), (0, 0, *level_preview_size),
                    border_radius=round(multiplayer_servers_rect.width / calc_scaled_num(35)))

level_preview_pos = (create_server_button.x, create_server_button.y + create_server_button.height + calc_scaled_num(25, "vertical"))

# Level Name
multiplayer_creation_font = p.font.Font(None, round(calc_scaled_num(75)))
level_name = multiplayer_creation_font.render(background_id_to_name[multiplayer_selected_level_id], True, "grey 10")
level_name_pos = (level_preview_pos[0] + level_preview_size[0] + calc_scaled_num(50),
                  level_preview_pos[1] + calc_scaled_num(15, "vertical"))

# Buttons
button_size = ((level_name.get_width()/2)-calc_scaled_num(10), (level_preview_size[1]/2)-calc_scaled_num(30, "vertical"))
left_selector_button = Button((level_name_pos[0] + calc_scaled_num(5),
                               level_preview_pos[1] + (level_preview_size[1]/2) + calc_scaled_num(15, "vertical")),
                              button_size, "grey 25", "<<<", "white", font_size=floor(calc_scaled_num(35)), border_radius=round(calc_scaled_num(10)))

right_selector_button = Button((left_selector_button.x + left_selector_button.width + calc_scaled_num(10),
                       level_preview_pos[1] + (level_preview_size[1]/2) + calc_scaled_num(15, "vertical")),
                      button_size, "grey 25", ">>>", "white", font_size=floor(calc_scaled_num(35)), border_radius=round(calc_scaled_num(10)))

left_selector_button.on_click = button_on_clicks[left_selector_button.text]
right_selector_button.on_click = button_on_clicks[right_selector_button.text]

multiplayer_server_creation_buttons = [left_selector_button, right_selector_button]


def draw_multiplayer(screen):
    # Rect
    p.draw.rect(screen, p.Color("grey 50"), multiplayer_servers_rect, border_radius=round(multiplayer_servers_rect.width / calc_scaled_num(25.6)))

    if multiplayer_page_joining:
        # List all servers:
        for server_display in server_displays:
            server_display.draw(screen)

    else:
        # Creating Server

            # Level Selector

                # Level Preview
        level_preview = medium_backgrounds[multiplayer_selected_level_id].copy().convert_alpha()
        level_preview.blit(level_preview_rect, (0, 0), None, p.BLEND_RGBA_MIN)
        screen.blit(level_preview, level_preview_pos)

                # Level Name
        level_name = multiplayer_creation_font.render(background_id_to_name[multiplayer_selected_level_id], True, "grey 10")
        screen.blit(level_name, level_name_pos)

                # Buttons
        left_selector_button.draw(screen)
        right_selector_button.draw(screen)

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
                        [page_buttons.append(server_display.join_button) for server_display in server_displays]
                        [page_buttons.append(button) for button in multiplayer_server_creation_buttons]

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

                                # These buttons are weird because they are nearly identical so have two variables but don't even return anything
                                if return_value[0] == "create server select":
                                    global multiplayer_selected_level_id
                                    index_of_level_id = level_ids.index(multiplayer_selected_level_id)
                                    match return_value[1]:
                                        case "right":
                                            if index_of_level_id == len(level_ids)-1:
                                                multiplayer_selected_level_id = level_ids[0]
                                            else:
                                                multiplayer_selected_level_id = level_ids[index_of_level_id+1]

                                        case "left":
                                            multiplayer_selected_level_id = level_ids[index_of_level_id-1]

                                    break

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
