from pygame.font import Font
from pygame import Color
from constants import screen_width, screen_height
font = Font(None, 30)


def draw_text(screen, towers, balance):
    for i, tower in enumerate(towers):
        dmg_text = font.render(f"Tower {i+1} Damage: {tower.dmg}", True, Color("black"))
        range_text = font.render(f"Tower {i+1} Range: {tower.range}", True, Color("black"))
        fire_rate_text = font.render(f"Tower {i+1} Fire Rate: {round(tower.fire_rate, 1)}", True, Color("black"))
        screen.blit(dmg_text, (screen_width - (25 + dmg_text.get_width()), (0 + (90 * i)) + 25))
        screen.blit(range_text, (screen_width - (25 + range_text.get_width()), (30 + (90 * i)) + 25))
        screen.blit(fire_rate_text, (screen_width - (25 + fire_rate_text.get_width()), (60 + (90 * i)) + 25))

    balance_text = font.render(f"Balance: {balance}", True, Color("black"))
    screen.blit(balance_text, (25, screen_height - 40))
