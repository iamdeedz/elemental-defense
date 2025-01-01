from pymultiplayer import TCPMultiplayerServer, ServerManager
from gameplay.levels.waves import waves
from json import dumps, loads

server = None
clients = set()
id_to_name = {}

level_id = None
in_game = False

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

        case "tower_sold":
            # Tell all other clients that a tower was sold.
            # Give them the id
            outgoing_msg = {"type": "tower_sold", "content": {"tower_id": msg["content"]["tower_id"]}}
            await server.send_to_all_except(client, dumps(outgoing_msg))

        case "name":
            # In the id to name dictionary, set the client's id to the name given
            # Tell all other clients the name
            id_to_name[client.id] = msg["content"]
            outgoing_msg = {"type": "name", "content": {"id": client.id, "name": msg["content"]}}
            await server.send_to_all_except(client, dumps(outgoing_msg))

        case "game start":
            # Tell all clients to go game
            outgoing_msg = {"type": "game_start", "content": level_id}
            await server.broadcast(dumps(outgoing_msg))

            # Update in_game variable
            global in_game
            in_game = True


# new tower \/
# sold tower \/
# new client's name \/
# start game \/
#
#
#
#
#


async def client_joined(client):
    print(f"Client {client.id} joined.")
    if in_game:
        outgoing_msg = {"type": "error", "content": "game_in_progress"}
        await server.send(client, dumps(outgoing_msg))
        return

    # Sync the new client so that they are up to date
    outgoing_msg = {"type": "sync", "content": {
        "id_to_name": id_to_name
    }}
    await server.send(client, dumps(outgoing_msg))

    # Tell the other clients the new client's id
    outgoing_msg = {"type": "client_joined", "content": client.id}
    await server.send_to_all_except(client, dumps(outgoing_msg))


async def client_left(client):
    print(f"Client {client.id} left.")

    # Tell the other clients the id of the client that left
    outgoing_msg = {"type": "client_left", "content": client.id}
    await server.send_to_all_except(client, dumps(outgoing_msg))


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
