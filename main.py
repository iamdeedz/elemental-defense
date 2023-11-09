import pygame as p
from constants import screen_width, screen_height, fps, bg, update_towers
from gameplay.waves import waves
from ui.text import draw_text
from ui.shop import draw_shop, place_tower, update_shop
from ui.upgrades import draw_upgrades, update_upgrades, toggle_upgrades


def main():
    p.init()
    screen = p.display.set_mode((screen_width, screen_height), p.NOFRAME)
    p.display.set_caption("Tower Defense")
    clock = p.time.Clock()
    update_towers()

    # Game objects
    balance = 150
    towers = []
    tower_being_placed = None
    tower_being_upgraded = None

    wave = waves[0]

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

                    if tower_being_placed:
                        balance = place_tower(towers, balance, tower_being_placed)
                    tower_being_placed = update_shop(towers, balance)

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

        draw_shop(screen, balance)
        if tower_being_upgraded:
            draw_upgrades(tower_being_upgraded, screen)

        # Text
        draw_text(screen, towers, wave.alive_enemies, balance, wave.number)

        p.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()
