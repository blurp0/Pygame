import pygame
import sys
import os
import random
from settings import font, WHITE


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.mixer.init()
attack_sound_path = resource_path("assets/audio/attack.wav")
attack_sound = pygame.mixer.Sound(attack_sound_path)

class Rooster:

    image_cache = {} 

    def __init__(self, name, color, x=0, y=0, is_enemy=False, max_health=100, boost_if_new=True):
        self.name = name
        self.color = color
        self.is_enemy = is_enemy
        self.max_health = max_health
        self.health = self.max_health

        self.skills = {
            "Tuka": {"damage": 20, "miss_chance": 0.1, "cooldown": 1, "cooldown_counter": 0, "description": "Isang mabilis na pag-atake gamit ang tuka."},
            "Kalkal": {"damage": 23, "miss_chance": 0.2, "cooldown": 2, "cooldown_counter": 0, "description": "Isang matalim na kalkal gamit ang mga pangil."},
            "Sugod": {"damage": 35, "miss_chance": 0.4, "cooldown": 3, "cooldown_counter": 0, "description": "Mag-sugod sa kalaban."},
            "Palo ng Pakpak": {"damage": 28, "miss_chance": 0.25, "cooldown": 1, "cooldown_counter": 0, "description": "Palo ng pakpak upang magdulot ng malalakas na hangin."}
        }

        self.skill_cooldowns = {skill: 0 for skill in self.skills}

        self.current_skill_used = None

        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y

        base_name = name.lower().replace(' ', '_')
        role = "enemy" if self.is_enemy else "player"
        filename = f"{base_name}_{role}.png"
        image_path = f"assets/{filename}"

        try:
            self.image = pygame.image.load(resource_path(image_path)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (250, 250))
            self.use_image = True
            Rooster.image_cache[f"{base_name}_{role}"] = self.image
            print(f"load image {self.image}")
        except Exception as e:
            print(f"Failed to load image {image_path}: {e}")
            self.rect = pygame.Rect(x, y, 80, 80)
            self.use_image = False

        # Attack animation setup
        self.attack_animation_frame = 0
        self.attack_animation_active = False
        self.attack_frames = [pygame.Surface((100, 100)) for _ in range(5)]  # Placeholder frames
        self.attack_animation_speed = 1.5

        # Track if the player is charging the attack
        self.is_charging_attack = False
        self.attack_target_x = 0
        self.attack_target_y = 0

    def _boost_skills(self):
        for key in self.skills:
            skill = self.skills[key]
            skill["damage"] = int(skill["damage"] * 1)

        # Boost HP as well
        self.max_health = int(self.max_health * 1.1)
        self.health = self.max_health  # Heal up to new max


    def draw(self, surface, target=None):
        if target is not None:
            # Determine who should be drawn first based on who is attacking
            if self.attack_animation_active:
                # This rooster is attacking, so draw the target first, then self
                target._draw_base(surface)
                self._animate_attack(surface, target)
            elif target.attack_animation_active:
                # Target is attacking, so draw self first, then let target animate over
                self._draw_base(surface)
            else:
                # No attack in progress, draw normally based on role
                if self.is_enemy:
                    self._draw_base(surface)
                    target._draw_base(surface)
                else:
                    target._draw_base(surface)
                    self._draw_base(surface)
        else:
            # No target provided, just draw this rooster normally
            self._draw_base(surface)

    def _draw_base(self, surface):
        """Helper to draw the sprite normally, without animation."""
        if self.use_image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)


    def reduce_cooldowns(self):
        for skill_name, skill in self.skills.items():
            if skill["cooldown_counter"] > 0:
                skill["cooldown_counter"] -= 1

    def can_use_skill(self, skill_name):
        return skill_name in self.skills and self.skills[skill_name]["cooldown_counter"] == 0

    def attack(self, target, skill_name):
        if skill_name not in self.skills:
            return 0

        skill = self.skills[skill_name]

        if skill["cooldown_counter"] > 0:
            print(f"{skill_name} is on cooldown for {skill['cooldown_counter']} more turn(s).")
            return 0

        damage = skill["damage"]
        miss_chance = skill["miss_chance"]

        if self.is_enemy:
            miss_chance *= 0.5

        skill["cooldown_counter"] = skill["cooldown"]  # Start cooldown regardless

        if random.random() < miss_chance:
            print(f"{self.name}'s {skill_name} missed!")
            return 0  # Return 0 when attack misses, not None
        attack_sound.play()
        # Trigger attack animation
        self.attack_animation_active = True
        self.attack_animation_frame = 0  # Reset animation frame

        # Track the target position for charging the attack
        self.is_charging_attack = True
        self.attack_target_x = target.x
        self.attack_target_y = target.y
        self.current_skill_used = skill_name

        print(f"{self.name} used {skill_name} and hit for {damage}!")
        return damage  # Ensure damage is returned when attack hits


    def _animate_attack(self, surface, target):
        if target is None:
            return  # Exit if no target is provided

        # Reset animation frame when attack starts
        if self.is_charging_attack and self.attack_animation_frame == 0:
            self.attack_animation_frame = 0

        # Update the attack animation frame
        self.attack_animation_frame += 1
        if self.attack_animation_frame >= len(self.attack_frames) * self.attack_animation_speed:
            self.attack_animation_active = False  # Stop animation after full cycle
            self.is_charging_attack = False  # End charging

            # Apply damage after animation ends
            if self.current_skill_used:
                target.health -= self.skills[self.current_skill_used]["damage"]
                print(f"{self.name} applied {self.skills[self.current_skill_used]['damage']} damage to {target.name} using {self.current_skill_used}")
                self.current_skill_used = None  # Reset after applying


        # Attack moves only during the animation
        if self.attack_animation_active:
            # Calculate the direction towards the target (x, y)
            direction_x = target.x - self.x
            direction_y = target.y - self.y
            distance = max(1, (direction_x**2 + direction_y**2) ** 0.5)  # Prevent division by 0

            # Normalize direction
            direction_x /= distance
            direction_y /= distance

            overshoot_factor = 1.2  

            # Increase movement distance for a more extended attack
            move_speed = 30  # Increased speed for a more noticeable movement
            movement_distance = self.attack_animation_frame // self.attack_animation_speed
            move_x = self.x + direction_x * movement_distance * move_speed * overshoot_factor
            move_y = self.y + direction_y * movement_distance * move_speed * overshoot_factor

            # Update the sprite's position
            self.x = move_x
            self.y = move_y

        # Draw the updated sprite (player or enemy) to simulate the attack animation
        surface.blit(self.image, (self.x, self.y))

        # Reset position after attack if the animation is inactive
        if not self.attack_animation_active:
            self.x = self.original_x  # Reset to original X position
            self.y = self.original_y  # Reset to original Y position


