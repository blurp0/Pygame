from rooster import Rooster
from settings import RED, WHITE

def reset_game(selected_name, all_roosters):
    player = Rooster(selected_name, all_roosters[selected_name].color, 100, 400)
    enemy = Rooster("Red", RED, 600, 100)
    return player, enemy, "player", False, "", "menu", False
