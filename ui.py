import pygame
from settings import screen, WIDTH, HEIGHT, WHITE, BLACK, GRAY, font

# Helper to fit text within a box
def render_fitting_text(text, max_width, max_height, color=BLACK):
    size = 36
    while size > 10:
        temp_font = pygame.font.SysFont(None, size)
        rendered = temp_font.render(text, True, color)
        if rendered.get_width() <= max_width - 10 and rendered.get_height() <= max_height - 10:
            return rendered
        size -= 1
    return font.render(text, True, color)

# Basic button drawing with hover effect
def draw_button(screen, text, x, y, width, height, color=GRAY):
    btn_rect = pygame.Rect(x, y, width, height)
    mouse_pos = pygame.mouse.get_pos()
    if btn_rect.collidepoint(mouse_pos):
        color = tuple(max(c - 30, 0) for c in color)
    pygame.draw.rect(screen, color, btn_rect)
    pygame.draw.rect(screen, BLACK, btn_rect, 2)
    label = render_fitting_text(text, width, height)
    screen.blit(label, (x + (width - label.get_width()) // 2,
                        y + (height - label.get_height()) // 2))
    return btn_rect

# Simple text drawing
def draw_text(screen, text, x, y):
    label = font.render(text, True, BLACK)
    screen.blit(label, (x, y))

# Draw health bar for combat
def draw_health_bar(surface, rooster, x, y):
    pygame.draw.rect(surface, (255, 255, 255), (x, y, 100, 10))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, max(rooster.health, 0), 10))

