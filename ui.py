import pygame
from rooster import Rooster
from settings import *

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
def draw_text(screen, text, x, y , color):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))
def draw_health_bar(surface, rooster, x, y, is_player=True):
    bar_width = 400
    bar_height = 40
    padding = 20
    container_width = bar_width + padding * 2
    container_height = bar_height + 80

    # Colors
    container_color = DARK_GRAY
    bar_bg_color = WHITE
    health_color = (0, 255, 0)
    text_color = WHITE
    triangle_color = DARK_GRAY

    # Fonts
    small_font = pygame.font.Font(None, 40)

    # Container rectangle
    container_rect = pygame.Rect(x - padding, y, container_width, container_height)
    pygame.draw.rect(surface, container_color, container_rect, border_radius=10)

    # Triangle pointer at the bottom corner (left or right side)
    triangle_height = 70
    triangle_width = 40
    triangle_base_y = container_rect.bottom - 15  # slightly above the bottom

    if is_player:
        # Bottom-left side triangle
        triangle_points = [
            (container_rect.left - triangle_width, triangle_base_y),
            (container_rect.left, triangle_base_y - triangle_height // 4),
            (container_rect.left, triangle_base_y + triangle_height // 10)
        ]
    else:
        # Bottom-right side triangle
        triangle_points = [
            (container_rect.right + triangle_width, triangle_base_y),
            (container_rect.right, triangle_base_y - triangle_height // 4),
            (container_rect.right, triangle_base_y + triangle_height // 10)
        ]
    pygame.draw.polygon(surface, triangle_color, triangle_points)

    # Draw rooster name
    name_text = small_font.render(rooster.name, True, text_color)
    name_rect = name_text.get_rect(topleft=(x, y + 10))
    surface.blit(name_text, name_rect)

    # Draw health bar
    bar_y = name_rect.bottom + 5
    pygame.draw.rect(surface, bar_bg_color, (x, bar_y, bar_width, bar_height))
    health_ratio = max(rooster.health / rooster.max_health, 0)
    current_bar_width = int(bar_width * health_ratio)
    pygame.draw.rect(surface, health_color, (x, bar_y, current_bar_width, bar_height))

    # Draw health text
    health_text = small_font.render(f"{rooster.health}/{rooster.max_health}", True, text_color)
    label_rect = health_text.get_rect()
    surface.blit(health_text, (x + bar_width - label_rect.width, bar_y + bar_height + 5))

def draw_menu(screen, width, height):
    
    CONTAINER_BG = (30, 30, 30, 180)  # Dark with some transparency

    # Title settings
    title_font = pygame.font.SysFont("impact", 72)  # Bold font for strong presence
    title_text = "Manok Masters"
    shadow_surface = title_font.render(title_text, True, RED)
    title_surface = title_font.render(title_text, True, YELLOW)

    # Tagline
    tagline_font = pygame.font.SysFont("arial", 28)
    tagline_text = "Laban kung laban, walang atrasan!"
    tagline_surface = tagline_font.render(tagline_text, True, WHITE)

    # Calculate container size based on title and tagline sizes + padding
    padding_x = 40
    padding_y = 20
    container_width = max(title_surface.get_width(), tagline_surface.get_width()) + padding_x * 2
    container_height = title_surface.get_height() + tagline_surface.get_height() + padding_y * 3

    container_x = (width - container_width) // 2
    container_y = 80  # Slightly above the title Y position

    # Create container surface with alpha for transparency
    container_surface = pygame.Surface((container_width, container_height), pygame.SRCALPHA)
    container_surface.fill((0, 0, 0, 0))  # Fully transparent background

    # Draw rounded rectangle as container background with bigger border radius
    pygame.draw.rect(container_surface, CONTAINER_BG, container_surface.get_rect(), border_radius=25)

    # Blit container onto main screen
    screen.blit(container_surface, (container_x, container_y))

    # Draw shadow (offset by 4 pixels)
    shadow_x = container_x + (container_width - shadow_surface.get_width()) // 2 + 4
    shadow_y = container_y + padding_y + 4
    screen.blit(shadow_surface, (shadow_x, shadow_y))

    # Draw title
    title_x = container_x + (container_width - title_surface.get_width()) // 2
    title_y = container_y + padding_y
    screen.blit(title_surface, (title_x, title_y))

    # Draw tagline below title with some vertical spacing
    tagline_x = container_x + (container_width - tagline_surface.get_width()) // 2
    tagline_y = title_y + title_surface.get_height() + padding_y
    screen.blit(tagline_surface, (tagline_x, tagline_y))

    # --- BUTTON SECTION ---
    button_font = pygame.font.SysFont(None, 45)  # Font for buttons with bigger size

    start_btn_color = (0, 200, 0)  # GREEN
    roster_btn_color = (0, 100, 255)  # BLUE
    shop_btn_color = (255, 140, 0)  # ORANGE
    exit_btn_color = (200, 0, 0)  # RED

    # Button labels
    buttons = [
        ("Laban na!", start_btn_color),
        ("Mga Manok", roster_btn_color),
        ("Tindahan", shop_btn_color),
        ("Lumabas", exit_btn_color)
    ]

    # Starting position for buttons (adjusted for container height)
    button_y = container_y + container_height + 40
    button_spacing = 20  # Spacing between buttons

    buttons_rect = []
    for label, color in buttons:
        btn_width, btn_height = button_font.size(label)
        btn_width += 60
        btn_height += 40

        button_rect = pygame.Rect(width // 2 - btn_width // 2, button_y, btn_width, btn_height)

        # Draw button background
        pygame.draw.rect(screen, color, button_rect, border_radius=10)

        # Draw text
        btn_label_surface = button_font.render(label, True, WHITE)
        btn_label_x = button_rect.centerx - btn_label_surface.get_width() // 2
        btn_label_y = button_rect.centery - btn_label_surface.get_height() // 2
        screen.blit(btn_label_surface, (btn_label_x, btn_label_y))

        buttons_rect.append(button_rect)
        button_y += btn_height + button_spacing

    # --- TUTORIAL BUTTON SECTION ---
    tutorial_btn_rect = pygame.Rect(width - 100, 20, 60, 60)
    tutorial_btn_surface = pygame.Surface((tutorial_btn_rect.width, tutorial_btn_rect.height), pygame.SRCALPHA)
    tutorial_btn_surface.fill((255, 255, 255, 200))  # Semi-transparent white
    screen.blit(tutorial_btn_surface, (tutorial_btn_rect.x, tutorial_btn_rect.y))

    question_mark_font = pygame.font.SysFont(None, 84)
    question_mark_surface = question_mark_font.render("?", True, BLACK)
    screen.blit(question_mark_surface, (
        tutorial_btn_rect.centerx - question_mark_surface.get_width() // 2,
        tutorial_btn_rect.centery - question_mark_surface.get_height() // 2))

    buttons_rect.append(tutorial_btn_rect)

    return buttons_rect



def draw_tutorial_overlay(screen, width, height, page_number, tutorial_pages):
    # Function to wrap text inside the overlay
    def wrap_text(text, font, max_width):
        words = text.split(' ')  # Split text into words
        lines = []
        current_line = words[0]

        for word in words[1:]:
            # Check if adding the next word exceeds the max width
            if font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word  # Add word to the current line
            else:
                lines.append(current_line)  # Add the current line to the lines list
                current_line = word  # Start a new line with the current word

        lines.append(current_line)  # Add the last line
        return lines

    # Overlay background (semi-transparent black)
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Title
    tutorial_title_font = pygame.font.SysFont(None, 60)
    tutorial_title_text = "Game Mechanics"
    tutorial_title_surface = tutorial_title_font.render(tutorial_title_text, True, (255, 255, 255))
    screen.blit(tutorial_title_surface, (width // 2 - tutorial_title_surface.get_width() // 2, 50))

    # Instructions for the current page
    instructions_font = pygame.font.SysFont(None, 50)
    padding = 200  # Padding on both left and right sides
    max_width = width - padding * 2  # Maximum width for wrapping (with padding)
    
    current_instructions = tutorial_pages[page_number]
    wrapped_lines = []

    for instruction in current_instructions:
        wrapped_lines.extend(wrap_text(instruction, instructions_font, max_width))  # Add wrapped lines
    
    line_spacing = 70
    total_height = len(wrapped_lines) * line_spacing

    # Center the block vertically and horizontally (text remains left-aligned with padding)
    start_y = (height - total_height) // 2
    block_x = padding  # Starting x position considering padding

    for i, line in enumerate(wrapped_lines):
        text_surface = instructions_font.render(line, True, (255, 255, 255))
        y = start_y + i * line_spacing
        screen.blit(text_surface, (block_x, y))

    # Back button (Top-Right Corner)
    back_btn_rect = pygame.Rect(width - 1250, 30, 100, 40)  # x stays the same, y is now 20 (top padding)
    pygame.draw.rect(screen, (200, 0, 0), back_btn_rect)
    back_btn_surface = pygame.font.SysFont(None, 35).render("Back", True, (255, 255, 255))
    screen.blit(back_btn_surface, (back_btn_rect.centerx - back_btn_surface.get_width() // 2,
                                   back_btn_rect.centery - back_btn_surface.get_height() // 2))

    # Next button
    font_size = 120
    next_btn_rect = pygame.Rect(width - 100, height // 2 - 40, 50, 50)

    # Create a semi-transparent white surface
    btn_surface = pygame.Surface((next_btn_rect.width, next_btn_rect.height), pygame.SRCALPHA)
    btn_surface.fill((255, 255, 255, 128))  # White with 50% opacity (128 out of 255)

    # Blit the semi-transparent surface onto the main screen
    screen.blit(btn_surface, (next_btn_rect.x, next_btn_rect.y))

    # Render the black ">" symbol
    next_btn_font = pygame.font.SysFont(None, font_size)
    next_btn_surface = next_btn_font.render(">", True, (0, 0, 0))  # Black text

    # Adjust vertical offset to move it up slightly if needed
    y_offset = -5
    screen.blit(next_btn_surface, (
        next_btn_rect.centerx - next_btn_surface.get_width() // 2,
        next_btn_rect.centery - next_btn_surface.get_height() // 2 + y_offset
    ))

    # Previous button
    font_size = 120
    prev_btn_rect = pygame.Rect(50, height // 2 - 40, 50, 50)  # Adjusted height and width

    # Create a semi-transparent white surface
    prev_surface = pygame.Surface((prev_btn_rect.width, prev_btn_rect.height), pygame.SRCALPHA)
    prev_surface.fill((255, 255, 255, 128))  # White with 50% opacity
    screen.blit(prev_surface, (prev_btn_rect.x, prev_btn_rect.y))

    # Render the black "<" symbol
    prev_btn_font = pygame.font.SysFont(None, font_size)
    prev_btn_symbol = prev_btn_font.render("<", True, (0, 0, 0))  # Black text

    # Move symbol up slightly
    y_offset = -5
    screen.blit(prev_btn_symbol, (
        prev_btn_rect.centerx - prev_btn_symbol.get_width() // 2,
        prev_btn_rect.centery - prev_btn_symbol.get_height() // 2 + y_offset
    ))


    return back_btn_rect, prev_btn_rect, next_btn_rect

def draw_shop(screen, items, width, height):
    # Use a bigger font
    title_font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)

    y = 200
    title = "Tindahan - I-click para Bumili"
    title_surface = title_font.render(title, True, BLACK)
    title_x = (width - title_surface.get_width()) // 2
    screen.blit(title_surface, (title_x, 60))

    buttons = []
    btn_width, btn_height = 360, 60
    for name, price in items.items():
        btn_x = (width - btn_width) // 2
        btn = draw_button(screen, f"{name} - {price} coins", btn_x, y, btn_width, btn_height)
        buttons.append((btn, name))
        y += btn_height + 30  # More spacing

    # Centered and bigger "Bumalik" button
    back_btn_x = (width - 300) // 2
    back_btn = draw_button(screen, "Bumalik", back_btn_x, y + 30, 300, 60)

    return buttons, back_btn


def draw_level_select(screen, highest_level, max_levels=5):
    # Title
    title = font.render("Pumili ng Antas", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    buttons = []
    # Button size and layout
    btn_width = 150
    btn_height = 80
    btn_spacing_x = 40
    btn_spacing_y = 30
    buttons_per_row = 3

    start_x = WIDTH // 2 - ((btn_width + btn_spacing_x) * buttons_per_row - btn_spacing_x) // 2
    start_y = 140

    for i in range(max_levels):
        row = i // buttons_per_row
        col = i % buttons_per_row
        x = start_x + col * (btn_width + btn_spacing_x)
        y = start_y + row * (btn_height + btn_spacing_y)

        level_num = i + 1
        text = str(level_num)
        color = (50, 150, 250) if level_num <= highest_level else (100, 100, 100)
        btn = draw_button(screen, text, x, y, btn_width, btn_height, color)
        buttons.append((btn, level_num))

    # Back button (larger and centered)
    back_btn = draw_button(
        screen, "Bumalik",
        WIDTH // 2 - 120,  # Centered
        y + btn_height + 50,
        240, 60,
        (200, 200, 200)
    )

    return buttons, back_btn


# Roster selection UI
def draw_roster(screen, unlocked_roosters, all_roosters, selected_rooster_name, width, height):
    draw_text(screen, "Naka-unlock na mga Manok", 50, 50,BLACK)
    buttons = []

    # Button dimensions for 2x3 grid
    button_width, button_height = 400, 100
    img_size = 80
    button_color = (245, 245, 220)

    rows = 3
    cols = 2

    loaded_count = 0
    total_to_load = len(unlocked_roosters)

    for i, name in enumerate(unlocked_roosters):
        rooster = all_roosters[name]

        base_name = rooster.name.lower().replace(' ', '_')
        role = "enemy"
        cache_key = f"{base_name}_{role}"

        # Preload if not cached yet
        if cache_key not in Rooster.image_cache:
            rooster_class = type(rooster)
            _ = rooster_class(0, 0, is_enemy=True)  # This should trigger image caching

        # If now cached, count it
        if cache_key in Rooster.image_cache:
            loaded_count += 1

        # Early break if all are cached
        if loaded_count == total_to_load:
            break

    # Now draw everything (no image loading needed anymore)
    for i, name in enumerate(unlocked_roosters):
        rooster = all_roosters[name]

        row = i // cols
        col = i % cols
        x_pos = 50 + col * (button_width + 20)
        y_pos = 100 + row * (button_height + 20)

        btn_rect = pygame.Rect(x_pos, y_pos, button_width, button_height)
        pygame.draw.rect(screen, button_color, btn_rect)

        base_name = rooster.name.lower().replace(' ', '_')
        cache_key = f"{base_name}_enemy"
        image = Rooster.image_cache.get(cache_key)

        if image:
            img_scaled = pygame.transform.scale(image, (img_size, img_size))
            screen.blit(img_scaled, (x_pos + 10, y_pos + 10))

        draw_text(
            screen,
            name + (" (Pinili)" if name == selected_rooster_name else ""),
            x_pos + img_size + 10,
            y_pos + (button_height // 2) - 10, BLACK
        )

        buttons.append((btn_rect, name))

    back_btn = draw_button(screen, "Bumalik", width - 150, height - 60, 100, 40)
    return buttons, back_btn


# Battle dialog box UI
def draw_dialog_box(screen, fight_mode, move_labels, move_data, message, inventory, dialog_state, selected_item=None):
    buttons = []
    dialog_rect = pygame.Rect(40, 500, 1175, 180)  # Dialog box
    pygame.draw.rect(screen, WHITE, dialog_rect)
    pygame.draw.rect(screen, BLACK, dialog_rect, 3)
    pygame.draw.line(screen, BLACK, (820, 500), (820, 680), 2)  # Divider

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

    if fight_mode:
        if dialog_state == "attack":
            for i, label in enumerate(move_labels[:4]):
                row, col = divmod(i, 2)
                x = 60 + col * 370
                y = 520 + row * 80
                btn_rect = pygame.Rect(x, y, 320, 60)
                color = GRAY
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    color = tuple(max(c - 30, 0) for c in color)
                pygame.draw.rect(screen, color, btn_rect)
                pygame.draw.rect(screen, BLACK, btn_rect, 2)

                # Skill stats
                skill = move_data[label]
                damage = skill["damage"]
                acc = int((1 - skill["miss_chance"]) * 100)
                cd = skill["cooldown"]
                cd_left = skill["cooldown_counter"]

                # Cooldown display logic
                if cd_left == 0:
                    cd_text = "CD: Ready"
                    cd_color = (0, 128, 0)  # Green
                else:
                    cd_text = f"CD: {cd_left}/{cd}"
                    cd_color = (200, 0, 0)  # Red

                # Text rendering
                title_font = pygame.font.SysFont("arial", 25, bold=True)
                stat_font = pygame.font.SysFont("arial", 14)

                # Text rendering
                title_font = pygame.font.SysFont("arial", 25, bold=True)
                stat_font = pygame.font.SysFont("arial", 14)

                # Skill name (centered)
                name_surf = title_font.render(label, True, BLACK)
                name_x = btn_rect.centerx - name_surf.get_width() // 1.3  # Center the name
                screen.blit(name_surf, (name_x, btn_rect.y + 3))

                # **Divider between skill name and stats**: Placing the divider correctly
                divider_x = btn_rect.x + btn_rect.width * 3 / 4  # Move divider after the skill name (1/3 of the button width)
                pygame.draw.line(screen, BLACK, (divider_x, btn_rect.y), (divider_x, btn_rect.y + btn_rect.height), 2)

                # **Narrower stats container**: 1/4 of the button width
                stats_width = btn_rect.width / 4  # Narrower width for the stats container
                stats_x = divider_x + 5  # Placing stats right after the divider

                # Position stats slightly higher
                stats_y_offset = 3

                # DMG, ACC, CD (right side of the button)
                dmg_surf = stat_font.render(f"DMG: {damage}", True, BLACK)
                acc_surf = stat_font.render(f"ACC: {acc}%", True, BLACK)
                cd_surf = stat_font.render(cd_text, True, cd_color)

                # Draw the skill stats inside the narrower container
                screen.blit(dmg_surf, (stats_x + 10, btn_rect.y + stats_y_offset))
                screen.blit(acc_surf, (stats_x + 10, btn_rect.y + stats_y_offset + 18))
                screen.blit(cd_surf, (stats_x + 10, btn_rect.y + stats_y_offset + 36))

                buttons.append((btn_rect, label))

            # Cancel button
            cancel_btn = draw_button(screen, "Kanselahin", 900, 550, 200, 80 , (255, 182, 193))
            buttons.append((cancel_btn, "Cancel"))

        elif dialog_state == "confirm_surrender":
            wrapped = wrap_text(message, font, 740)
            for i, line in enumerate(wrapped[:4]):
                screen.blit(font.render(line, True, BLACK), (60, 520 + i * 35))

            yes_btn = draw_button(screen, "Oo", 950, 525, 140, 50, (144, 238, 144))
            no_btn = draw_button(screen, "Hindi", 950, 600, 140, 50, (255, 160, 122))
            buttons.append((yes_btn, "Yes"))
            buttons.append((no_btn, "No"))

        else:
            for i, line in enumerate(wrap_text(message, font, 740)[:4]):
                screen.blit(font.render(line, True, BLACK), (60, 520 + i * 35))

            top_labels = ["Laban", "Bag"]
            colors = {"Laban": (255, 105, 97), "Bag": (218, 165, 32), "Sumuko": (135, 206, 250)}
            for i, label in enumerate(top_labels):
                x = 880 + i * 150
                btn = draw_button(screen, label, x, 520, 140, 60, colors[label])
                buttons.append((btn, label))

            s_btn = draw_button(screen, "Sumuko", 880, 600, 290, 60, colors["Sumuko"])
            buttons.append((s_btn, "Sumuko"))

    return buttons


# Bag (inventory) overlay UI
def draw_bag_overlay(screen, inventory, selected_item):
    buttons = []
    
    # Expanded overlay size
    overlay_rect = pygame.Rect(80, 50, 1100, 550)
    pygame.draw.rect(screen, (245, 245, 220), overlay_rect)
    pygame.draw.rect(screen, BLACK, overlay_rect, 3)

    # Expanded item list area (taller and wider)
    item_rect = pygame.Rect(100, 80, 400, 470)
    pygame.draw.rect(screen, (240, 230, 210), item_rect)
    pygame.draw.rect(screen, BLACK, item_rect, 2)

    for idx, (item, count) in enumerate(inventory.items()):
        btn = pygame.Rect(item_rect.x + 10, item_rect.y + 10 + idx * 50, item_rect.width - 20, 40)
        pygame.draw.rect(screen, GRAY, btn)
        pygame.draw.rect(screen, BLACK, btn, 2)
        screen.blit(font.render(f"{item} x{count}", True, BLACK), (btn.x + 5, btn.y + 5))
        buttons.append((btn, item))

    # Moved detail pane further right and larger
    detail = pygame.Rect(530, 100, 600, 200)
    pygame.draw.rect(screen, (255, 248, 220), detail)
    pygame.draw.rect(screen, BLACK, detail, 2)

    if selected_item:
        screen.blit(font.render(selected_item, True, BLACK), (detail.x + 10, detail.y + 10))
        desc = "Pagalingin ng 50 HP" if "Maliit" in selected_item else "Pagalingin ng 80 HP"
        screen.blit(font.render(desc, True, BLACK), (detail.x + 10, detail.y + 50))
    else:
        screen.blit(font.render("Pumili ng item", True, BLACK), (detail.x + 10, detail.y + 10))

    # Repositioned buttons below the detail pane
    use_btn = draw_button(screen, "Gamitin", detail.x, detail.y + detail.height + 20, 150, 50, (144, 238, 144))
    cancel_btn = draw_button(screen, "Kanselahin", detail.x + 170, detail.y + detail.height + 20, 150, 50, (255, 182, 193))
    buttons.append((use_btn, "Use"))
    buttons.append((cancel_btn, "Cancel"))

    return buttons

def draw_post_win_buttons(screen, width, height, game_over, victory, is_final_level=False):
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(230)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))

    f = pygame.font.SysFont(None, 36)

    def wrap_text(text, font_obj, max_width):
        words = text.split()
        lines, cur = [], ""
        for word in words:
            test_line = cur + (' ' if cur else '') + word
            if font_obj.size(test_line)[0] <= max_width:
                cur = test_line
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    # Set message
    if victory:
        if is_final_level:
            message = "Tagumpay! Natalo mo ang huling kalaban!\nMaraming salamat sa paglalaro ng Sabong!"
        else:
            message = "Tagumpay! Pumili ng iyong susunod na hakbang:"
    else:
        message = "Pagkatalo! Pumili ng iyong susunod na hakbang:"

    # Wrap and draw message lines
    wrapped_lines = wrap_text(message, f, 500)
    for i, line in enumerate(wrapped_lines):
        text_surf = f.render(line, True, (0, 0, 0))
        screen.blit(text_surf, (width // 2 - text_surf.get_width() // 2, 100 + i * 30))

    # Draw buttons
    button_width = 300
    button_height = 80
    button_gap = 20

    if victory:
        if is_final_level:
            # Final level: only show main menu
            main_btn_y = 230
            main_btn = draw_button(screen, "Pangunahing Menu", width // 2 - button_width // 2, main_btn_y, button_width, button_height, (255, 228, 181))
            return None, main_btn
        else:
            # Normal victory: next + main
            next_btn_y = 230
            next_btn = draw_button(screen, "Susunod na Antas", width // 2 - button_width // 2, next_btn_y, button_width, button_height, (173, 216, 230))
            main_btn_y = next_btn_y + button_height + button_gap
            main_btn = draw_button(screen, "Pangunahing Menu", width // 2 - button_width // 2, main_btn_y, button_width, button_height, (255, 228, 181))
            return next_btn, main_btn
    else:
        # Loss: retry + main
        retry_btn_y = 230
        retry_btn = draw_button(screen, "Subukan muli", width // 2 - button_width // 2, retry_btn_y, button_width, button_height, (173, 216, 230))
        main_btn_y = retry_btn_y + button_height + button_gap
        main_btn = draw_button(screen, "Pangunahing Menu", width // 2 - button_width // 2, main_btn_y, button_width, button_height, (255, 228, 181))
        return retry_btn, main_btn


def draw_shop_confirmation(screen, message, width, height):
    font = pygame.font.SysFont(None, 36)  # Bigger font
    box_width, box_height = 500, 200  # Bigger box
    box_rect = pygame.Rect(width // 2 - box_width // 2, height // 2 - box_height // 2-15, box_width, box_height)

    pygame.draw.rect(screen, (255, 255, 200), box_rect)
    pygame.draw.rect(screen, (0, 0, 0), box_rect, 3)  # Border for clarity

    # Word-wrapping logic
    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        return lines

    wrapped_lines = wrap_text(message, font, box_width - 40)
    y_offset = box_rect.y + 20
    for line in wrapped_lines:
        msg_surface = font.render(line, True, (0, 0, 0))
        x_position = box_rect.centerx - msg_surface.get_width() // 2
        screen.blit(msg_surface, (x_position, y_offset))
        y_offset += msg_surface.get_height() + 5

    # Bigger Buttons
    btn_width, btn_height = 80, 50
    spacing = 50
    yes_btn = pygame.Rect(width // 2 - btn_width - spacing // 2, box_rect.bottom - btn_height - 20, btn_width, btn_height)
    no_btn = pygame.Rect(width // 2 + spacing // 2, box_rect.bottom - btn_height - 20, btn_width, btn_height)

    pygame.draw.rect(screen, (0, 200, 0), yes_btn)
    pygame.draw.rect(screen, (200, 0, 0), no_btn)

    yes_text = font.render("Oo", True, (255, 255, 255))
    no_text = font.render("Hindi", True, (255, 255, 255))

    screen.blit(yes_text, (yes_btn.x + (btn_width - yes_text.get_width()) // 2, yes_btn.y + (btn_height - yes_text.get_height()) // 2))
    screen.blit(no_text, (no_btn.x + (btn_width - no_text.get_width()) // 2, no_btn.y + (btn_height - no_text.get_height()) // 2))

def draw_rooster_skills_panel(screen, skills, selected_skill, width, height):
    panel_width = 300  # Adjust the panel width
    panel_height = 250  # Adjust the panel height
    panel_x = width - panel_width - 20  # Move the panel a little to the left
    panel_y = 100  # Move the panel further down from the top of the screen

    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(screen, (220, 220, 220), panel_rect)
    pygame.draw.rect(screen, BLACK, panel_rect, 2)

    skill_buttons = []
    y_offset = panel_rect.y + 10
    button_height = 50  # Adjust button height
    button_padding = 5  # Add padding between the button and text

    for skill_name, skill_info in skills.items():
        btn = pygame.Rect(panel_rect.x + 10, y_offset, panel_rect.width - 20, button_height)
        pygame.draw.rect(screen, GRAY, btn)
        pygame.draw.rect(screen, BLACK, btn, 2)
        
        # Render text for skill
        text_surf = font.render(skill_name, True, BLACK)
        text_rect = text_surf.get_rect()
        text_rect.center = btn.center  # Center the text within the button
        screen.blit(text_surf, text_rect.topleft)

        skill_buttons.append((btn, skill_name))

        y_offset += button_height + 10  # Add more space between buttons if needed

    return skill_buttons


def draw_skill_description_box(screen, selected_skill_name, skills, WIDTH, HEIGHT):
    # Define the size and position for the description box
    desc_rect = pygame.Rect(50, HEIGHT - 180, WIDTH - 350, 100)  # Reduced width to give space for damage & accuracy
    pygame.draw.rect(screen, (245, 245, 220), desc_rect)
    pygame.draw.rect(screen, BLACK, desc_rect, 2)

    # Define the size and position for the damage and accuracy box (separate from the description)
    stats_rect = pygame.Rect(WIDTH - 250, HEIGHT - 180, 230, 100)
    pygame.draw.rect(screen, (245, 245, 220), stats_rect)
    pygame.draw.rect(screen, BLACK, stats_rect, 2)

    if selected_skill_name:
        skill_info = skills[selected_skill_name]
        name_text = font.render(f"{selected_skill_name}:", True, BLACK)

        # Wrap the description text to fit within the left side of the box
        wrapped_desc_lines = wrap_text(skill_info["description"], desc_rect.width - 20)

        # Drawing skill name
        screen.blit(name_text, (desc_rect.x + 10, desc_rect.y + 10))

        # Drawing wrapped description lines with padding on the left
        y_offset = desc_rect.y + 40
        for line in wrapped_desc_lines:
            wrapped_desc = font.render(line, True, BLACK)
            screen.blit(wrapped_desc, (desc_rect.x + 10, y_offset))
            y_offset += wrapped_desc.get_height() + 5  # Add spacing between lines

        # No separator line below the description, just keep it neat

        # Displaying Damage and Accuracy in the right box
        damage_text = font.render(f"Pinsala: {skill_info['damage']}", True, BLACK)
        accuracy_text = font.render(f"Katumpakan: {round((1 - skill_info['miss_chance']) * 100)}%", True, BLACK)

        # Adjust the vertical position for damage and accuracy to avoid overlap
        screen.blit(damage_text, (stats_rect.x + 10, stats_rect.y + 20))
        screen.blit(accuracy_text, (stats_rect.x + 10, stats_rect.y + 60))

    else:
        wrapped_lines = wrap_text("Pumili ng isang kasanayan upang makita ang mga detalye", desc_rect.width - 20)
        for i, line in enumerate(wrapped_lines):
            prompt_surface = font.render(line, True, (100, 100, 100))
            screen.blit(prompt_surface, (desc_rect.x + 10, desc_rect.y + 20 + i * 25))  # 25 = line spacing




# Helper function to wrap text
def wrap_text(text, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Check if adding this word exceeds the width
        test_line = f"{current_line} {word}".strip()
        test_surface = font.render(test_line, True, BLACK)
        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word  # Start a new line with the current word

    if current_line:  # Add the last line if there's any leftover text
        lines.append(current_line)

    return lines

def draw_shop_message(screen, message, width, height):
    font = pygame.font.SysFont(None, 36)
    box_width, box_height = 500, 150
    box_rect = pygame.Rect(width // 2 - box_width // 2, height // 2 - box_height // 2, box_width, box_height)

    pygame.draw.rect(screen, (255, 230, 230), box_rect)  # Light red background
    pygame.draw.rect(screen, (150, 0, 0), box_rect, 3)

    # Word-wrapping logic
    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        return lines

    wrapped_lines = wrap_text(message, font, box_width - 40)
    
    # Adjust vertical offset to center the text better inside the box
    total_text_height = sum([font.size(line)[1] for line in wrapped_lines]) + 5 * (len(wrapped_lines) - 1)
    y_offset = box_rect.y + (box_height - total_text_height) // 2  # Centering text vertically

    for line in wrapped_lines:
        msg_surface = font.render(line, True, (0, 0, 0))
        x_position = box_rect.centerx - msg_surface.get_width() // 2  # Center the text horizontally
        screen.blit(msg_surface, (x_position, y_offset))
        y_offset += msg_surface.get_height() + 5

