from math import floor
from pgaddons import Button, InputField
from constants import calc_scaled_tuple, screen_width, screen_height, calc_scaled_num, is_clicked
from .button_on_clicks import toggle_transfer # NOQA
import pygame as p

is_open = False

toggle_button_size = calc_scaled_tuple((200, 50))
toggle_button = Button(
    (screen_width-toggle_button_size[0], screen_height-toggle_button_size[1]),
    toggle_button_size,
    p.Color("grey 30"),
    "Transfer Money",
    p.Color("white"),
    font_size=floor(calc_scaled_num(30))
)
toggle_button.on_click = toggle_transfer

money_input_size = calc_scaled_tuple((200, 50))
money_input = InputField(
    (screen_width-money_input_size[0], screen_height-money_input_size[1]-toggle_button_size[1]-calc_scaled_num(5, "vertical")),
    money_input_size,
    p.Color("grey 50"),
    p.Color("grey 70"),
    "Type Here",
    font_size=floor(calc_scaled_num(30)),
    max_length=6
)


def draw_transfer(screen):
    toggle_button.draw(screen)

    if not is_open:
        return

    money_input.draw(screen)


def update_transfer(event):
    match event.type:
        case p.MOUSEBUTTONDOWN:
            if event.button != 1:
                return

            global is_open
            if is_clicked(toggle_button):
                is_open = toggle_button.on_click(is_open)

            if not is_open:
                return

            money_input.active = True if is_clicked(money_input) else False

        case p.KEYDOWN:
            money_input.on_key_press(event.key)
