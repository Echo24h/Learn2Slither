import pygame
from .settings import BLOCK_SIZE, WIDTH, HEIGHT


def init_fonts():
    """Initialiser les polices de caractères"""
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)
    return font_style, score_font


def show_score(score, screen, score_font):
    """Afficher le score sur l'écran"""
    value = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(value, [0, 0])  # Afficher le score en haut à gauche


def load_sprite(path):
    """Charger un sprite à partir d'un fichier image"""
    sprite = pygame.image.load(path)
    return pygame.transform.scale(sprite, (BLOCK_SIZE, BLOCK_SIZE))


def draw_background(screen):
    """Dessiner un fond d'échiquier sur l'écran"""

    light_gray = (169, 169, 169)  # Gris clair
    dark_gray = (105, 105, 105)   # Gris foncé

    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, light_gray, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            else:
                pygame.draw.rect(screen, dark_gray, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))