from pygame import Color, init as pygame_init
from pygame.font import Font
from constants import screen_width, screen_height

pygame_init()
font = Font(None, 30)


def draw_text(screen, towers, enemies, balance, wave):
    for i, enemy in enumerate(enemies):
        type_text = font.render(f"Enemy {i+1} Type: {enemy.name}", True, Color("black"))
        hp_text = font.render(f"Enemy {i+1} HP: {enemy.hp}", True, Color("black"))
        screen.blit(type_text, (screen_width - (25 + type_text.get_width()), (0 + (90 * i)) + 25))
        screen.blit(hp_text, (screen_width - (25 + hp_text.get_width()), (30 + (90 * i)) + 25))

    balance_text = font.render(f"Balance: {balance}", True, Color("black"))
    screen.blit(balance_text, (25, screen_height - 40))
    wave_text = font.render(f"Wave: {wave}", True, Color("black"))
    screen.blit(wave_text, (25, screen_height - balance_text.get_height() - 50))
