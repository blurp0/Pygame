# rooster.py

import pygame
from settings import font, WHITE

class Rooster:
    def __init__(self, name, color, x=0, y=0, is_enemy=False):
        self.name = name
        self.color = color
        self.health = 100
        self.skills = {
            "Peck": 10,
            "Scratch": 15,
            "Charge": 20,
            "Dodge": 0
        }
        self.x = x
        self.y = y
        self.is_enemy = is_enemy

        try:
            base_name = name.lower().replace(' ', '_')
            role = "enemy" if self.is_enemy else "player"
            filename = f"{base_name}_{role}.png"
            image_path = f"assets/{filename}"
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
            self.use_image = True
            print(f"Loading image: {image_path}")
        except Exception as e:
            print(f"Failed to load image {image_path}: {e}")
            self.rect = pygame.Rect(x, y, 80, 80)
            self.use_image = False

    def draw(self, surface):
        if self.use_image:
            surface.blit(self.image, (self.x, self.y))
            name_text = font.render(self.name, True, WHITE)
            surface.blit(name_text, (self.x, self.y - 30))
        else:
            pygame.draw.rect(surface, self.color, self.rect)
            name_text = font.render(self.name, True, WHITE)
            surface.blit(name_text, (self.rect.x, self.rect.y - 30))

    def attack(self, target, skill):
        damage = self.skills[skill]
        target.health -= damage
        return damage

class ManokNaPuti(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Puti", (255, 255, 255), x, y, is_enemy)
        self.health = 100
        self.skills = {
            "Peck": 10,
            "Scratch": 15,
            "Charge": 60,
            "Dodge": 0
        }

class ManokNaPula(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Pula", (255, 0, 0), x, y, is_enemy)
        self.health = 110
        self.skills = {
            "Peck": 12,
            "Scratch": 18,
            "Fury": 25,
            "Dodge": 0
        }

class ManokNaItim(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Itim", (30, 30, 30), x, y, is_enemy)
        self.health = 120
        self.skills = {
            "Dark Peck": 15,
            "Shadow Claw": 20,
            "Blackout": 30,
            "Dodge": 0
        }
