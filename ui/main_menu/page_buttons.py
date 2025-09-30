from math import floor
from pgaddons import Button
from .button_on_clicks import button_on_clicks # NOQA
from constants import screen_width, screen_height, calc_scaled_tuple, calc_scaled_num, font_path
from pygame.font import Font

scaled_400x100_tuple = calc_scaled_tuple((400, 100))

buttons_by_page = {
    "home": [
        Button((screen_width // 2 - (scaled_400x100_tuple[0] // 2), screen_height // 2 - (scaled_400x100_tuple[1] // 2) - calc_scaled_num(100, direction="vertical")), scaled_400x100_tuple, "grey 50", "Play", "white", font=Font(font_path, floor(calc_scaled_num(45)))),
        Button((screen_width // 2 - (scaled_400x100_tuple[0] // 2), screen_height // 2 + calc_scaled_num(100, direction="vertical")), scaled_400x100_tuple, "grey 50", "Settings", "white", font=Font(font_path, floor(calc_scaled_num(45))))
    ],

    "play": [
        Button((0, 0), (screen_width//2, screen_height), "grey 25", "Single Player", "white", font=Font(font_path, floor(calc_scaled_num(60)))),
        Button((screen_width//2, 0), (screen_width//2, screen_height), "grey 25", "Multi Player", "white", font=Font(font_path, floor(calc_scaled_num(60)))),
        Button((0, 0), calc_scaled_tuple((200, 50)), "grey 50", "Back", "white", font=Font(font_path, floor(calc_scaled_num(30))))
    ],

    "settings": [
        Button((0, 0), calc_scaled_tuple((200, 50)), "grey 50", "Back", "white", font=Font(font_path, floor(calc_scaled_num(30)))),
    ],

    "singleplayer": [
        Button((0, 0), calc_scaled_tuple((200, 50)), "grey 50", "Back", "white", font=Font(font_path, floor(calc_scaled_num(30)))),
        Button((screen_width // 2, screen_height // 2), calc_scaled_tuple((150, 150)), "grey 50", "Test Level", "white", font=Font(font_path, floor(calc_scaled_num(30))))
    ],


    "multiplayer": [
        Button((0, 0), calc_scaled_tuple((200, 50)), "grey 50", "Back", "white", font=Font(font_path, floor(calc_scaled_num(30)))),
        Button(calc_scaled_tuple((150, 125)), calc_scaled_tuple((275, 50)), "grey 25", "Create Server", "white", font=Font(font_path, floor(calc_scaled_num(30))), border_radius=round(300 / calc_scaled_num(25.6))),
        Button((screen_width-calc_scaled_num(425), calc_scaled_num(125, "vertical")), calc_scaled_tuple((275, 50)), "grey 25", "Refresh Servers", "white", font=Font(font_path, floor(calc_scaled_num(30))), border_radius=round(300 / calc_scaled_num(25.6)))
    ],
}

for page in buttons_by_page:
    for button in buttons_by_page[page]:
        if button.text in button_on_clicks:
            button.on_click = button_on_clicks[button.text]
