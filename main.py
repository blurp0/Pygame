import pygame
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS  # Set by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

import random
from settings import *
from rooster import ManokNaPuti, ManokNaPula, ManokNaItim, ManokNaBalbon, ChickenNiGlock9
from ui import (
    draw_menu,
    draw_level_select,
    draw_rooster_skills_panel,
    draw_roster,
    draw_health_bar,
    draw_button,
    draw_skill_description_box,
    draw_text,
    draw_dialog_box,
    draw_bag_overlay,
    draw_post_win_buttons,
    draw_shop_confirmation
)
zoom_factor = 0.95
scaled_bg_width = int(WIDTH * zoom_factor)
scaled_bg_height = int(HEIGHT * zoom_factor)
# Load battle background once
battle_bg_path = resource_path("assets/GrassyField.png")
battle_bg = pygame.image.load(battle_bg_path).convert()
battle_bg = pygame.transform.scale(battle_bg, (scaled_bg_width, scaled_bg_height))
bg_rect = pygame.Rect(-40, 150, scaled_bg_width, scaled_bg_height)

# Initialize game states and data
all_roosters = {
    "Manok na Puti": ManokNaPuti(),
    "Manok na Pula": ManokNaPula(),
    "Manok na Itim": ManokNaItim(),
    "Manok na Balbon": ManokNaBalbon(),
    "Chicken Ni Glock9": ChickenNiGlock9()
}

unlocked_roosters = ["Manok na Puti"]
selected_rooster_name = "Manok na Puti"
inventory = {"Maliit na Potion": 2, "Malaking Potion": 1}


# Core game state
game_state = "menu"
dialog_state = "menu"
fight_mode = False
message = ""
game_over = False
surrender_time = None
selected_item = None
pending_enemy_attack = False
enemy_attack_start_time = None
next_level_btn = None
main_menu_btn = None
current_level = 1
reward_given = False
confirm_purchase = False
item_to_buy = None


# Track progression and rewards
highest_level_unlocked = 1
money = 0
beaten_levels = set()
beaten_counts = {}
shop_items = {"Maliit na Potion": 10, "Malaking Potion": 25}
shop_buttons = []
shop_back_btn = None
selected_skill = None

# Level select transition
def enter_level_select():
    global game_state
    game_state = "level_select"

