def back():
    return "back"


def play():
    return "play"


def settings():
    return "settings"


def single_player():
    return "singleplayer"


def multi_player():
    return "multiplayer"


def test_level():
    return "level", -999


button_on_clicks = {
    "Back": back,
    "Play": play,
    "Settings": settings,
    "Test Level": test_level,
    "Single Player": single_player,
    "Multi Player": multi_player
}
