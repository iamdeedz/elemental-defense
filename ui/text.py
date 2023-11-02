from pygame.font import Font
from pygame import Color
font = Font(None, 30)


def draw_text(screen, towers):
    for i, tower in enumerate(towers):
        dmg_text = font.render(f"Tower {i+1} Damage: {tower.dmg}", True, Color("black"))
        range_text = font.render(f"Tower {i+1} Range: {tower.range}", True, Color("black"))
        fire_rate_text = font.render(f"Tower {i+1} Fire Rate: {round(tower.fire_rate, 1)}", True, Color("black"))
        screen.blit(dmg_text, (0, 0 + (90 * i)))
        screen.blit(range_text, (0, 30 + (90 * i)))
        screen.blit(fire_rate_text, (0, 60 + (90 * i)))
