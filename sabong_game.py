import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sabong - Full Game")

# Fonts and colors
font = pygame.font.SysFont(None, 36)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)

# Rooster class
class Rooster:
    def __init__(self, name, color, x=0, y=0):
        self.name = name
        self.color = color
        self.health = 100
        self.skills = {
            "Peck": 10,
            "Scratch": 15,
            "Charge": 20,
            "Dodge": 0
        }
        self.rect = pygame.Rect(x, y, 80, 80)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        name_text = font.render(self.name, True, WHITE)
        surface.blit(name_text, (self.rect.x, self.rect.y - 30))

    def attack(self, target, skill):
        damage = self.skills[skill]
        target.health -= damage
        return damage

# Globals
all_roosters = {
    "White": Rooster("White", WHITE),
    "Red": Rooster("Red", RED)
}
unlocked_roosters = ["White"]
selected_rooster_name = "White"

# Game states
game_state = "menu"
dialog_state = "menu"
fight_mode = False


def reset_game():
    global player, enemy, current_turn, game_over, message, dialog_state, fight_mode
    player = Rooster(selected_rooster_name, all_roosters[selected_rooster_name].color, 100, 400)
    enemy = Rooster("Red", RED, 600, 100)
    current_turn = "player"
    game_over = False
    message = ""
    dialog_state = "menu"
    fight_mode = False

reset_game()

def draw_button(text, x, y, width, height, color=GRAY):
    btn_rect = pygame.Rect(x, y, width, height)
    mouse_pos = pygame.mouse.get_pos()
    if btn_rect.collidepoint(mouse_pos):
        color = tuple(max(c - 30, 0) for c in color)
    pygame.draw.rect(screen, color, btn_rect)
    pygame.draw.rect(screen, BLACK, btn_rect, 2)
    label = render_fitting_text(text, width, height)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
    return btn_rect

def draw_text(text, x, y):
    label = font.render(text, True, BLACK)
    screen.blit(label, (x, y))

def draw_health_bar(rooster, x, y):
    pygame.draw.rect(screen, RED, (x, y, 100, 10))
    pygame.draw.rect(screen, GREEN, (x, y, max(rooster.health, 0), 10))

def render_fitting_text(text, max_width, max_height):
    size = 36
    while size > 10:
        temp_font = pygame.font.SysFont(None, size)
        rendered = temp_font.render(text, True, BLACK)
        if rendered.get_width() <= max_width - 10 and rendered.get_height() <= max_height - 10:
            return rendered
        size -= 1
    return font.render(text, True, BLACK)

