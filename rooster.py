import pygame
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

import random
from settings import font, WHITE

class Rooster:
    def __init__(self, name, color, x=0, y=0, is_enemy=False, max_health=100):
        self.name = name
        self.color = color
        self.is_enemy = is_enemy

        # Buffed stats for enemy
        health_bonus= 50 if is_enemy else 0  # +50 HP for enemies
        self.max_health = max_health + health_bonus
        self.health = self.max_health

        self.skills = {
            "Tuka": {"damage": 10, "miss_chance": 0.2, "description": "Isang mabilis na pag-atake gamit ang tuka."},
            "Kalkal": {"damage": 15, "miss_chance": 0.3, "description": "Isang matalim na kalkal gamit ang mga pangil."},
            "Sugod": {"damage": 20, "miss_chance": 0.35, "description": "Mag-sugod sa kalaban."},
            "Palo ng Pakpak": {"damage": 12, "miss_chance": 0.4, "description": "Palo ng pakpak upang magdulot ng malalakas na hangin."}
        }

        if is_enemy:
            self._boost_skills()

        self.x = x
        self.y = y

        base_name = name.lower().replace(' ', '_')
        role = "enemy" if self.is_enemy else "player"
        filename = f"{base_name}_{role}.png"
        image_path = f"assets/{filename}"

        try:
            self.image = pygame.image.load(resource_path(image_path)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (250, 250))
            self.use_image = True
            print(f"Loaded image: {image_path}")
        except Exception as e:
            print(f"Failed to load image {image_path}: {e}")
            self.rect = pygame.Rect(x, y, 80, 80)
            self.use_image = False

    def _boost_skills(self):
        # Increase skill damage by 25% for enemies
        for key in self.skills:
            skill = self.skills[key]
            skill["damage"] = int(skill["damage"] * 1.1)

    def draw(self, surface):
        if self.use_image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)

    def attack(self, target, skill_name):
        if skill_name not in self.skills:
            return 0

        skill = self.skills[skill_name]
        damage = skill["damage"]
        miss_chance = skill["miss_chance"]

        if self.is_enemy:
            miss_chance *= 0.8  # Enemies are more accurate

        if random.random() < miss_chance:
            print(f"{self.name}'s {skill_name} missed!")
            return 0

        target.health -= damage
        print(f"{self.name} used {skill_name} and hit for {damage}!")
        return damage

# Subclasses — enemy boost handled automatically
class ManokNaPuti(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Puti", (255, 255, 255), x, y, is_enemy, max_health=130)
        self.skills = {
            "Tuka": {"damage": 12, "miss_chance": 0.2, "description": "Isang mabilis na tuka na nagbibigay ng magaan na pinsala."},
            "Kalkal": {"damage": 18, "miss_chance": 0.3, "description": "Isang matalim na kalkal na may katamtamang pinsala."},
            "Sugod": {"damage": 25, "miss_chance": 0.35, "description": "Sugod ng buong lakas, na nagbibigay ng malakas na pinsala."},
            "Palo ng Pakpak": {"damage": 15, "miss_chance": 0.4, "description": "Palo ng pakpak upang magdulot ng wind blast."}
        }
        if is_enemy:
            self._boost_skills()

class ManokNaPula(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Pula", (255, 0, 0), x, y, is_enemy, max_health=140)
        self.skills = {
            "Tuka": {"damage": 18, "miss_chance": 0.25, "description": "Isang mabilis at malakas na tuka."},
            "Kalkal": {"damage": 22, "miss_chance": 0.3, "description": "Isang kalkal na may matinding pinsala."},
            "Galit": {"damage": 28, "miss_chance": 0.35, "description": "Isang matinding at wild na atake."},
            "Tuka ng Apoy": {"damage": 25, "miss_chance": 0.4, "description": "Pasikatin ang tuka at magbigay ng pinsala mula sa apoy."}
        }
        if is_enemy:
            self._boost_skills()

class ManokNaItim(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Itim", (30, 30, 30), x, y, is_enemy, max_health=150)
        self.skills = {
            "Madilim na Tuka": {"damage": 18, "miss_chance": 0.25, "description": "Isang madilim na tuka na may pinsalang tumatagal."},
            "Anino ng Pangil": {"damage": 22, "miss_chance": 0.3, "description": "Isang anino ng pangil na may katamtamang pinsala."},
            "Kadiliman": {"damage": 35, "miss_chance": 0.4, "description": "Atake na may kadiliman na pansamantalang nagpapadilim sa kalaban."},
            "Pakpak ng Multo": {"damage": 20, "miss_chance": 0.35, "description": "Palo ng pakpak na may multong aura at nagdudulot ng pinsala."}
        }
        if is_enemy:
            self._boost_skills()

class ManokNaBalbon(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Manok na Balbon", (50, 25, 25), x, y, is_enemy, max_health=160)
        self.skills = {
            "Matingkad na Sipang": {"damage": 22, "miss_chance": 0.3, "description": "Isang malakas na sipang na may malupit na pinsala."},
            "Bagyong Balahibo": {"damage": 28, "miss_chance": 0.35, "description": "Isang bagyong balahibo na nagdudulot ng malawakang pinsala."},
            "Bomba ng Balahibo": {"damage": 40, "miss_chance": 0.4, "description": "Maglunsad ng bomba ng balahibo para sa matinding pinsala."},
            "Pagbuga ng Hayop": {"damage": 26, "miss_chance": 0.3, "description": "Pagbash sa kalaban gamit ang lakas ng hayop."}
        }
        if is_enemy:
            self._boost_skills()

class ChickenNiGlock9(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False):
        super().__init__("Chicken Ni Glock9", (80, 10, 150), x, y, is_enemy, max_health=170)
        self.skills = {
            "Rap Sapantaha": {"damage": 22, "miss_chance": 0.2, "description": "Isang mabilis na slap na may rap style."},
            "Pagbagsak ng Bar": {"damage": 30, "miss_chance": 0.3, "description": "I-drop ang bar para sa malupit na pinsala."},
            "Mic Pagputok": {"damage": 45, "miss_chance": 0.45, "description": "Mag-unleash ng isang malupit na mic attack."},
            "Kick ng Beat": {"damage": 26, "miss_chance": 0.35, "description": "Kick ang kalaban alinsunod sa beat para sa katamtamang pinsala."}
        }
        if is_enemy:
            self._boost_skills()
