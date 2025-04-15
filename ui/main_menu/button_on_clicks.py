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


def create_server_level_select_left():
    return "create server select", "left"


def create_server_level_select_right():
    return "create server select", "right"


# This has a different naming scheme because it would clash with the pymultiplayer function otherwise
def create_server_button(parameters):
    from pymultiplayer import create_server
    from constants import server_manager_ip, server_manager_port
    from asyncio import run
    run(create_server(server_manager_ip, server_manager_port, parameters))

    # Update the servers
    from .main import update_servers # NOQA
    update_servers()

    # Return this so that after creating a server, the creation menu closes, indicating success
    return "create server menu"


button_on_clicks = {
    "Back": back,
    "Play": play,
    "Settings": settings,
    "Test Level": test_level,
    "Single Player": single_player,
    "Multi Player": multi_player,
    "Create Server": create_server_menu,
    "Join": join_server,
    "Refresh Servers": refresh_servers,
    "<<<": create_server_level_select_left,
    ">>>": create_server_level_select_right,
    "Create": create_server_button
}
