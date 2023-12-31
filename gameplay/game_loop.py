import pygame as p
from constants import screen_width, screen_height, fps, bg, update_towers
from gameplay.waves import waves
from ui.text import draw_text
from ui.shop.shop import Shop
from ui.upgrades import draw_upgrades, update_upgrades, toggle_upgrades


def game_loop(screen, clock):
    # Game objects
    balance = 150
    towers = []
    tower_being_upgraded = None

    wave = waves[0]
    shop = Shop()

    running = True
    paused = False

    while running:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                running = False

            if event.type == p.KEYDOWN and event.key == p.K_SPACE:
                paused = not paused

            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    balance, were_upgrades_visible = update_upgrades(tower_being_upgraded, balance)

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
            wave = waves[wave.number]
        for tower in towers:
            balance = tower.update(wave.alive_enemies, balance)

        # Move enemies
        for enemy in wave.alive_enemies:
            kill = enemy.move()
            if kill:
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

        # Text
        draw_text(screen, towers, wave.alive_enemies, balance, wave.number)

        p.display.update()
        clock.tick(fps)
