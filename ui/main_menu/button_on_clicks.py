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


def create_server_menu():
    return "create server menu"


def join_server(self):
    return "join", int(self.level_id), int(self.port)


def refresh_servers():
    from .main import update_servers # NOQA
    update_servers()


button_on_clicks = {
    "Back": back,
    "Play": play,
    "Settings": settings,
    "Test Level": test_level,
    "Single Player": single_player,
    "Multi Player": multi_player,
    "Create Server": create_server_menu,
    "Join": join_server,
    "Refresh Servers": refresh_servers
}