def draw_dialog_box(in_fight_mode=False, moves=None):
    buttons = []
    dialog_rect = pygame.Rect(30, 400, 740, 170)
    pygame.draw.rect(screen, WHITE, dialog_rect)
    pygame.draw.rect(screen, BLACK, dialog_rect, 3)
    pygame.draw.line(screen, BLACK, (470, 410), (470, 560), 2)

    if in_fight_mode and moves:
        for i, label in enumerate(moves[:4]):
            row = i // 2
            col = i % 2
            x = 50 + col * 180
            y = 430 + row * 50
            btn_rect = pygame.Rect(x, y, 160, 40)
            btn_color = GRAY
            if btn_rect.collidepoint(pygame.mouse.get_pos()):
                btn_color = tuple(max(c - 30, 0) for c in btn_color)
            pygame.draw.rect(screen, btn_color, btn_rect)
            pygame.draw.rect(screen, BLACK, btn_rect, 2)
            text = render_fitting_text(label, btn_rect.width, btn_rect.height)
            screen.blit(text, (btn_rect.x + (btn_rect.width - text.get_width()) // 2,
                            btn_rect.y + (btn_rect.height - text.get_height()) // 2))
            buttons.append((btn_rect, label))

        cancel_rect = pygame.Rect(490, 480, 220, 40)
        cancel_color = (255, 182, 193)
        if cancel_rect.collidepoint(pygame.mouse.get_pos()):
            cancel_color = tuple(max(c - 30, 0) for c in cancel_color)
        pygame.draw.rect(screen, cancel_color, cancel_rect)
        pygame.draw.rect(screen, BLACK, cancel_rect, 2)
        cancel_text = render_fitting_text("Cancel", cancel_rect.width, cancel_rect.height)
        screen.blit(cancel_text, (cancel_rect.x + (cancel_rect.width - cancel_text.get_width()) // 2,
                                  cancel_rect.y + (cancel_rect.height - cancel_text.get_height()) // 2))
        buttons.append((cancel_rect, "Cancel"))

    else:
        if dialog_state == "bag":
            y_offset = 430
            for i, (item, count) in enumerate(inventory.items()):
                btn_rect = pygame.Rect(490, y_offset + i * 50, 220, 40)
                pygame.draw.rect(screen, (240, 230, 140), btn_rect)
                pygame.draw.rect(screen, BLACK, btn_rect, 2)
                item_text = font.render(f"{item} x{count}", True, BLACK)
                screen.blit(item_text, (btn_rect.x + 10, btn_rect.y + 5))
                buttons.append((btn_rect, item))
            cancel_rect = pygame.Rect(490, y_offset + len(inventory) * 50, 220, 40)
            pygame.draw.rect(screen, (255, 182, 193), cancel_rect)
            pygame.draw.rect(screen, BLACK, cancel_rect, 2)
            cancel_text = font.render("Cancel", True, BLACK)
            screen.blit(cancel_text, (cancel_rect.x + 60, cancel_rect.y + 5))
            buttons.append((cancel_rect, "Cancel"))
        else:
            def wrap_text(text, font, max_width):
                words = text.split()
                lines = []
                current_line = ""
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if font.size(test_line)[0] <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
                return lines

            wrapped_lines = wrap_text(message, font, 400)
            for i, line in enumerate(wrapped_lines[:4]):
                dialog_text = font.render(line, True, BLACK)
                screen.blit(dialog_text, (50, 420 + i * 30))

            top_labels = ["Fight", "Bag"]
            button_colors = {
                "Fight": (255, 105, 97),
                "Bag": (218, 165, 32),
                "Surrender": (135, 206, 250),
            }

            for i, label in enumerate(top_labels):
                x = 490 + i * 125
                y = 430
                btn_rect = pygame.Rect(x, y, 110, 40)
                btn_color = button_colors[label]
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    btn_color = tuple(max(c - 30, 0) for c in btn_color)
                pygame.draw.rect(screen, btn_color, btn_rect)
                pygame.draw.rect(screen, BLACK, btn_rect, 2)
                text = render_fitting_text(label, btn_rect.width, btn_rect.height)
                screen.blit(text, (btn_rect.x + (btn_rect.width - text.get_width()) // 2,
                                btn_rect.y + (btn_rect.height - text.get_height()) // 2))
                buttons.append((btn_rect, label))

                surr_rect = pygame.Rect(490, 480, 250, 40)
                surr_color = button_colors["Surrender"]
                if surr_rect.collidepoint(pygame.mouse.get_pos()):
                    surr_color = tuple(max(c - 30, 0) for c in surr_color)
                pygame.draw.rect(screen, surr_color, surr_rect)
                pygame.draw.rect(screen, BLACK, surr_rect, 2)
                surr_text = render_fitting_text("Surrender", surr_rect.width, surr_rect.height)
                screen.blit(surr_text, (surr_rect.x + (surr_rect.width - surr_text.get_width()) // 2,
                                        surr_rect.y + (surr_rect.height - surr_text.get_height()) // 2))
                buttons.append((surr_rect, "Surrender"))

    return buttons

def draw_menu():
    title = font.render("Sabong Main Menu", True, WHITE)
    screen.blit(title, (WIDTH // 2 - 120, 100))
    start_btn = draw_button("Start Game", WIDTH // 2 - 100, 200, 200, 40)
    roster_btn = draw_button("Roster", WIDTH // 2 - 100, 260, 200, 40)
    exit_btn = draw_button("Exit", WIDTH // 2 - 100, 320, 200, 40)
    return start_btn, roster_btn, exit_btn

def draw_roster():
    draw_text("Unlocked Roosters", 50, 50)
    buttons = []
    for i, name in enumerate(unlocked_roosters):
        rooster = all_roosters[name]
        btn_rect = pygame.Rect(50, 100 + i * 60, 200, 40)
        pygame.draw.rect(screen, rooster.color, btn_rect)
        draw_text(name + (" (Selected)" if name == selected_rooster_name else ""), 60, 110 + i * 60)
        buttons.append((btn_rect, name))
    back_btn = draw_button("Back", WIDTH - 150, HEIGHT - 60, 100, 40)
    return buttons, back_btn

inventory = {
    "Small Potion": 2,
    "Large Potion": 1
}

# Main loop
clock = pygame.time.Clock()
running = True
message = ""
last_state = None

while running:
    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    reset_game()
                    game_state = "game"
                elif roster_btn.collidepoint(event.pos):
                    game_state = "roster"
                elif exit_btn.collidepoint(event.pos):
                    running = False

        elif game_state == "roster":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn_rect, name in buttons:
                    if btn_rect.collidepoint(event.pos):
                        selected_rooster_name = name
                if back_btn.collidepoint(event.pos):
                    game_state = "menu"

        elif game_state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fight_mode:
                    fight_buttons = draw_dialog_box(in_fight_mode=True, moves=list(player.skills.keys()))
                    for btn, label in fight_buttons:
                        if btn.collidepoint(event.pos):
                            if label == "Cancel":
                                fight_mode = False
                            elif label in player.skills and current_turn == "player" and not game_over:
                                dmg = player.attack(enemy, label)
                                message = f"You used {label}! Enemy took {dmg} damage."
                                current_turn = "enemy"
                                fight_mode = False
                            break
                else:
                    action_buttons = draw_dialog_box()
                    for btn, label in action_buttons:
                        if btn.collidepoint(event.pos):
                            if dialog_state == "bag":
                                if label == "Small Potion" and inventory[label] > 0:
                                    player.health = min(player.health + 20, 100)
                                    inventory[label] -= 1
                                    message = "You used Small Potion! Healed 20 HP."
                                    dialog_state = "menu"
                                    current_turn = "enemy"
                                elif label == "Large Potion" and inventory[label] > 0:
                                    player.health = min(player.health + 50, 100)
                                    inventory[label] -= 1
                                    message = "You used Large Potion! Healed 50 HP."
                                    dialog_state = "menu"
                                    current_turn = "enemy"
                                elif label == "Cancel":
                                    dialog_state = "menu"
                            else:
                                if label.lower() == "fight":
                                    fight_mode = True
                                elif label.lower() == "bag":
                                    dialog_state = "bag"
                                elif label.lower() == "surrender":
                                    message = "You surrendered!"
                                    game_over = True
                                    pygame.time.delay(1000)
                                    game_state = "menu"

    if game_state == "menu":
        start_btn, roster_btn, exit_btn = draw_menu()
    elif game_state == "roster":
        buttons, back_btn = draw_roster()
    elif game_state == "game":
        player.draw(screen)
        enemy.draw(screen)
        draw_health_bar(player, 100, 380)
        draw_health_bar(enemy, 600, 180)

        if not game_over and current_turn == "enemy":
            pygame.time.delay(800)
            skill = random.choice(list(enemy.skills.keys()))
            dmg = enemy.attack(player, skill)
            message = f"Enemy used {skill}! You took {dmg} damage."
            current_turn = "player"

        if player.health <= 0:
            message = "You lost!"
            game_over = True
        elif enemy.health <= 0 and "Red" not in unlocked_roosters:
            unlocked_roosters.append("Red")
            message = "You won! You unlocked Red rooster!"
            game_over = True

        if fight_mode:
            draw_dialog_box(in_fight_mode=True, moves=list(player.skills.keys()))
        else:
            draw_dialog_box()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
