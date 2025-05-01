# Initial inventory setup
inventory = {
    "Small Potion": 2,
    "Large Potion": 1
}


# Use potion function that updates the player's health
def use_potion(player, item):
    if item in inventory and inventory[item] > 0:
        if item == "Small Potion":
            player.health = min(player.health + 20, 100)
            inventory[item] -= 1
            return "You used Small Potion! Healed 20 HP."
        elif item == "Large Potion":
            player.health = min(player.health + 50, 100)
            inventory[item] -= 1
            return "You used Large Potion! Healed 50 HP."
    return f"You don't have {item} or it's out of stock."


# Add item to inventory
def add_item(item, quantity=1):
    if item in inventory:
        inventory[item] += quantity
    else:
        inventory[item] = quantity


# Remove item from inventory
def remove_item(item, quantity=1):
    if item in inventory and inventory[item] >= quantity:
        inventory[item] -= quantity
        if inventory[item] == 0:
            del inventory[item]
    else:
        return f"Not enough {item} in inventory."


# Check if an item exists in inventory
def check_item(item):
    return item in inventory and inventory[item] > 0


# Display inventory items
def display_inventory():
    if inventory:
        inventory_list = [f"{item}: {quantity}" for item, quantity in inventory.items()]
        return "\n".join(inventory_list)
    return "Inventory is empty."


# Example of usage (simulating a player and using potions)
class Player:
    def __init__(self):
        self.health = 100  # Initial health


# Simulating player usage of items
player = Player()

# Test item usage
print(use_potion(player, "Small Potion"))  # Should heal and reduce potion count
print(use_potion(player, "Large Potion"))  # Should heal and reduce potion count

# Add and remove items from inventory
add_item("Small Potion", 3)
remove_item("Large Potion", 1)

# Check inventory display
print(display_inventory())
