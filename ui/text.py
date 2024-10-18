from math import floor
from pygame import Color, init as pygame_init
from pygame.font import Font
from constants import screen_width, screen_height, calc_scaled_num, calc_scaled_tuple

pygame_init()
font = Font(None, floor(calc_scaled_num(30)))


def draw_text(screen, enemies, balance, wave, lives):
    for i, enemy in enumerate(enemies):
        type_text = font.render(f"Enemy {i+1} Type: {enemy.name}", True, Color("black"))
        hp_text = font.render(f"Enemy {i+1} HP: {enemy.hp}", True, Color("black"))
        screen.blit(type_text, (screen_width - (25 + type_text.get_width()), calc_scaled_num((0 + (90 * i)) + 25)))
        screen.blit(hp_text, (screen_width - (25 + hp_text.get_width()), calc_scaled_num((30 + (90 * i)) + 25)))

    balance_text = font.render(f"Balance: {balance}", True, Color("black"))
    wave_text = font.render(f"Wave: {wave}", True, Color("black"))
    lives_text = font.render(f"Lives: {lives}", True, Color("black"))

    texts = [balance_text, wave_text, lives_text]
    prev_texts = []

    for text in texts:
        y = screen_height - 40 - calc_scaled_num(len(prev_texts) * 10)
        for prev_text in prev_texts:
            y -= prev_text.get_height()
        screen.blit(text, (calc_scaled_num(25), y))
        prev_texts.append(text)
