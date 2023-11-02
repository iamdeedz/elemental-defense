import pygame as p
from constants import screen_width, screen_height, fps, bg, imgs
from gameplay.enemy import Enemy
from gameplay.spawn_handler import SpawnHandler
from gameplay.tower import Tower
from ui.buttons import update_buttons, draw_buttons
from ui.text import draw_text


def main():
    p.init()
    screen = p.display.set_mode((screen_width, screen_height), p.NOFRAME)
    p.display.set_caption("Tower Defense")
    clock = p.time.Clock()

    # Game objects
    dart = Tower(imgs["dart"], 100, 1, 500, 1, (400, 315))
    dart2 = Tower(imgs["dart"], 100, 1, 500, 1, (636, 321))
    dart3 = Tower(imgs["dart"], 100, 1, 500, 1, (500, 100))
    towers = [dart, dart2, dart3]
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
                    update_buttons(towers)

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

        # Text
        draw_text(screen, towers)

        p.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()
