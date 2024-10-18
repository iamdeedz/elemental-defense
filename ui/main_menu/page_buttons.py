from math import floor
from pgaddons import Button
from .button_on_clicks import button_on_clicks # NOQA
from constants import screen_width, screen_height, calc_scaled_tuple, calc_scaled_num

buttons_by_page = {
    "main": [
        Button((screen_width // 2, screen_height // 2), calc_scaled_tuple((200, 50)), "grey 50", "Play", "white", font_size=floor(calc_scaled_num(30))),
        Button((screen_width // 2, screen_height // 2 + calc_scaled_num(200, direction="vertical")), calc_scaled_tuple((200, 50)), "grey 50", "Settings", "white", font_size=floor(calc_scaled_num(30)))
    ],

    "play": [
        Button((0, 0), calc_scaled_tuple((200, 50)), "grey 50", "Back", "white", font_size=floor(calc_scaled_num(30))),
        Button((screen_width // 2, screen_height // 2), calc_scaled_tuple((150, 150)), "grey 50", "Test Level", "white", font_size=floor(calc_scaled_num(30)))
    ],

    "settings": [
        Button((0, 0), calc_scaled_tuple((200, 50)), "grey 50", "Back", "white", font_size=floor(calc_scaled_num(30))),
    ],
}

for page in buttons_by_page:
    for button in buttons_by_page[page]:
        if button.text in button_on_clicks:
            button.on_click = button_on_clicks[button.text]
        elif button.text == "Back":
            pass
