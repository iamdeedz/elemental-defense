from pymultiplayer import TCPMultiplayerServer, ServerManager

server = None


async def msg_handler(msg, client):
    print(f"Client {client.id} sent: {msg}")


async def client_joined(client):
    print(f"Client {client.id} joined.")


async def client_left(client):
    print(f"Client {client.id} left.")


def init_func(ip, port, parameters):
    global server
    server = TCPMultiplayerServer(msg_handler, ip, port, max_clients=4)
    server.set_client_joined_func(client_joined)
    server.set_client_left_func(client_left)
    server.run()


if __name__ == "__main__":
    server_manager = ServerManager("127.0.0.1", 1300, 4, init_func)
    server_manager.run()
