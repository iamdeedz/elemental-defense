from pymultiplayer import TCPMultiplayerServer, ServerManager
from gameplay.levels.waves import waves

server = None

# Game objects
level_id = None

balance = 250
lives = 3
towers = []
wave = None

async def msg_handler(msg, client):
    print(f"Client {client.id} sent: {msg}")


async def client_joined(client):
    print(f"Client {client.id} joined.")


async def client_left(client):
    print(f"Client {client.id} left.")


def init_func(ip, port, parameters):
    global server, level_id
    level_id = parameters["level_id"]

    server = TCPMultiplayerServer(msg_handler, ip, port, max_clients=4)
    server.set_client_joined_func(client_joined)
    server.set_client_left_func(client_left)
    server.run()


if __name__ == "__main__":
    server_manager = ServerManager("127.0.0.1", 1300, 4, init_func)
    server_manager.run()
