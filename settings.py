import pygame

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sabong - Full Game")

# Base Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
GRAY = (200, 200, 200)

# Additional Colors
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (220, 220, 220)
PASTEL_GREEN = (119, 221, 119)
BLUE = (70, 130, 180)
DARK_BLUE = (25, 25, 112)
GOLD = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
BEIGE = (245, 245, 220)
NAVY = (0, 0, 128)

HIGHLIGHT_COLOR = (255, 0, 0)
BUTTON_COLOR = (0, 0, 255) 
FONT_SIZE = 24 
# Font
font = pygame.font.SysFont(None, 36)