def draw_shop(screen, items, width, height):
    y = 100
    title = "Tindahan - I-click para Bumili"
    title_surface = font.render(title, True, BLACK)
    title_x = (width - title_surface.get_width()) // 2
    screen.blit(title_surface, (title_x, 50))

    buttons = []
    for name, price in items.items():
        btn = draw_button(screen, f"{name} - {price} coins", width // 2 - 120, y, 240, 40)
        buttons.append((btn, name))
        y += 60

    back_btn = draw_button(screen, "Bumalik", width // 2 - 100, y + 20, 200, 40)
    return buttons, back_btn


def reset_game(level=1):
    global player, enemy, current_turn, game_over, message, dialog_state, fight_mode
    global selected_item, surrender_time, pending_enemy_attack, enemy_attack_start_time, current_level
    global reward_given

    current_level = level

    # Initialize player based on selection
    if selected_rooster_name == "Manok na Puti":
        player = ManokNaPuti(150, 300, is_enemy=False)
    elif selected_rooster_name == "Manok na Pula":
        player = ManokNaPula(150, 300, is_enemy=False)
    elif selected_rooster_name == "Manok na Itim":
        player = ManokNaItim(150, 300, is_enemy=False)
    elif selected_rooster_name == "Manok na Balbon":
        player = ManokNaBalbon(150, 300, is_enemy=False)
    else:
        selected_rooster_name == "Chicken Ni Glock9"
        player = ChickenNiGlock9(150, 300, is_enemy=False)
    # Assign enemy based on level
    if level == 1:
        enemy = ManokNaPuti(540, 70, is_enemy=True)
    elif level == 2:
        enemy = ManokNaPula(540, 70, is_enemy=True)
    elif level == 3:
        enemy = ManokNaItim(540, 70, is_enemy=True)
    elif level == 4:
        enemy  = ManokNaBalbon(540, 70, is_enemy=True)
    else:
        enemy = ChickenNiGlock9(540, 70, is_enemy=True)

    current_turn = "player"
    game_over = False
    dialog_state = "menu"
    fight_mode = True
    selected_item = None
    surrender_time = None
    pending_enemy_attack = False
    enemy_attack_start_time = None
    reward_given = False
    message = "Ano ang gagawin mo?"

# Start at the highest unlocked level
reset_game(highest_level_unlocked)

# Main loop
clock = pygame.time.Clock()
running = True

# Global button variables
start_btn = roster_btn = shop_btn = exit_btn = None
level_buttons = []
level_back_btn = None
buttons = []
back_btn = None
dialog_buttons = []
bag_buttons = []
shop_buttons = []
shop_back_btn = None
retry_btn = None



# Main game loop
while running:
    screen.fill(PASTEL_GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MENU
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn and start_btn.collidepoint(event.pos):
                    enter_level_select()
                elif shop_btn and shop_btn.collidepoint(event.pos):
                    game_state = "shop"
                elif roster_btn and roster_btn.collidepoint(event.pos):
                    game_state = "roster"
                elif exit_btn and exit_btn.collidepoint(event.pos):
                    running = False

        # LEVEL SELECT
        elif game_state == "level_select":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn, lvl in level_buttons:
                    if btn.collidepoint(event.pos) and lvl <= highest_level_unlocked:
                        reset_game(lvl)
                        game_state = "game"
                if level_back_btn and level_back_btn.collidepoint(event.pos):
                    game_state = "menu"

        # SHOP
        elif game_state == "shop":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirm_purchase:
                    yes_rect = pygame.Rect(WIDTH//2 - 70, HEIGHT//2 + 20, 60, 30)
                    no_rect = pygame.Rect(WIDTH//2 + 10, HEIGHT//2 + 20, 60, 30)

                    if yes_rect.collidepoint(event.pos):
                        cost = shop_items[item_to_buy]
                        if money >= cost:
                            inventory[item_to_buy] = inventory.get(item_to_buy, 0) + 1
                            money -= cost
                            message = "Matagumpay na Nabili ang Item"
                        else:
                            message = "Nabigo ang Pagbili ng Item, Kulang ang Pera"
                        confirm_purchase = False
                        item_to_buy = None

                    elif no_rect.collidepoint(event.pos):
                        confirm_purchase = False
                        item_to_buy = None
                        message = "Kinansela ang Pagbili"
                else:
                    for btn_rect, item_name in shop_buttons:
                        if btn_rect.collidepoint(event.pos):
                            confirm_purchase = True
                            item_to_buy = item_name
                            message = f"Are you sure you want to purchase {item_name}?"

                    if shop_back_btn and shop_back_btn.collidepoint(event.pos):
                        game_state = "menu"

        # ROSTER
        elif game_state == "roster":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn_rect, name in buttons:
                    if btn_rect.collidepoint(event.pos):
                        selected_rooster_name = name
                        selected_skill = None  # Reset selected skill when a new rooster is selected

                if back_btn and back_btn.collidepoint(event.pos):
                    game_state = "menu"

        # GAME
        elif game_state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and not (dialog_state == "waiting" or current_turn == "enemy"):
                    if dialog_state == "bag":
                        for btn_rect, label in bag_buttons:
                            if btn_rect.collidepoint(event.pos):
                                if label in inventory:
                                    selected_item = label
                                elif label == "Use" and selected_item:
                                    if selected_item == "Maliit na Potion":
                                        player.health += 20
                                    elif selected_item == "Large Potion":
                                        player.health += 50
                                    inventory[selected_item] -= 1
                                    player.health = min(player.health, player.max_health)
                                    message = f"Ginamit mo ang {selected_item}!"
                                    selected_item = None
                                    dialog_state = "waiting"
                                    enemy_attack_start_time = pygame.time.get_ticks()
                                    pending_enemy_attack = True
                                    current_turn = "enemy"
                                elif label == "Cancel":
                                    selected_item = None
                                    dialog_state = "menu"
                                    message = "Ano ang gagawin mo?"

                    elif dialog_state == "attack":
                        for btn_rect, label in dialog_buttons:
                            if btn_rect.collidepoint(event.pos):
                                if label in player.skills:
                                    dmg = player.attack(enemy, label)
                                    if dmg == 0:
                                        message = f"Nagmiss ang {label} Hindi tumama ang atake."
                                    else:
                                        enemy.health = max(enemy.health - dmg, 0)
                                        message = f"Ginamit mo ang {label}! Nakatanggap ng {dmg}  pinsala ang kaaway."

                                    dialog_state = "waiting"
                                    enemy_attack_start_time = pygame.time.get_ticks()
                                    pending_enemy_attack = True
                                    current_turn = "enemy"
                                    break

                                elif label == "Cancel":
                                    dialog_state = "menu"
                                    message = "Ano ang gagawin mo?"
                                    break

                    elif dialog_state == "confirm_surrender":
                        for btn_rect, label in dialog_buttons:
                            if btn_rect.collidepoint(event.pos):
                                if label == "Yes":
                                    message = "Sumuko ka!"
                                    game_over = True
                                    surrender_time = pygame.time.get_ticks()
                                    dialog_state = "menu"
                                elif label == "No":
                                    dialog_state = "menu"
                                    message = "Ano ang gagawin mo?"

                    else:
                        for btn_rect, label in dialog_buttons:
                            if btn_rect.collidepoint(event.pos):
                                if label == "Laban":
                                    dialog_state = "attack"
                                    fight_mode = True
                                elif label == "Bag":
                                    dialog_state = "bag"
                                elif label == "Sumuko":
                                    dialog_state = "confirm_surrender"
                                    message = "Sigurado ka bang gusto mong sumuko?"
                                elif label == "Cancel":
                                    dialog_state = "menu"
                                    break

                else:
                    if next_level_btn and next_level_btn.collidepoint(event.pos):
                        reset_game(current_level + 1)
                    elif main_menu_btn and main_menu_btn.collidepoint(event.pos):
                        game_state = "menu"
                    elif retry_btn and retry_btn.collidepoint(event.pos):
                        reset_game(current_level)
                        game_state = "game"  # Ensure the state resets to "game"

    # DRAWING
    if game_state == "menu":
        start_btn, roster_btn, shop_btn, exit_btn = draw_menu(screen, WIDTH)
    elif game_state == "level_select":
        level_buttons, level_back_btn = draw_level_select(screen, highest_level_unlocked)
    elif game_state == "shop":
        shop_buttons, shop_back_btn = draw_shop(screen, shop_items, WIDTH, HEIGHT)
        if confirm_purchase:
            draw_shop_confirmation(screen, message, WIDTH, HEIGHT)
    elif game_state == "roster":
        buttons, back_btn = draw_roster(screen, unlocked_roosters, all_roosters, selected_rooster_name, WIDTH, HEIGHT)

        # Retrieve the selected rooster object from all_roosters
        selected_rooster = all_roosters[selected_rooster_name]

        # Draw the rooster's skills panel
        skill_buttons = draw_rooster_skills_panel(screen, selected_rooster.skills, selected_skill, WIDTH, HEIGHT)

        # Draw the skill description box
        draw_skill_description_box(screen, selected_skill, selected_rooster.skills, WIDTH, HEIGHT)

        # Handle skill selection
        for btn, skill in skill_buttons:
            if btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                selected_skill = skill  # Update selected skill on click (directly assign skill as it is the name)

    elif game_state == "game":
        screen.blit(battle_bg, (0, 0), bg_rect)
        player.draw(screen)
        enemy.draw(screen)
        draw_health_bar(screen, player, 100, 240)
        draw_health_bar(screen, enemy, 300, 30)

        # Enemy attack delay
        if not game_over and current_turn == "enemy" and pending_enemy_attack:
            if pygame.time.get_ticks() - enemy_attack_start_time >= 2000:
                skill = random.choice(list(enemy.skills.keys()))
                dmg = enemy.attack(player, skill)

                # Check if the damage is zero and update the message accordingly
                if dmg == 0:
                    message = f"Enemy ginamit ang {skill}, pero hindi tumama ang atake!"
                else:
                    # Ensure the player's health doesn't go below 0
                    player.health = max(player.health - dmg, 0)  # Prevent player health from going below 0
                    message = f"Ginamit ng kaaway ang {skill}! Nakakuha ka ng {dmg} na pinsala."
                
                current_turn = "player"
                pending_enemy_attack = False
                dialog_state = "menu"
                fight_mode = True

        # WIN/LOSS & REWARD
        if player.health <= 0:
            message = "Tinalo ka"
            game_over = True
            reward_given = True  # Prevent reward when the player loses

        elif enemy.health <= 0:
            if not reward_given:  # Ensure reward is given only once
                unlocked_name = enemy.name

                # Coin reward logic: full on 1st clear, 30% on 2nd, none thereafter
                base_reward = current_level * 10
                count = beaten_counts.get(current_level, 0) + 1
                beaten_counts[current_level] = count

                if count == 1:
                    reward = base_reward
                elif count == 2:
                    reward = int(base_reward * 0.3)
                else:
                    reward = 0

                if count <= 2:
                    money += reward

                # Unlock and notify
                if unlocked_name not in unlocked_roosters:
                    unlocked_roosters.append(unlocked_name)
                    message = f"Nanalo ka! Na-unlock ang {unlocked_name} at nakakuha ng {reward} coins!"
                else:
                    message = f"Nanalo ka! Nakakuha ka ng {reward} coins!"

                highest_level_unlocked = max(highest_level_unlocked, current_level + 1)
                reward_given = True  # ✅ Prevent Multiple Rewards

            game_over = True


        # Draw buttons for WIN/LOSS state
        if game_over:
            if "nanalo" in message.lower():
                # Show next level or main menu buttons when the player wins
                next_level_btn, main_menu_btn = draw_post_win_buttons(screen, WIDTH, HEIGHT, game_over=True, victory=True)
                retry_btn = None
            elif "sumuko" in message.lower():
                # Immediately go to the main menu without displaying anything
                game_over = True
                reward_given = True  # Ensure no rewards are given on surrender
                highest_level_unlocked = max(highest_level_unlocked, current_level)
                pygame.time.wait(1000)
                game_state = "menu" # Make sure the level progress is not lost
                # No buttons or messages, just transition to the menu

            else:
                # Show Retry and Main Menu buttons on Loss
                retry_btn, main_menu_btn = draw_post_win_buttons(screen, WIDTH, HEIGHT, game_over=True, victory=False)
                next_level_btn = None

        # Drawing the dialog box
        dialog_buttons = draw_dialog_box(
            screen, fight_mode, list(player.skills.keys()),
            message, inventory, dialog_state, selected_item
        )

        # Drawing the bag overlay when the player is in "bag" state
        bag_buttons = (
            draw_bag_overlay(screen, inventory, selected_item)
            if dialog_state == "bag" else []
        )

        # Handling surrender logic
        if game_over and message.startswith("You surrendered!") and surrender_time:
            if pygame.time.get_ticks() - surrender_time >= 1500:
                game_state = "menu"
                surrender_time = None


    # Display money
    if game_state == "menu" or (game_state == "game" and game_over):
        draw_text(screen, f"Pera: {money}", 10, 10)

    elif game_state == "shop":  # Assuming you have a "shop" state for the shop screen
        draw_text(screen, f"Pera: {money}", 10, 10)
        # Add other shop-related UI elements here (items, buttons, etc.)


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
