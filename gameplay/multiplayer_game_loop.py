import pygame as p
from constants import fps, backgrounds, server_manager_ip
from gameplay.levels.waves import waves
from ui.text import draw_text
from ui.shop.shop import Shop
from ui.upgrades import draw_upgrades, update_upgrades, toggle_upgrades
from ui.transfer.transfer import update_transfer, draw_transfer

import asyncio
from pymultiplayer import MultiplayerClient
from json import loads, dumps


client = None


async def msg_handler(msg):
    msg = loads(msg)
    print(msg)

    match msg["type"]:
        case "client_joined":
            pass

        case "client_left":
            pass

        case "sync":
            pass


async def gamestate_manager(screen, clock):
    go_to_game = await lobby(screen, clock)

    if go_to_game:
        await multiplayer_game_loop(screen, clock)

async def lobby(screen, clock):
    while True:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                await client.disconnect()
                quit()

        screen.fill(p.Color("grey 25"))

        p.display.update()
        clock.tick(fps)

async def multiplayer_game_loop(screen, clock):
    pass


def start_multiplayer(port, screen, clock):
    global client
    client = MultiplayerClient(msg_handler, ip=server_manager_ip, port=port)
    client.start()

    asyncio.run(gamestate_manager(screen, clock))
