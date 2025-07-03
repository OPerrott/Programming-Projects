import pygame

def draw_flash(screen, intensity):
    if intensity > 0:
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(intensity)
        overlay.fill((255, 255, 255))
        screen.blit(overlay, (0, 0))

def draw_ui(screen, font, score, time_left, level, best_score):
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f"Time: {time_left}", True, (255, 255, 255)), (10, 40))
    screen.blit(font.render(f"Level: {level}", True, (255, 255, 255)), (10, 70))
    screen.blit(font.render(f"Best: {best_score}", True, (255, 215, 0)), (10, 100))
