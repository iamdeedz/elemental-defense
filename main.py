import pygame as p
from constants import screen_width, screen_height, fps, bg, imgs, update_towers
from gameplay.enemy import Enemy
from gameplay.spawn_handler import SpawnHandler
from ui.buttons import update_buttons, draw_buttons
from ui.text import draw_text
from ui.shop import draw_shop, place_tower, update_shop


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
    ball = Enemy(5, 2.5, imgs["ball"])
    ball2 = Enemy(5, 2.5, imgs["ball"], spawn_delay=1)
    ball3 = Enemy(5, 2.5, imgs["ball"], spawn_delay=2)
    ball4 = Enemy(5, 2.5, imgs["ball"], spawn_delay=3)
    ball5 = Enemy(5, 2.5, imgs["ball"], spawn_delay=4)
    boss_ball = Enemy(100, 1, imgs["ball"], spawn_delay=10)
    enemies = [ball, ball2, ball3, ball4, ball5, boss_ball]
    alive_enemies = []
    spawn_handler = SpawnHandler(enemies)

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
                    balance = update_buttons(towers, balance)
                    if tower_being_placed:
                        balance = place_tower(towers, balance, tower_being_placed)
                    tower_being_placed = update_shop(towers, balance)

        if paused:
            continue

        spawn_handler.update()
        alive_enemies += spawn_handler.enemies_to_spawn
        for tower in towers:
            tower.update(alive_enemies)

        # Move enemies
        for enemy in alive_enemies:
            kill = enemy.move()
            if kill:
                alive_enemies.remove(enemy)

        # Draw
        screen.fill(p.Color("black"))
        screen.blit(bg, (0, 0))

        for tower in towers:
            tower.draw(screen)

        for enemy in alive_enemies:
            enemy.draw(screen)

        draw_buttons(screen)
        draw_shop(screen, balance)

        # Text
        draw_text(screen, towers, balance)

        p.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()
