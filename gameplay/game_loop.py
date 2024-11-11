import pygame as p
from constants import fps, bg
from gameplay.levels.waves import waves
from ui.text import draw_text
from ui.shop.shop import Shop
from ui.upgrades import draw_upgrades, update_upgrades, toggle_upgrades
from ui.transfer.transfer import update_transfer, draw_transfer

from pymultiplayer import MultiplayerClient


def game_loop(screen, clock, level_id):
    # Game objects
    balance = 250
    lives = 3
    towers = []
    tower_being_upgraded = None

    wave = waves[level_id][0]
    shop = Shop()

    running = True
    paused = False

    while running:
        if lives <= 0:
            print("you lose because you lost all of your lives")
            running = False
            continue

        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                running = False

            if event.type == p.MOUSEBUTTONDOWN or p.KEYDOWN:
                update_transfer(event)

            if event.type == p.KEYDOWN and event.key == p.K_SPACE:
                paused = not paused

            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Upgrades + Shop
                    balance, were_upgrades_visible, sold = update_upgrades(tower_being_upgraded, balance, towers)
                    if sold:
                        towers.remove(tower_being_upgraded)
                        tower_being_upgraded = None

                    if not were_upgrades_visible:
                        tower_being_upgraded = None

                    for tower in towers:
                        if tower.is_clicked():
                            tower_being_upgraded = tower
                            toggle_upgrades()
                            break

                    balance = shop.update(towers, balance)

        if paused:
            continue

        is_done = wave.update()
        if is_done:
            try:
                wave = waves[level_id][wave.number]
            except IndexError:
                print("you win but i dont have a win screen yet")
                running = False
        for tower in towers:
            balance = tower.update(wave.alive_enemies, towers, balance)

        # Move enemies
        for enemy in wave.alive_enemies:
            return_values = enemy.move()
            is_dead = return_values[0]
            reached_end = return_values[1]
            if is_dead:
                wave.alive_enemies.remove(enemy)
            elif reached_end:
                lives -= 1
                wave.alive_enemies.remove(enemy)

        # Draw
        screen.fill(p.Color("black"))
        screen.blit(bg, (0, 0))

        for tower in towers:
            tower.draw(screen)

        for enemy in wave.alive_enemies:
            enemy.draw(screen)

        shop.draw(screen)
        if tower_being_upgraded:
            draw_upgrades(tower_being_upgraded, screen)

        draw_transfer(screen)

        draw_text(screen, wave.alive_enemies, balance, wave.number, lives)

        p.display.update()
        clock.tick(fps)