# Main menu UI
def draw_menu(screen, width):
    title = font.render("Sabong Main Menu", True, WHITE)
    screen.blit(title, (width // 2 - 120, 100))

    start_btn = draw_button(screen, "Start Game", width // 2 - 100, 200, 200, 40)
    roster_btn = draw_button(screen, "Roster", width // 2 - 100, 260, 200, 40)
    shop_btn = draw_button(screen, "Shop", width // 2 - 100, 320, 200, 40)
    exit_btn = draw_button(screen, "Exit", width // 2 - 100, 380, 200, 40)

    return start_btn, roster_btn, shop_btn, exit_btn

# Shop UI
def draw_shop(screen, inventory, player_money, width, height):
    # Title
    title = font.render("Shop", True, WHITE)
    screen.blit(title, (width // 2 - 40, 50))

    # Item List (example items: healing potions)
    items = [("Small Potion", 20), ("Large Potion", 50), ("Revive Stone", 100)]
    buttons = []
    for i, (item_name, item_price) in enumerate(items):
        item_btn_rect = pygame.Rect(50, 120 + i * 60, 200, 40)
        pygame.draw.rect(screen, GRAY, item_btn_rect)
        pygame.draw.rect(screen, BLACK, item_btn_rect, 2)
        screen.blit(font.render(f"{item_name} - {item_price} Coins", True, BLACK), (item_btn_rect.x + 10, item_btn_rect.y + 10))
        buttons.append((item_btn_rect, item_name, item_price))

    # Player Money Display
    draw_text(screen, f"Coins: {player_money}", width - 150, 50)

    # Back Button
    back_btn = draw_button(screen, "Back", width - 150, height - 60, 100, 40)
    buttons.append((back_btn, "Back"))

    return buttons

# Level select UI: only levels up to highest_level are enabled
def draw_level_select(screen, highest_level, max_levels=5):
    # Title
    title = font.render("Select Level", True, WHITE)
    screen.blit(title, (WIDTH // 2 - 80, 50))

    buttons = []
    # Layout: spread buttons horizontally
    spacing = 80
    total_width = max_levels * spacing
    start_x = WIDTH // 2 - total_width // 2 + spacing//2
    y = 150
    for lvl in range(1, max_levels + 1):
        x = start_x + (lvl - 1) * spacing
        text = str(lvl)
        # Locked if above highest
        color = (50, 150, 250) if lvl <= highest_level else (100, 100, 100)
        btn = draw_button(screen, text, x, y, 60, 60, color)
        buttons.append((btn, lvl))

    # Back button
    back_btn = draw_button(screen, "Back", WIDTH // 2 - 50, y + 120, 100, 40)
    return buttons, back_btn

# Roster selection UI
def draw_roster(screen, unlocked_roosters, all_roosters, selected_rooster_name, width, height):
    draw_text(screen, "Unlocked Roosters", 50, 50)
    buttons = []
    for i, name in enumerate(unlocked_roosters):
        rooster = all_roosters[name]
        btn_rect = pygame.Rect(50, 100 + i * 60, 200, 40)
        pygame.draw.rect(screen, rooster.color, btn_rect)
        draw_text(screen, name + (" (Selected)" if name == selected_rooster_name else ""),
                  60, 110 + i * 60)
        buttons.append((btn_rect, name))
    back_btn = draw_button(screen, "Back", width - 150, height - 60, 100, 40)
    return buttons, back_btn

# Battle dialog box UI
def draw_dialog_box(screen, fight_mode, moves, message, inventory, dialog_state, selected_item=None):
    buttons = []
    dialog_rect = pygame.Rect(30, 400, 740, 170)
    pygame.draw.rect(screen, WHITE, dialog_rect)
    pygame.draw.rect(screen, BLACK, dialog_rect, 3)
    pygame.draw.line(screen, BLACK, (470, 410), (470, 560), 2)

    if fight_mode:
        if dialog_state == "attack":
            # Attack skill buttons
            for i, label in enumerate(moves[:4]):
                row, col = divmod(i, 2)
                x = 50 + col * 180
                y = 430 + row * 50
                btn_rect = pygame.Rect(x, y, 160, 40)
                color = GRAY
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    color = tuple(max(c - 30, 0) for c in color)
                pygame.draw.rect(screen, color, btn_rect)
                pygame.draw.rect(screen, BLACK, btn_rect, 2)
                text_surf = render_fitting_text(label, btn_rect.width, btn_rect.height)
                screen.blit(text_surf, (btn_rect.x + (btn_rect.width - text_surf.get_width()) // 2,
                                         btn_rect.y + (btn_rect.height - text_surf.get_height()) // 2))
                buttons.append((btn_rect, label))
            cancel_btn = draw_button(screen, "Cancel", 490, 480, 220, 40, (255, 182, 193))
            buttons.append((cancel_btn, "Cancel"))
        else:
            # Message and main action buttons
            # Wrap message
            def wrap_text(txt, font_obj, max_w):
                words = txt.split()
                lines, cur = [], ''
                for w in words:
                    test = cur + (' ' if cur else '') + w
                    if font_obj.size(test)[0] <= max_w:
                        cur = test
                    else:
                        lines.append(cur)
                        cur = w
                if cur: lines.append(cur)
                return lines

            for i, line in enumerate(wrap_text(message, font, 400)[:4]):
                screen.blit(font.render(line, True, BLACK), (50, 420 + i * 30))

            top_labels = ["Fight", "Bag"]
            colors = {"Fight": (255, 105, 97), "Bag": (218, 165, 32), "Surrender": (135, 206, 250)}
            for i, label in enumerate(top_labels):
                x = 490 + i * 125
                btn = draw_button(screen, label, x, 430, 110, 40, colors[label])
                buttons.append((btn, label))
            s_btn = draw_button(screen, "Surrender", 490, 480, 250, 40, colors["Surrender"])
            buttons.append((s_btn, "Surrender"))
    return buttons

# Bag (inventory) overlay UI
def draw_bag_overlay(screen, inventory, selected_item):
    buttons = []
    overlay_rect = pygame.Rect(100, 150, 600, 300)
    pygame.draw.rect(screen, (245, 245, 220), overlay_rect)
    pygame.draw.rect(screen, BLACK, overlay_rect, 3)

    # List of items
    item_rect = pygame.Rect(110, 160, 250, 280)
    pygame.draw.rect(screen, (240, 230, 210), item_rect)
    pygame.draw.rect(screen, BLACK, item_rect, 2)
    for idx, (item, count) in enumerate(inventory.items()):
        btn = pygame.Rect(item_rect.x + 10, item_rect.y + 10 + idx * 50, item_rect.width - 20, 40)
        pygame.draw.rect(screen, GRAY, btn)
        pygame.draw.rect(screen, BLACK, btn, 2)
        screen.blit(font.render(f"{item} x{count}", True, BLACK), (btn.x + 5, btn.y + 5))
        buttons.append((btn, item))

    # Detail pane and action buttons
    detail = pygame.Rect(380, 160, 200, 120)
    pygame.draw.rect(screen, (255, 248, 220), detail)
    pygame.draw.rect(screen, BLACK, detail, 2)
    if selected_item:
        screen.blit(font.render(selected_item, True, BLACK), (detail.x + 10, detail.y + 10))
        desc = "Heals 20 HP" if "Small" in selected_item else "Heals 50 HP"
        screen.blit(font.render(desc, True, BLACK), (detail.x + 10, detail.y + 50))
    else:
        screen.blit(font.render("Select an item", True, BLACK), (detail.x + 10, detail.y + 10))

    use_btn = draw_button(screen, "Use", detail.x, detail.y + detail.height + 10, 90, 40, (144, 238, 144))
    cancel_btn = draw_button(screen, "Cancel", detail.x + 110, detail.y + detail.height + 10, 90, 40, (255, 182, 193))
    buttons.append((use_btn, "Use"))
    buttons.append((cancel_btn, "Cancel"))
    return buttons

# Post-win actions UI
def draw_post_win_buttons(screen, width, height):
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(230)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))

    f = pygame.font.SysFont(None, 36)
    screen.blit(f.render("Victory! Choose your next action:", True, (0, 0, 0)), (width // 2 - 180, 200))
    next_btn = draw_button(screen, "Next Level", width // 2 - 150, 260, 140, 50, (173, 216, 230))
    main_btn = draw_button(screen, "Main Menu", width // 2 + 10, 260, 140, 50, (255, 228, 181))
    return next_btn, main_btn
