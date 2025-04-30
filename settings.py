import pygame

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sabong - Full Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 36)
