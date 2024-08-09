from pygame import Color, init as pygame_init
from pygame.font import Font
from constants import screen_width, screen_height

pygame_init()
font = Font(None, 30)


def draw_text(screen, enemies, balance, wave, lives, range):
    for i, enemy in enumerate(enemies):
        type_text = font.render(f"Enemy {i+1} Type: {enemy.name}", True, Color("black"))
        hp_text = font.render(f"Enemy {i+1} HP: {enemy.hp}", True, Color("black"))
        screen.blit(type_text, (screen_width - (25 + type_text.get_width()), (0 + (90 * i)) + 25))
        screen.blit(hp_text, (screen_width - (25 + hp_text.get_width()), (30 + (90 * i)) + 25))

    balance_text = font.render(f"Balance: {balance}", True, Color("black"))
    wave_text = font.render(f"Wave: {wave}", True, Color("black"))
    lives_text = font.render(f"Lives: {lives}", True, Color("black"))
    range_text = font.render(f"Range: {range}", True, Color("black"))

    texts = [balance_text, wave_text, lives_text, range_text]
    prev_texts = []

    for text in texts:
        y = screen_height - 40 - (len(prev_texts) * 10)
        for prev_text in prev_texts:
            y -= prev_text.get_height()
        screen.blit(text, (25, y))
        prev_texts.append(text)
