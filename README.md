# Dungeon Master

A 2D adventure game developed in Python using Pygame, where players navigate through a dungeon, defeat enemies, and solve puzzles.

## Game Overview

Dungeon Master is a top-down pixel art adventure game where you play as an archer navigating through a dungeon. Your goal is to defeat a skeleton enemy, collect a key, and escape through a locked door.

## Features

- Smooth player movement and animation system
- Combat with bow and arrow mechanics
- Enemy AI with patrol patterns
- Interactive elements (keys, doors)
- Task-based progression system
- Sound effects and background music
- Main menu with start, settings, and exit options

## Controls

- **W** - Move Up
- **A** - Move Left
- **S** - Move Down
- **D** - Move Right
- **Left Arrow** - Shoot Arrow Left
- **Right Arrow** - Shoot Arrow Right

## Screenshots

(Add some screenshots of your game here)

## Installation

### Prerequisites
- Python 3.x
- Pygame library

### Installation Steps

1. Clone this repository or download the ZIP file
2. Install required dependencies:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python main.py
   ```

### Building an Executable

The project includes a `main.spec` file for building an executable using PyInstaller:

```
pyinstaller main.spec
```

## Project Structure

- `main.py` - Entry point for the game
- `menu.py` - Main menu interface
- `game.py` - Core game logic and loop
- `level.py` - Level layout and interaction
- `config.py` - Game settings and constants
- `resources.py` - Asset loading and resource management
- `buttons.py` - UI button components
- `sprites/` - Game object classes:
  - `base.py` - Base sprite class
  - `player.py` - Player character logic
  - `enemy.py` - Enemy behavior
  - `bullet.py` - Projectile mechanics

## Gameplay Guide

1. The game begins in the main menu. Click "Start" to begin playing.
2. Your first task is to defeat the skeleton enemy by shooting it with arrows.
3. Once defeated, the skeleton will drop a key.
4. Collect the key to unlock the exit door.
5. Navigate to the door to complete the level.

## Assets

The game uses various graphical and sound assets:
- Player character sprites with walking and attack animations
- Skeleton enemy with walking and death animations
- Environmental elements (barriers, doors)
- UI elements and buttons
- Sound effects for actions and background music

## Development

This game was developed using:
- Pygame for rendering and game logic
- Object-oriented programming for entity management
- State-based animation systems
- Event-driven input handling

## Credits

Sprites are based on LPC (Liberated Pixel Cup) assets.
Some assets may have been customized for this project.

## License

(Add appropriate license information here)