# Subclasses — enemy boost handled automatically
class ManokNaPuti(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False, boost_if_new=True):
        super().__init__("Manok na Puti", (255, 255, 255), x, y, is_enemy, max_health=130)
        self.skills = {
            "Tuka": {
                "damage": 20,
                "miss_chance": 0.1,
                "description": "Isang mabilis at matalim na tuka na kayang tumama sa kalaban bago ito makaiwas.",
                "cooldown": 1,
                "cooldown_counter": 0
            },
            "Kalkal": {
                "damage": 23,
                "miss_chance": 0.2,
                "description": "Isang mabagsik na kalkal gamit ang mga kuko para magdulot ng matinding galos.",
                "cooldown": 1,
                "cooldown_counter": 0
            },
            "Sugod": {
                "damage": 35,
                "miss_chance": 0.3,
                "description": "Isang mabangis na pagsugod gamit ang buong lakas ng katawan upang pabagsakin ang kalaban.",
                "cooldown": 3,
                "cooldown_counter": 0
            },
            "Palo ng Pakpak": {
                "damage": 28,
                "miss_chance": 0.25,
                "description": "Malakas na hampas ng pakpak na maaaring magpatilapon sa kalaban.",
                "cooldown": 2,
                "cooldown_counter": 0
            }
        }


class ManokNaPula(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False, boost_if_new=True):
        super().__init__("Manok na Pula", (255, 0, 0), x, y, is_enemy, max_health=140)
        self.skills = {
            "Tuka": {
                "damage": 20,
                "miss_chance": 0.1,
                "description": "Isang mabilis at malakas na tuka na kayang tumagos sa panangga ng kalaban.",
                "cooldown": 1,
                "cooldown_counter": 0
            },
            "Kalkal": {
                "damage": 23,
                "miss_chance": 0.2,
                "description": "Isang mabangis na kalkal gamit ang matutulis na kuko para magdulot ng matinding pinsala.",
                "cooldown": 1,
                "cooldown_counter": 0
            },
            "Galit": {
                "damage": 40,
                "miss_chance": 0.25,
                "description": "Isang ligaw at walang habas na atake dulot ng matinding galit.",
                "cooldown": 3,
                "cooldown_counter": 0
            },
            "Tuka ng Apoy": {
                "damage": 35,
                "miss_chance": 0.25,
                "description": "Isang mainit at naglalagablab na tuka na parang apoy ang bawat tama.",
                "cooldown": 2,
                "cooldown_counter": 0
            }
        }


