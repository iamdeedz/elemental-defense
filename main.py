from gameplay.game_loop import game_loop
from ui.main_menu import main_menu
from pymultiplayer import TCPMultiplayerServer, MultiplayerClient  # TODO: Implement multiplayer


def main():
    main_menu()
    game_loop()


if __name__ == '__main__':
    main()
