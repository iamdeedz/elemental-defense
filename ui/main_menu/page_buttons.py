from math import floor
from pgaddons import Button
from .button_on_clicks import button_on_clicks # NOQA
from constants import screen_width, screen_height, calc_scaled_tuple, calc_scaled_num

buttons_by_page = {
    "home": [
        Button((screen_width // 2, screen_height // 2), calc_scaled_tuple((200, 50)), "grey 50", "Play", "white", font_size=floor(calc_scaled_num(30))),
        Button((screen_width // 2, screen_height // 2 + calc_scaled_num(200, direction="vertical")), calc_scaled_tuple((200, 50)), "grey 50", "Settings", "white", font_size=floor(calc_scaled_num(30)))
    ],

    "play": [
        Button((0, 0), (screen_width//2, screen_height), "grey 25", "Single Player", "white", font_size=floor(calc_scaled_num(60))),
        Button((screen_width//2, 0), (screen_width//2, screen_height), "grey 25", "Multi Player", "white", font_size=floor(calc_scaled_num(60))),
        Button((0, 0), calc_scaled_tuple((200, 50)), "grey 50", "Back", "white", font_size=floor(calc_scaled_num(30)))
    ],

    "settings": [
        Button((0, 0), calc_scaled_tuple((200, 50)), "grey 50", "Back", "white", font_size=floor(calc_scaled_num(30))),
    ],

    "singleplayer": [
        Button((0, 0), calc_scaled_tuple((200, 50)), "grey 50", "Back", "white", font_size=floor(calc_scaled_num(30))),
        Button((screen_width // 2, screen_height // 2), calc_scaled_tuple((150, 150)), "grey 50", "Test Level", "white", font_size=floor(calc_scaled_num(30)))
    ],


    "multiplayer": [
        Button((0, 0), calc_scaled_tuple((200, 50)), "grey 50", "Back", "white", font_size=floor(calc_scaled_num(30))),
        Button(calc_scaled_tuple((150, 125)), calc_scaled_tuple((275, 50)), "grey 25", "Create Server", "white", font_size=floor(calc_scaled_num(30)), border_radius=round(300 / calc_scaled_num(25.6))),
    ],
}

for page in buttons_by_page:
    for button in buttons_by_page[page]:
        if button.text in button_on_clicks:
            button.on_click = button_on_clicks[button.text]
