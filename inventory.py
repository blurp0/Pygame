inventory = {
    "Small Potion": 2,
    "Large Potion": 1
}

def use_potion(player, item):
    if item == "Small Potion" and inventory[item] > 0:
        player.health = min(player.health + 20, 100)
        inventory[item] -= 1
        return "You used Small Potion! Healed 20 HP."
    elif item == "Large Potion" and inventory[item] > 0:
        player.health = min(player.health + 50, 100)
        inventory[item] -= 1
        return "You used Large Potion! Healed 50 HP."
    return ""
