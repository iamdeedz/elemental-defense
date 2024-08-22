def back():
    return "back"


def play():
    return "play"


def settings():
    return "settings"


def test_level():
    return "level", -999


button_on_clicks = {
    "Back": back,
    "Play": play,
    "Settings": settings,
    "Test Level": test_level
}
