from math import floor
from pgaddons import Button, InputField
from pygame import Color
from constants import calc_scaled_tuple, screen_width, screen_height, calc_scaled_num, is_clicked
from .button_on_clicks import toggle_transfer # NOQA

is_open = False

toggle_button_size = calc_scaled_tuple((200, 50))
toggle_button = Button(
    (screen_width-toggle_button_size[0], screen_height-toggle_button_size[1]),
    toggle_button_size,
    Color("grey 50"),
    "Transfer Money",
    Color("white"),
    font_size=floor(calc_scaled_num(30))
)
toggle_button.on_click = toggle_transfer


def draw_transfer(screen):
    toggle_button.draw(screen)


def update_transfer():
    global is_open
    if is_clicked(toggle_button):
        is_open = toggle_button.on_click(is_open)
