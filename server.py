from pymultiplayer import TCPMultiplayerServer, ServerManager
from gameplay.levels.waves import waves
from json import dumps, loads

server = None

# Game objects
level_id = None

lives = 3
towers = []
wave = None

async def msg_handler(msg, client):
    print(f"Client {client.id} sent: {msg}")

    match msg["type"]:
        case "new_tower":
            # Tell all other clients that a new tower was placed.
            # Give them the coordinates, owner's id, tower's id, and type of tower
            outgoing_msg = {"type": "new_tower", "content": {
                "coordinates": msg["content"]["coordinates"],
                "owner": client.id,
                "tower_id": msg["content"]["tower_id"],
                "tower": msg["content"]["tower"]
            }}
            await server.send_to_all_except(client, dumps(outgoing_msg))

        case "sold_tower":
            # Tell all other clients that a tower was sold.
            # Give them the id
            pass

        case "name":
            # In the id to name dictionary, set the client's id to the name given
            # Tell all other clients the name
            pass

# new tower
# sold tower
# new client's name
#
#
#
#
#
#
#

async def client_joined(client):
    print(f"Client {client.id} joined.")
    # Sync the new client so that they are up to date

    # Tell the other clients the new client's id
    # Add the new client to a list of all clients


async def client_left(client):
    print(f"Client {client.id} left.")
    # Tell the other clients the id of the client that left
    # Remove that client from the list of all clients


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
