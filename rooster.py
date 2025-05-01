import pygame
import random
from settings import font, WHITE

class Rooster:
    def __init__(self, name, color, x=0, y=0, is_enemy=False, max_health=100):
        self.name = name
        self.color = color
        self.max_health = max_health
        self.health = self.max_health
        self.skills = {
            "Peck": (10, 0.2),
            "Scratch": (15, 0.3),
            "Charge": (20, 0.35),
            "Wing Flap": (12, 0.4)
        }
        self.x = x
        self.y = y
        self.is_enemy = is_enemy

        base_name = name.lower().replace(' ', '_')
        role = "enemy" if self.is_enemy else "player"
        filename = f"{base_name}_{role}.png"
        image_path = f"assets/{filename}"

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
            self.use_image = True
            print(f"Loaded image: {image_path}")
        except Exception as e:
            print(f"Failed to load image {image_path}: {e}")
            self.rect = pygame.Rect(x, y, 80, 80)
            self.use_image = False

    def draw(self, surface):
        if self.use_image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)

    def attack(self, target, skill):
        if skill not in self.skills:
            return 0  # Invalid skill

        damage, miss_chance = self.skills[skill]

        # If the rooster is an enemy, reduce the miss chance
        if self.is_enemy:
            miss_chance *= 0.5  # 50% lower chance to miss for enemy

        if random.random() < miss_chance:
            print(f"{self.name}'s {skill} missed!")
            return 0

        target.health -= damage
        print(f"{self.name} used {skill} and hit for {damage}!")
        return damage


class ManokNaPuti(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Puti", (255, 255, 255), x, y, is_enemy, max_health=130)
        self.skills = {
            "Peck": (12, 0.2),          
            "Scratch": (18, 0.3),       
            "Charge": (25, 0.35),       
            "Wing Flap": (15, 0.4)   
        }

class ManokNaPula(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Pula", (255, 0, 0), x, y, is_enemy, max_health=140)
        self.skills = {
            "Peck": (18, 0.25),         
            "Scratch": (22, 0.3),       
            "Fury": (28, 0.35),        
            "Flame Beak": (25, 0.4)    
        }

class ManokNaItim(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Itim", (30, 30, 30), x, y, is_enemy, max_health=150)
        self.skills = {
            "Dark Peck": (18, 0.25),     
            "Shadow Claw": (22, 0.3),     
            "Blackout": (35, 0.4),      
            "Ghost Wing": (20, 0.35)      
        }

class ManokNaBalbon(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Balbon", (50, 25, 25), x, y, is_enemy, max_health=160)
        self.skills = {
            "Fierce Kick": (22, 0.3),      
            "Feather Storm": (28, 0.35),    
            "Feather Bomb": (40, 0.4),      
            "Beast Bash": (26, 0.3)        
        }

class ChickenNiGlock9(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Chicken Ni Glock9", (80, 10, 150), x, y, is_enemy, max_health=170)
        self.skills = {
            "Rap Slap": (22, 0.2),        
            "Bar Drop": (30, 0.3),         
            "Mic Explosion": (45, 0.45),    
            "Beat Kick": (26, 0.35)        
        }
