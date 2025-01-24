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

all_ids = []
id_to_name = {}
client = None
name = None
is_owner = False
go_to_game = False


async def msg_handler(msg):
    global id_to_name, all_ids, is_owner, go_to_game
    msg = loads(msg)
    print(msg)

    match msg["type"]:
        case "client_joined":
            all_ids.append(msg["content"])

        case "client_left":
            all_ids.remove(msg["content"])

        case "sync":
            all_ids = msg["content"]["all_ids"]
            id_to_name = msg["content"]["id_to_name"]
            id_to_name[client.id] = name

        case "name":
            id_to_name[msg["content"]["id"]] = msg["content"]["name"]

        case "owner":
            is_owner = True

        case "start":
            go_to_game = True

        case "error":
            match msg["content"]:
                case "game_in_progress":
                    await client.disconnect()
                    quit()


async def gamestate_manager(screen, clock, level_id):
    await lobby(screen, clock, level_id)

    await multiplayer_game_loop(screen, clock, level_id)


async def lobby(screen, clock, level_id):
    while True:
        # Connecting
        if client.id:
            break

        font = p.font.Font(None, floor(calc_scaled_num(75)))
        text = font.render("Connecting...", True, "grey 80")

        screen.fill("grey 25")

        screen.blit(text, ((screen_width/2)-(text.get_width()/2), (screen_height/2)-(text.get_height()/2)))

        p.display.update()
        clock.tick(fps)

    msg = {"type": "name", "content": name}
    await client.send(dumps(msg))

    margin = calc_scaled_tuple((100, 100))

    clients_rect = p.Rect(margin, (screen_width-(margin[0]*2), screen_height-(margin[1]*2)))

    start_button = Button((screen_width - calc_scaled_num(450), screen_height - calc_scaled_num(150, "vertical") - calc_scaled_num(300/4, "vertical")),
                          calc_scaled_tuple((275, 275/4)), "grey 25", "Start", "grey 90",
                          font_size=floor(calc_scaled_num(37.5)),
                          border_radius=round(17.5))

    while True:
        if go_to_game:
            return

        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                await client.disconnect()
                quit()

            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                if is_owner:
                    if is_clicked(start_button):
                        outgoing_msg = {"type": "start"}
                        await client.send(dumps(outgoing_msg))

        screen.fill(p.Color("grey 25"))

        # Draw
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
        font = p.font.Font(None, floor(calc_scaled_num(50)))

        # Ensure all keys are integers, not strings
        global id_to_name
        for key, value in id_to_name.copy().items():
            id_to_name[int(key)] = value

        for i, player in enumerate(all_ids):
            try:
                player_name_str = id_to_name[player]
            except KeyError:
                player_name_str = f"Player {player}"

            player_name = font.render(player_name_str, True, p.Color("grey 10"))
            screen.blit(player_name, (clients_rect.left + calc_scaled_num(75),
                                      clients_rect.top + (calc_scaled_num(50, "vertical")*2) + level_preview_size[1] + ((i+1)*(player_name.get_height()+calc_scaled_num(10, "vertical")))))

        # Start Button
        if is_owner:
            start_button.draw(screen)

        p.display.update()
        clock.tick(fps)


async def multiplayer_game_loop(screen, clock, level_id):
    while True:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                await client.disconnect()
                quit()

        screen.fill(p.Color("black"))
        screen.blit(backgrounds[level_id], (0, 0))

        p.display.update()
        clock.tick(fps)


def get_name(screen, clock):
    element_size = calc_scaled_tuple((300, 75))

    name_input = InputField(
        ((screen_width / 2) - (element_size[0] / 2), (screen_height / 2) - (element_size[1] / 2)-(element_size[1] / 2)),
        element_size, "grey 30", "grey 40", "Enter your name...", font_colour="grey 80", max_length=12, font_size=floor(calc_scaled_num(35)))

    submit_button = Button((name_input.x, name_input.y+element_size[1]), element_size, "grey 50", "Submit", text_colour="grey 80", font_size=floor(calc_scaled_num(35)))

    font = p.font.Font(None, floor(calc_scaled_num(50)))
    text = None

    while True:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                quit()

            if event.type == p.KEYDOWN and event.key == p.K_RETURN:
                if len(name_input.text) > 3:
                    return name_input.text
                else:
                    text = font.render("Name must be longer than 3 characters", True, "white")

            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                name_input.active = True if is_clicked(name_input) else False
                if is_clicked(submit_button):
                    if len(name_input.text) > 3:
                        return name_input.text
                    else:
                        text = font.render("Name must be longer than 3 characters", True, "white")

            if event.type == p.KEYDOWN:
                name_input.on_key_press(event.key)

        screen.fill("grey 25")

        name_input.draw(screen)
        submit_button.draw(screen)
        if text:
            screen.blit(text, ((screen_width/2)-(text.get_width()/2), submit_button.y+element_size[1]+calc_scaled_num(50, direction="vertical")))

        p.display.update()
        clock.tick(fps)


def start_multiplayer(screen, clock, level_id, port):
    input_name = get_name(screen, clock)
    global name
    name = input_name

    global client
    client = MultiplayerClient(msg_handler, ip=server_manager_ip, port=port)
    client.start()

    asyncio.run(gamestate_manager(screen, clock, level_id))