class ManokNaItim(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False, boost_if_new=True):
        super().__init__("Manok na Itim", (30, 30, 30), x, y, is_enemy, max_health=150)
        self.skills = {
            "Madilim na Tuka": {
                "damage": 25,
                "miss_chance": 0.1,
                "description": "Isang malamig at tahimik na tuka na tila galing sa dilim.",
                "cooldown": 1,
                "cooldown_counter": 0
            },
            "Anino ng Pangil": {
                "damage": 30,
                "miss_chance": 0.25,
                "description": "Isang mabilis na atake mula sa anino na parang may matutulis na pangil.",
                "cooldown": 2,
                "cooldown_counter": 0
            },
            "Kadiliman": {
                "damage": 40,
                "miss_chance": 0.25,
                "description": "Isang malupit na atakeng bumabalot sa kalaban sa purong kadiliman.",
                "cooldown": 3,
                "cooldown_counter": 0
            },
            "Pakpak ng Multo": {
                "damage": 28,
                "miss_chance": 0.2,
                "description": "Isang nakakakilabot na hampas gamit ang pakpak na tila sinasaniban ng espiritu.",
                "cooldown": 1,
                "cooldown_counter": 0
            }
        }


class ManokNaBalbon(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False, boost_if_new=True):
        super().__init__("Manok na Balbon", (50, 25, 25), x, y, is_enemy, max_health=160)
        self.skills = {
            "Matingkad na Sipang": {
                "damage": 25,
                "miss_chance": 0.1,
                "description": "Isang malakas at biglaang sipa na kayang magpabuwal sa kalaban.",
                "cooldown": 1,
                "cooldown_counter": 0
            },
            "Bagyong Balahibo": {
                "damage": 30,
                "miss_chance": 0.25,
                "description": "Isang masidhing pag-atake na parang bagyo ng lumilipad na balahibo.",
                "cooldown": 2,
                "cooldown_counter": 0
            },
            "Bomba ng Balahibo": {
                "damage": 45,
                "miss_chance": 0.25,
                "description": "Isang matinding pagsabog ng balahibo na tumatama sa maraming bahagi ng katawan ng kalaban.",
                "cooldown": 3,
                "cooldown_counter": 0
            },
            "Pagbuga ng Hayop": {
                "damage": 28,
                "miss_chance": 0.2,
                "description": "Isang mabangis na bugang parang halakhak ng isang galit na hayop.",
                "cooldown": 1,
                "cooldown_counter": 0
            }
        }


class ChickenNiGlock9(Rooster):
    def __init__(self, x=0, y=0, is_enemy=False,boost_if_new=True):
        super().__init__("Chicken Ni Glock9", (80, 10, 150), x, y, is_enemy, max_health=170)
        self.skills = {
            "Rap Sapantaha": {
                "damage": 30,
                "miss_chance": 0.1,
                "description": "Isang mabilis at malupit na slap na may kasamang rap flow.",
                "cooldown": 1,
                "cooldown_counter": 0
            },
            "Pagbagsak ng Bar": {
                "damage": 40,
                "miss_chance": 0.25,
                "description": "Isang mabigat na drop ng bar na tumatama nang malakas sa kalaban.",
                "cooldown": 2,
                "cooldown_counter": 0
            },
            "Mic Pagputok": {
                "damage": 50,
                "miss_chance": 0.25,
                "description": "Isang pagsabog ng mic na may kasamang malalakas na tunog na nagdudulot ng pinsala.",
                "cooldown": 3,
                "cooldown_counter": 0
            },
            "Kick ng Beat": {
                "damage": 35,
                "miss_chance": 0.2,
                "description": "Isang malakas na kick na tumutok sa beat ng musika, sinasabay sa galaw ng kalaban.",
                "cooldown": 1,
                "cooldown_counter": 0
            }
        }

