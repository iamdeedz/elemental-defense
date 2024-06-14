from pgaddons import Button
from .button_on_clicks import button_on_clicks # NOQA
from constants import screen_width, screen_height

buttons_by_page = {
    "main": [
        Button((screen_width // 2, screen_height // 2), (200, 50), "grey 50", "Play", "white"),
        Button((screen_width // 2, screen_height // 2 + 200), (200, 50), "grey 50", "Settings", "white")
    ],

    "play": [
        Button((0, 0), (200, 50), "grey 50", "Back", "white"),
        Button((screen_width // 2, screen_height // 2), (150, 150), "grey 50", "Test Level", "white")
    ]
}

for page in buttons_by_page:
    for button in buttons_by_page[page]:
        if button.text in button_on_clicks:
            button.on_click = button_on_clicks[button.text]
        elif button.text == "Back":
            pass
