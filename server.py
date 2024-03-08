from pymultiplayer import TCPMultiplayerServer
from json import dumps, loads


async def msg_handler(msg, client):
    print(f"Client with id {client.id}:", msg["content"])
    print("Sending back:", msg["content"])
    await client.ws.send(dumps(msg))


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler)
    server.run()
