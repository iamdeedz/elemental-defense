def back():
    return "back"


def play():
    return "play"


def test_level():
    return "level", -999


button_on_clicks = {
    "Back": back,
    "Play": play,
    "Test Level": test_level
}
