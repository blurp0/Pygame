# 🐓 Pygame Rooster Combat Game

A **Python Pygame-based combat game** where roosters battle using skills, stats, and items.  
This project demonstrates **game loops, OOP design, UI handling, and state management** using Pygame.

> 🎯 Ideal as a **school project, portfolio game, or learning reference** for Pygame development.

---

## 🎮 Game Overview

The game simulates rooster combat with:
- Playable rooster characters
- Skill-based attacks
- Inventory and items
- UI menus and multiple game states

The project is modular, making it easy to extend with new mechanics, animations, or sound effects.

---

## ✨ Features

- 🐔 Roosters with HP, attack, defense, and skills  
- ⚔️ Turn-based / action-based combat logic  
- 🎒 Inventory system  
- 🖥️ UI buttons, menus, and HUD  
- 🔄 Game state management (menu, battle, pause)  
- ⚙️ Centralized settings & styles  

---

## 🧠 Technologies Used

- **Python 3**
- **Pygame**
- Object-Oriented Programming (OOP)

---

## 📦 Requirements

Install dependencies:

```bash
pip install pygame
```

Python **3.x** is required.

---

## ▶️ How to Run the Game

Clone the repository:

```bash
git clone https://github.com/blurp0/Pygame.git
cd Pygame
```

Run the game:

```bash
python main.py
```

---

## 📁 Project Structure

```
Pygame/
├── assets/            # Images, sounds, and assets
├── main.py            # Game entry point
├── sabong_game.py     # Main game loop & combat logic
├── rooster.py         # Rooster classes & skills
├── inventory.py       # Inventory and item logic
├── game_state.py      # State management
├── ui.py              # UI elements and menus
├── settings.py        # Game configuration
├── style.py           # UI styling
└── README.md
```

---

## 🧩 Code Snippets

### 🎮 Main Game Loop (`main.py`)

```python
import pygame
from sabong_game import SabongGame

pygame.init()

game = SabongGame()
game.run()

pygame.quit()
```

---

### 🐔 Rooster Class Example (`rooster.py`)

```python
class Rooster:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        self.hp -= max(0, damage - self.defense)

    def is_alive(self):
        return self.hp > 0
```

---

### ⚔️ Simple Attack Logic

```python
def attack(attacker, defender):
    damage = attacker.attack
    defender.take_damage(damage)
```

---

### 🧠 Game State Handling (`game_state.py`)

```python
class GameState:
    MENU = "menu"
    BATTLE = "battle"
    PAUSE = "pause"
```

---

### 🎒 Inventory Example (`inventory.py`)

```python
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def use_item(self, index):
        return self.items.pop(index)
```

---

## 🕹️ Controls

*(May be updated depending on implementation)*

- **Arrow Keys / WASD** — Navigate
- **Mouse Click** — Select / interact
- **ESC** — Pause or return to menu

---

## 🖼️ Screenshots

Add screenshots by placing images in the `assets/` folder:

```markdown
![Gameplay](assets/screenshot.png)
```

---

## 🚧 Future Improvements

- Animations and sound effects
- AI-controlled opponents
- Skill cooldowns
- Save/load system
- Multiplayer support

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Open a Pull Request  

---
