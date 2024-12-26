from math import floor
from pgaddons import Button, InputField, NUMERALS
from constants import calc_scaled_tuple, screen_width, screen_height, calc_scaled_num, is_clicked, elements
from .button_on_clicks import toggle_transfer, send # NOQA
import pygame as p

is_open = False

element_size = calc_scaled_tuple((200, 50))

toggle_button = Button(
    (screen_width-element_size[0], screen_height-element_size[1]),
    element_size,
    p.Color("grey 30"),
    "Transfer Money",
    p.Color("white"),
    font_size=floor(calc_scaled_num(30))
)
toggle_button.on_click = toggle_transfer

money_input = InputField(
    (screen_width-element_size[0], screen_height-(element_size[1]*2)-calc_scaled_num(25, "vertical")),
    element_size,
    p.Color("grey 50"),
    p.Color("grey 70"),
    "Type Here",
    font_size=floor(calc_scaled_num(30)),
    max_length=6,
    char_set=NUMERALS
)


send_button = Button(
    (screen_width-element_size[0], screen_height-(element_size[1]*3)-calc_scaled_num(30, "vertical")),
    element_size,
    p.Color("grey 50"),
    "Send",
    p.Color("white"),
    font_size=floor(calc_scaled_num(30))
)
send_button.on_click = send


def draw_transfer(screen):
    toggle_button.draw(screen)

    if not is_open:
        return

    money_input.draw(screen)
    send_button.draw(screen)


def update_transfer(event):
    match event.type:
        case p.MOUSEBUTTONDOWN:
            if event.button != 1:
                return

            global is_open
            if is_clicked(toggle_button):
                is_open = toggle_button.on_click(is_open)

            if is_clicked(send_button):
                send_button.on_click(money_input.text)

            if not is_open:
                return

            money_input.active = True if is_clicked(money_input) else False

        case p.KEYDOWN:
            money_input.on_key_press(event.key)
