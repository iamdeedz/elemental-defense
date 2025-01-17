import pygame as p
from constants import fps, backgrounds, medium_backgrounds, background_id_to_name, server_manager_ip, calc_scaled_tuple, calc_scaled_num, screen_width, screen_height
from gameplay.levels.waves import waves
from ui.text import draw_text
from ui.shop.shop import Shop
from ui.upgrades import draw_upgrades, update_upgrades, toggle_upgrades
from ui.transfer.transfer import update_transfer, draw_transfer
from math import floor
from pgaddons import InputField, Button, is_clicked

import asyncio
from pymultiplayer import MultiplayerClient
from json import loads, dumps

other_client_ids = set()
id_to_name = {}
client = None


async def msg_handler(msg):
    msg = loads(msg)
    print(msg)

    match msg["type"]:
        case "client_joined":
            other_client_ids.add(msg["content"])

        case "client_left":
            other_client_ids.remove(msg["content"])

        case "sync":
            pass

        case "name":
            id_to_name[msg["content"]["id"]] = msg["content"]["name"]


async def gamestate_manager(screen, clock, level_id):
    go_to_game = await lobby(screen, clock, level_id)

    if go_to_game:
        await multiplayer_game_loop(screen, clock, level_id)

async def lobby(screen, clock, level_id):

    while True:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                await client.disconnect()
                quit()

        screen.fill(p.Color("grey 25"))

        # Draw
        margin = calc_scaled_tuple((100, 100))
        clients_rect = p.Rect(margin, (screen_width-(margin[0]*2), screen_height-(margin[1]*2)))
        p.draw.rect(screen, p.Color("grey 50"), clients_rect, border_radius=round(clients_rect.width / calc_scaled_num(25.6)))

        # Level Preview
        level_preview_size = medium_backgrounds[level_id].get_size()
        level_preview_rect = p.Surface(level_preview_size, p.SRCALPHA)

        p.draw.rect(level_preview_rect, (255, 255, 255), (0, 0, *level_preview_size), border_radius=round(clients_rect.width / calc_scaled_num(35)))

        level_preview = medium_backgrounds[level_id].copy().convert_alpha()
        level_preview.blit(level_preview_rect, (0, 0), None, p.BLEND_RGBA_MIN)

        screen.blit(level_preview,
                    (clients_rect.left + calc_scaled_num(50), clients_rect.top + calc_scaled_num(50, "vertical")))

        # Level Name
        font = p.font.Font(None, floor(calc_scaled_num(112.5)))
        level_name = font.render(background_id_to_name[level_id], True, p.Color("grey 10"))
        screen.blit(level_name, (clients_rect.left + (calc_scaled_num(50)*2) + level_preview_size[0], clients_rect.top + calc_scaled_num(75, "vertical")))

        # Players
        font = p.font.Font(None, floor(calc_scaled_num(30)))
        all_players = other_client_ids.copy()
        all_players.add(client.id)
        for i, player in enumerate(all_players):
            player_name = font.render("", True, p.Color("grey 10"))
            screen.blit(player_name, (clients_rect.left + calc_scaled_num(75),
                                      clients_rect.top + (calc_scaled_num(50, "vertical")*2) + level_preview_size[1] + ((i+1)*(player_name.get_height()+calc_scaled_num(10, "vertical")))))

        p.display.update()
        clock.tick(fps)


async def multiplayer_game_loop(screen, clock, level_id):
    pass


def get_name(screen, clock):
    element_size = calc_scaled_tuple((400, 100))

    name_input = InputField(
        ((screen_width / 2) - (element_size[0] / 2), (screen_height / 2) - (element_size[1] / 2)),
        element_size, "grey 50", "grey 75", "Enter your name...", max_length=12)

    submit_button = Button((name_input.x, name_input.y+element_size[1]), element_size, "grey 50", "Submit")

    font = p.font.Font(None, floor(calc_scaled_num(50)))
    text = None

    while True:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                quit()

            if event.type == p.MOUSEBUTTONDOWN and event.button == 0:
                name_input = True if is_clicked(name_input) else False
                if is_clicked(submit_button):
                    if len(name_input.text) > 3:
                        return name_input.text
                    else:
                        text = font.render("Name must be longer than 3 charcters", True, "grey 10")

            if event.type == p.KEYDOWN:
                name_input.on_key_press(event.key)

        screen.fill("grey 25")

        name_input.draw(screen)
        submit_button.draw(screen)
        if text:
            screen.blit(text, ((screen_width/2)-(text.get_width()/2), submit_button.y+element_size[1]))

        p.display.flip()
        clock.tick(fps)


def start_multiplayer(screen, clock, level_id, port):
    name = get_name(screen, clock)
    print(name)

    global client
    client = MultiplayerClient(msg_handler, ip=server_manager_ip, port=port)
    client.start()

    asyncio.run(gamestate_manager(screen, clock, level_id))
