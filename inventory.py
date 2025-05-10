inventory = {
    "Maliit na Potion": 30,
    "Malaking Potion": 20
}

shop_items = {
    "Maliit na Potion": 10,
    "Malaking Potion": 20
}

def can_afford(item_name, money):
    return money >= shop_items.get(item_name, float('inf'))

def buy_item(item_name, inventory, money):
    cost = shop_items.get(item_name)
    if cost is not None and money >= cost:
        inventory[item_name] = inventory.get(item_name, 0) + 1
        return inventory, money - cost, "Matagumpay na Nabili ang Item"
    else:
        return inventory, money, "Nabigo ang Pagbili ng Item, Kulang ang Pera"

def use_item(item_name, inventory, player, small_potion=50, big_potion=80):
    if inventory.get(item_name, 0) <= 0:
        return "Wala ka nang {}!".format(item_name), inventory, player

    if item_name == "Maliit na Potion":
        player.health = min(player.health + small_potion, player.max_health)
        message = f"Ginamit mo ang {item_name}! Gumaling ng {small_potion} HP!"
    elif item_name == "Malaking Potion":
        player.health = min(player.health + big_potion, player.max_health)
        message = f"Ginamit mo ang {item_name}! Gumaling ng {big_potion} HP!"
    else:
        return "Hindi kilalang item.", inventory, player

    inventory[item_name] -= 1
    return message, inventory, player
