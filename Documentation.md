# Dungeon Master Game Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
   - [Game Loop](#game-loop)
   - [Menu System](#menu-system)
   - [Resource Management](#resource-management)
4. [Game Mechanics](#game-mechanics)
   - [Character Control](#character-control)
   - [Combat System](#combat-system)
   - [Objective System](#objective-system)
   - [Collisions](#collisions)
5. [Sprite System](#sprite-system)
   - [Base Classes](#base-classes)
   - [Player Class](#player-class)
   - [Enemy Class](#enemy-class)
   - [Sprite Manager](#sprite-manager)
6. [Level Design](#level-design)
7. [Camera](#camera)
8. [UI Components](#ui-components)
   - [Buttons](#buttons)
   - [Hint System](#hint-system)
9. [Resources](#resources)
   - [Sprites](#sprites)
   - [Sounds](#sounds)
   - [Images](#images)
10. [Configuration](#configuration)
11. [Detailed File Analysis](#detailed-file-analysis)

## Project Overview

Dungeon Master is a 2D top-down adventure game created with the Pygame library. The player explores a dungeon, defeats enemies, collects keys, and reaches the exit. The game includes animated characters, collision detection, and camera movement.

### Key Features:
- Complete animation system for characters and enemies
- Bow and arrow combat system
- Collisions with obstacles and other objects
- Objective and progress system
- Camera that follows the player
- Menu system with interactive buttons

## Project Structure

```
DungeonMaster/
├── main.py              # Entry point
├── game.py              # Main game class and logic
├── menu.py              # Menu system
├── config.py            # Constants and game settings
├── resources.py         # Resource loading utilities
├── camera.py            # Camera management
├── level.py             # Level creation and management
├── sprite_manager.py    # Centralized sprite management
├── buttons.py           # UI button components
├── sprites/             # Sprite classes
│   ├── base.py          # Base sprite class
│   ├── player.py        # Player character class
│   ├── enemy.py         # Enemy class
│   └── bullet.py        # Projectile class
├── Finals/              # Game resources - sprites and animations
├── background/          # Background images
├── menu/                # Menu resources
└── objects/             # Game object sprites
```

## Core Components

### Game Loop

The basic structure of the game follows a standard game loop defined in the `Game` class in `game.py`:

1. **Event Handling** (`handle_events`): Processes user input and game events
2. **Game State Update** (`update`): Updates positions, animations, and game logic
3. **Rendering** (`render`): Draws the game world and UI to the screen
4. **Frame Rate Control**: Maintains a stable frame rate

```python
def run(self):
    """Main game loop"""
    while self.running:
        # Handle user input
        self.handle_events()
        # Update game state
        self.update()
        # Render the game to the screen
        self.render()
        # Control frame rate (FPS)
        self.clock.tick(FPS)
```

#### Detailed Game Loop Breakdown:

1. **Initialization**:
   - Creates all necessary objects (player, enemies, level)
   - Loads resources (images, animations)
   - Sets up the initial game state

2. **Game Loop**:
   - `handle_events()`:
     - Processes events from Pygame (key presses, window closing)
     - Tracks key states for smooth control
     - Triggers appropriate character actions (movement, attack)

   - `update()`:
     - Updates positions and states of all game objects
     - Checks for collisions between objects
     - Updates the state of game objectives
     - Checks for win or loss conditions

   - `render()`:
     - Draws the background
     - Applies camera offset
     - Renders all sprites considering the offset
     - Renders the user interface
     - Updates the screen using `pygame.display.update()`

   - `clock.tick(FPS)`:
     - Regulates the game loop speed
     - Ensures consistent game speed regardless of computer performance

### Menu System

The menu system (`menu.py`) provides the entry point to the game and contains:

- `Menu` class: manages the main game menu
- Interactive buttons for starting the game and exiting
- Background music and visuals
- Event handling system for buttons

```python
def run(self):
    """Main menu loop"""
    while self.running:
        self.handle_events()  # Process events (button clicks)
        self.update()         # Update states (mouse hover checks)
        self.render()         # Render menu
        self.clock.tick(FPS)  # Control frame rate
```

#### Detailed Menu Analysis:

1. **Menu Initialization**:
   ```python
   def __init__(self):
       pygame.init()
       pygame.mixer.init()  # Initialize audio system
       # Create window
       self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
       pygame.display.set_caption("Dungeon Master")
       # Load background and title
       self.background = ResourceManager.load_image(MENU_BG, (WINDOW_WIDTH, WINDOW_HEIGHT))
       self.title_menu = ResourceManager.load_image(MENU_TITLE)
       # Load and start background music
       self.background_music = pygame.mixer.Sound(MENU_MUSIC)
       self.background_music.set_volume(0.5)  
       self.background_music.play(loops=-1)  # Infinite playback
       # Create buttons
       self.start_button = ImageButton(
           (WINDOW_WIDTH / 2) - 100, 200, 200, 65,
           MENU_BUTTON_START_PASSIVE, MENU_BUTTON_START_ACTIVE, "menu/click.mp3", 0.2
       )
       self.quit_button = ImageButton(
           (WINDOW_WIDTH / 2) - 100, 300, 200, 65,
           MENU_BUTTON_EXIT_PASSIVE, MENU_BUTTON_EXIT_ACTIVE, "menu/click.mp3", 0.2
       )
       # Create clock for FPS control
       self.clock = pygame.time.Clock()
       self.running = True
   ```

2. **Menu Event Handling**:
   ```python
   def handle_events(self):
       for event in pygame.event.get():
           # Handle window closing
           if event.type == pygame.QUIT:
               self.quit_game()
           # Pass mouse click events to buttons
           elif event.type == pygame.MOUSEBUTTONDOWN:
               self.start_button.handle_event(event)
               self.quit_button.handle_event(event)
           # Handle custom events from buttons
           elif event.type == pygame.USEREVENT:
               if event.button == self.start_button:
                   self.start_game()
               elif event.button == self.quit_button:
                   self.quit_game()
   ```

3. **Mouse Hover Checks**:
   ```python
   def update(self):
       if not pygame.get_init():  
           return
       mouse_pos = pygame.mouse.get_pos()
       # Update hover state for buttons
       self.start_button.check_hover(mouse_pos)
       self.quit_button.check_hover(mouse_pos)
   ```

4. **Menu Rendering**:
   ```python
   def render(self):
       # Draw background
       self.screen.blit(self.background, (0, 0))
       # Draw centered title
       title_x = (WINDOW_WIDTH - self.title_menu.get_width()) // 2
       self.screen.blit(self.title_menu, (title_x, 50))
       # Draw buttons
       self.start_button.draw(self.screen)
       self.quit_button.draw(self.screen)
       # Update screen
       pygame.display.flip()
   ```

5. **Starting the Game from Menu**:
   ```python
   def start_game(self):
       # Pause music before starting the game
       self.background_music.stop()
       # Create game instance and pass music
       game = Game(self.background_music)
       game.run()  # Start the game loop
       # Resume menu music after game ends
       if self.running and pygame.get_init():
           self.background_music.play(loops=-1)
   ```

### Resource Management

The `ResourceManager` class in `resources.py` centralizes resource loading for:
- Preventing repeated loading of the same resources
- Providing a unified scaling interface
- Organizing access to character animations

```python
class ResourceManager:
    """Class for loading and managing game resources"""

    @staticmethod
    def load_image(path, size=None):
        """Load image with optional scaling"""
        image = pygame.image.load(path)
        if size:
            return pygame.transform.scale(image, size)
        return image

    @staticmethod
    def load_animation(paths, sizes=None):
        """Load a list of images for animation"""
        if sizes:
            return [pygame.transform.scale(pygame.image.load(path), sizes) for path in paths]
        return [pygame.image.load(path) for path in paths]
```

#### Additional Loading Functions:

1. **Player Animation Loading**:
   ```python
   def load_player_animations():
       # Running animations
       run_left = ResourceManager.load_animation([
           "Finals/hero/run/l_run_1.png", "Finals/hero/run/l_run_2.png",
           # ...other animation frames
       ])
       # Attack animations
       attack_right = ResourceManager.load_animation([
           "Finals/hero/attack/r_attack_1.png", "Finals/hero/attack/r_attack_2.png",
           # ...other animation frames
       ])
       return {
           'run_left': run_left,
           'run_right': run_right,
           'run_up': run_up,
           'run_down': run_down,
           'attack_left': attack_left,
           'attack_right': attack_right,
           'stay': {
               'left': ResourceManager.load_image('Finals/hero/stay/l_stay.png', (36, 52)),
               'right': ResourceManager.load_image('Finals/hero/stay/r_stay.png', (36, 52)),
               'up': ResourceManager.load_image('Finals/hero/stay/u_stay.png', (30, 52)),
               'down': ResourceManager.load_image('Finals/hero/stay/d_stay.png', (30, 58))
           }
       }
   ```

2. **Enemy Animation Loading**:
   ```python
   def load_enemy_animations():
       # Movement animations in different directions
       run_left = ResourceManager.load_animation([
           "Finals/enemy/left/l_run_1.png", "Finals/enemy/left/l_run_2.png",
           # ...other animation frames
       ])
       # Death animation
       death = ResourceManager.load_animation([
           "Finals/enemy/death/death_1.png", "Finals/enemy/death/death_2.png",
           # ...other animation frames
       ])
       return {
           'run_left': run_left,
           'run_right': run_right,
           'run_up': run_up,
           'run_down': run_down,
           'death': death
       }
   ```

## Game Mechanics

### Character Control

The character control system is implemented in the `Player` class (file `sprites/player.py`):

```python
def update_movement(self):
    """Update velocity based on active keys"""
    # If attack animation is playing, stop movement
    if self.attacking_left or self.attacking_right:
        self.x_speed = 0
        self.y_speed = 0
        return
    # Reset velocity
    self.x_speed = 0
    self.y_speed = 0
    # Horizontal movement
    if self.moving_left:
        self.x_speed -= self.base_speed
        self.last_direction = 'left'
    if self.moving_right:
        self.x_speed += self.base_speed
        self.last_direction = 'right'
    # Vertical movement
    if self.moving_up:
        self.y_speed -= self.base_speed
        if not (self.moving_left or self.moving_right):
            self.last_direction = 'up'
    if self.moving_down:
        self.y_speed += self.base_speed
        if not (self.moving_left or self.moving_right):
            self.last_direction = 'down'
    # Normalize velocity for diagonal movement
    if self.x_speed != 0 and self.y_speed != 0:
        diagonal_speed = self.base_speed / math.sqrt(2)
        self.x_speed = diagonal_speed if self.x_speed > 0 else -diagonal_speed
        self.y_speed = diagonal_speed if self.y_speed > 0 else -diagonal_speed
```

#### Control System Features:

1. **Independent Key Presses**: The player can press and hold multiple keys simultaneously for diagonal movement.

2. **Diagonal Movement Normalization**: When moving diagonally, speed is normalized so the player doesn't move faster than in orthogonal directions.

3. **Last Direction Tracking**: The game remembers the last direction of movement to correctly display idle animation.

4. **Movement Animation Control**:
   ```python
   def update_animation(self):
       # ... existing code ...
       # Movement animation
       if self.x_speed != 0 or self.y_speed != 0:
           self.run_animation_index = (self.run_animation_index + 1) % 8
           # Choose animation based on direction
           if abs(self.x_speed) > abs(self.y_speed):
               # Horizontal movement dominates
               if self.x_speed > 0:
                   anim_frame = self.animations['run_right'][self.run_animation_index]
               else:
                   anim_frame = self.animations['run_left'][self.run_animation_index]
           else:
               # Vertical movement dominates or diagonal
               if self.y_speed > 0:
                   anim_frame = self.animations['run_down'][self.run_animation_index]
               else:
                   anim_frame = self.animations['run_up'][self.run_animation_index]
           self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
       else:
           # Idle animation
           self.image = self.animations['stay'][self.last_direction]
   ```

5. **Handling Collisions with Obstacles**:
   ```python
   def update(self, barriers):
       self.update_movement()
       # Horizontal movement
       self.rect.x += self.x_speed
       # Check screen boundaries
       if self.rect.left < 0:
           self.rect.left = 0
       if self.rect.right > pygame.display.get_surface().get_width():
           self.rect.right = pygame.display.get_surface().get_width()
       # Check collisions with barriers horizontally
       platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
       if self.x_speed > 0:  # moving right
           for p in platforms_touched:
               self.rect.right = min(self.rect.right, p.rect.left)
       if self.x_speed < 0:  # moving left
           for p in platforms_touched:
               self.rect.left = max(self.rect.left, p.rect.right)
       # Similarly for vertical movement
       # ... rest of the code ...
   ```

### Combat System

The combat system is based on bow shooting:

1. **Creating Projectiles (Arrows)**:
   ```python
   def fire_right(self):
       """Shoot to the right"""
       bullet = Bullet("objects/arrow_r.png", 31, 5,
                      self.rect.x + self.rect.width,
                      (self.rect.y + self.rect.height // 2) - 7,
                      18)
       return bullet
   ```

2. **Attack Animation**:
   ```python
   def update_animation(self):
       # Attack animation takes priority
       if self.attacking_left:
           if self.attack_animation_index == 9:
               bullet = self.fire_left()
               self.attack_animation_index += 1
               return bullet
           elif self.attack_animation_index == 11:
               self.attack_animation_index = 0
               self.attacking_left = False
               return None
           else:
               self.attack_animation_index += 1
           anim_frame = self.animations['attack_left'][self.attack_animation_index]
           self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
           return None
       # ... similarly for attacking_right ...
   ```

3. **Projectile Hit Detection**:
   ```python
   def check_bullet_collisions(self, tips):
       for bullet in self.bullets:
           # Check collision with enemies
           enemy_hit = pygame.sprite.spritecollideany(bullet, self.monsters)
           if enemy_hit:
               self.sprite_manager.remove(bullet, 'bullets')
               self.tip_1.image = ResourceManager.load_image("objects/tip_1_done.png", (300, 30))
               enemy_hit.start_death()
               return True, enemy_hit
           # Check collision with barriers
           if pygame.sprite.spritecollideany(bullet, self.barriers):
               self.sprite_manager.remove(bullet, 'bullets')
       return False, None
   ```

4. **Enemy Behavior When Taking Damage**:
   ```python
   def start_death(self):
       """Start death animation"""
       self.dying = True
       self.speed_x = 0
       self.speed_y = 0
       self.death_index = 0
   ```

### Objective System

The game has a linear objective system:

1. **Initial Objective**: Defeat the enemy
2. **Second Objective**: Collect the key dropped by the enemy
3. **Final Objective**: Reach the door with the key

```python
def check_key_collection(self, hero):
    """Check key collection"""
    if not self.key_collected and pygame.sprite.spritecollideany(hero, self.keys):
        self.sprite_manager.empty_group('keys')
        self.key_collected = True
        self.tip_2.image = ResourceManager.load_image("objects/tip_2_done.png", (300, 30))
        self.tip_3_visible = True
        return True
    return False
```

### Collisions

The game implements several types of collisions:

1. **Player with Barriers**: Prevents movement through walls
2. **Projectiles with Enemies**: Detects hits and triggers enemy death animation
3. **Projectiles with Barriers**: Removes the projectile upon wall collision
4. **Player with Enemies**: Triggers game over when colliding
5. **Player with Key**: Collects the key and updates the objective
6. **Player with Door**: Checks for key possession and completes the level upon success

```python
# Example of player collision with enemies in Game class update() method
if pygame.sprite.spritecollideany(self.hero, self.sprite_manager.monsters):
    self.window.blit(self.lose_fon, (0, 0))
    self.window.blit(self.lose_image, (150, 50))
    self.finish = True

# Example of collision with final door
if pygame.sprite.collide_rect(self.hero, self.level.final_door):
    if self.level.key_collected:
        self.window.blit(self.win_fon, (0, 0))
        self.window.blit(self.win_image, (150, 50))
        self.finish = True
```

## Sprite System

### Base Classes

The base `GameSprite` class is defined in `sprites/base.py` and inherits from `pygame.sprite.Sprite`:

```python
class GameSprite(pygame.sprite.Sprite):
    """Base class for all game sprites"""
    def __init__(self, picture, width, height, x, y):
        super().__init__()
        self.image = ResourceManager.load_image(picture, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self, surface):
        """Draw the sprite on a surface"""
        surface.blit(self.image, (self.rect.x, self.rect.y))
```

### Player Class

The `Player` class (file `sprites/player.py`) extends the base class:

```python
class Player(GameSprite):
    """Player class with improved movement system"""
    def __init__(self, picture, width, height, x, y, x_speed, y_speed, animations):
        super().__init__(picture, width, height, x, y)
        self.base_speed = 3  # base speed
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.animations = animations
        # Movement states (independent)
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        # Attack states
        self.attacking_left = False
        self.attacking_right = False
        # Animation indices
        self.run_animation_index = 0
        self.attack_animation_index = 0
        # Last direction for correct idle animation
        self.last_direction = 'right'
```

#### Key Player Class Methods:

1. **Movement and Collision Updates**:
   - `update_movement()`: Calculates character speed based on pressed keys
   - `update(barriers)`: Moves the character and checks collisions with obstacles

2. **Attack System**:
   - `fire_left()`, `fire_right()`: Create projectiles
   - `start_left_attack()`, `start_right_attack()`: Start attack animations

3. **Animation System**:
   - `update_animation()`: Selects and applies the appropriate animation based on state

4. **Movement Control**:
   - `start_left_move()`, `stop_left_move()`, etc.: Methods for controlling movement states

### Enemy Class

The `Enemy` class (file `sprites/enemy.py`) implements automatic movement and animation for enemies:

```python
class Enemy(GameSprite):
    """Enemy class"""
    def __init__(self, picture, width, height, x, y, speed_x, speed_y, animations):
        super().__init__(picture, width, height, x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.animations = animations
        # Enemy states
        self.e_left = False
        self.e_right = False
        self.e_up = False
        self.e_down = False
        self.dying = False
        self.dead = False
        # Animation index
        self.anim_index = 0
        self.death_index = 0
```

#### Key Enemy Class Methods:

1. **Movement Update**:
   ```python
   def update(self):
       # If enemy is dying or dead, don't move it
       if self.dying or self.dead:
           return
       # Update position
       self.rect.x += self.speed_x
       self.rect.y += self.speed_y
       # Patrol logic (rectangular path)
       if self.rect.y <= 185:
           self.speed_y = 0
           self.speed_x = 2
           self.e_up = False
           self.e_right = True
       if self.rect.x >= 500:
           self.speed_x = 0
           self.speed_y = 2
           self.e_right = False
           self.e_down = True
       # ... other patrol conditions ...
   ```

2. **Death Handling**:
   ```python
   def start_death(self):
       """Start death animation"""
       self.dying = True
       self.speed_x = 0
       self.speed_y = 0
       self.death_index = 0
   ```

3. **Animation**:
   ```python
   def update_animation(self):
       # Death animation
       if self.dying:
           if self.death_index < len(self.animations['death']) - 1:
               self.death_index += 1
               self.image = pygame.transform.scale(self.animations['death'][self.death_index],
                                                self.animations['death'][self.death_index].get_size())
           else:
               self.dead = True
               self.dying = False
           return
       # Movement animation based on direction
       if self.e_left:
           self.anim_index = (self.anim_index + 1) % 9
           anim_frame = self.animations['run_left'][self.anim_index]
           self.image = pygame.transform.scale(anim_frame, anim_frame.get_size())
       # ... animations for other directions ...
   ```

4. **Creating Grave and Key After Death**:
   ```python
   def create_grave_and_key(self):
       """Creates grave and key after enemy death"""
       from sprites.base import GameSprite
       grave = Enemy('Finals/enemy/death/death_5.png', 27, 28,
                     self.rect.x, self.rect.y + 18, 0, 0, self.animations)
       grave.dead = True
       key = GameSprite("objects/key.png", 16, 16, self.rect.x + 3, self.rect.y + 24)
       return grave, key
   ```

### Sprite Manager

The `SpriteManager` class (file `sprite_manager.py`) centralizes management of all sprites:

```python
class SpriteManager:
    """Class for centralized management of all sprites in the game"""
    def __init__(self):
        # Main group for all sprites
        self.all_sprites = pygame.sprite.Group()
        # Groups by sprite type for convenient interaction
        self.barriers = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.graves = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.decoration = pygame.sprite.Group()  # For non-interactive elements
        self.players = pygame.sprite.Group()     # For the player
        # Dictionary for quick access to groups by name
        self.groups = {
            'all': self.all_sprites,
            'barriers': self.barriers,
            'bullets': self.bullets,
            'monsters': self.monsters,
            'graves': self.graves,
            'keys': self.keys,
            'decoration': self.decoration,
            'players': self.players
        }
```

#### Key SpriteManager Methods:

1. **Adding Sprites**:
   ```python
   def add(self, sprite, *groups):
       """
       Adds sprite to specified groups and to the general all_sprites group
       :param sprite: Sprite to add
       :param groups: Group names ('barriers', 'bullets', etc.)
       """
       self.all_sprites.add(sprite)
       for group_name in groups:
           if group_name in self.groups:
               self.groups[group_name].add(sprite)
   ```

2. **Removing Sprites**:
   ```python
   def remove(self, sprite, *groups):
       """
       Removes sprite from specified groups
       :param sprite: Sprite to remove
       :param groups: Group names; if not specified - removes from all groups
       """
       if not groups:
           # If groups not specified, remove from all groups
           for group in self.groups.values():
               group.remove(sprite)
       else:
           for group_name in groups:
               if group_name in self.groups:
                   self.groups[group_name].remove(sprite)
   ```

3. **Update and Drawing**:
   ```python
   def update(self, *args, **kwargs):
       """Updates all sprites"""
       self.all_sprites.update(*args, **kwargs)
   def draw(self, surface):
       """Draws all sprites on the surface"""
       self.all_sprites.draw(surface)
   ```

4. **Group Clearing**:
   ```python
   def empty_group(self, group_name):
       """Clears specified sprite group"""
       if group_name in self.groups:
           # Get list of sprites in the group
           sprites_to_remove = list(self.groups[group_name])
           # Remove each sprite from this group
           for sprite in sprites_to_remove:
               self.groups[group_name].remove(sprite)
               # Check if this sprite exists in other groups
               in_other_groups = False
               for name, group in self.groups.items():
                   if name != group_name and name != 'all' and sprite in group:
                       in_other_groups = True
                       break
               # If sprite is not in other groups, remove it from all_sprites
               if not in_other_groups:
                   self.all_sprites.remove(sprite)
   ```

## Level Design

The `Level` class (file `level.py`) creates and manages the game level:

```python
class Level:
    """Class for creating and managing the game level"""
    def __init__(self, sprite_manager=None):
        # Use passed sprite_manager or create new one
        if sprite_manager is None:
            from sprite_manager import SpriteManager
            self.sprite_manager = SpriteManager()
        else:
            self.sprite_manager = sprite_manager
        # References to groups for backward compatibility
        self.barriers = self.sprite_manager.barriers
        self.bullets = self.sprite_manager.bullets
        self.monsters = self.sprite_manager.monsters
        self.graves = self.sprite_manager.graves
        self.keys = self.sprite_manager.keys
        # Level objects
        self.final_door = None
        self.tip_1 = None
        self.tip_2 = None
        self.tip_3 = None
        # Flags
        self.key_collected = False
        self.tip_2_visible = False
        self.tip_3_visible = False
```

#### Key Level Methods:

1. **Creating Barriers**:
   ```python
   def create_barriers(self):
       """Creating obstacles in the level"""
       barriers_data = [
           {"path": "background/barrier.png", "size": (8, 140), "pos": (427, 10)},
           {"path": "background/barrier.png", "size": (8, 140), "pos": (554, 10)},
           # ... other barriers ...
       ]
       for barrier_data in barriers_data:
           barrier = GameSprite(
               barrier_data["path"],
               barrier_data["size"][0],
               barrier_data["size"][1],
               barrier_data["pos"][0],
               barrier_data["pos"][1]
           )
           self.sprite_manager.add(barrier, 'barriers')
   ```

2. **Creating Level Objects**:
   ```python
   def create_level_objects(self, tips):
       """Creating level objects (doors, hints, etc.)"""
       self.final_door = GameSprite("objects/furniture/door.png", 35, 42, 460, 45)
       self.sprite_manager.add(self.final_door, 'decoration')
       self.tip_1 = GameSprite("objects/tip_1.png", 350, 30, 10, 350)
       self.tip_2 = GameSprite("objects/tip_2.png", 350, 30, 10, 400)
       self.tip_3 = GameSprite("objects/tip_3.png", 300, 35, 10, 450)
   ```

3. **Handling Collisions and Objectives**:
   - `check_key_collection(hero)`: Checks if player picks up the key
   - `check_bullet_collisions(tips)`: Checks collisions of projectiles with enemies and walls
   - `add_grave_and_key(grave, key)`: Adds grave and key after enemy death

## Camera

The `Camera` class (file `camera.py`) implements a camera system that follows the player:

```python
class Camera:
    def __init__(self, width, height, zoom_width=200, zoom_height=200):
        # Camera window dimensions
        self.width = width
        self.height = height
        # Camera zoom dimensions (viewport area)
        self.zoom_width = zoom_width
        self.zoom_height = zoom_height
        # Camera offset
        self.offset_x = 0
        self.offset_y = 0
        # Create surface for zoom
        self.zoom_surface = pygame.Surface((zoom_width, zoom_height))
        # Scaling (magnification) of zoom on screen
        self.scale_factor = min(width / zoom_width, height / zoom_height)
```

#### Key Camera Methods:

1. **Updating Camera Position**:
   ```python
   def update(self, target):
       # Center camera on target
       self.offset_x = target.rect.centerx - self.zoom_width // 2
       self.offset_y = target.rect.centery - self.zoom_height // 2
   ```

2. **Applying Offset to Entities**:
   ```python
   def apply(self, entity):
       # Move object relative to camera
       return pygame.Rect(
           entity.rect.x - self.offset_x,
           entity.rect.y - self.offset_y,
           entity.rect.width,
           entity.rect.height
       )
   ```

3. **Applying Offset to Rectangles**:
   ```python
   def apply_rect(self, rect):
       # Apply camera offset to rectangle (for background)
       return pygame.Rect(
           rect.x - self.offset_x,
           rect.y - self.offset_y,
           rect.width,
           rect.height
       )
   ```

### Camera Integration in Game:

```python
def render(self):
    """Render the game world"""
    if not self.finish:
        # Clear zoom surface
        self.zoom_surface.fill(BLACK)
        # Update camera to follow hero
        self.camera.update(self.hero)
        # Draw background considering camera offset
        bg_rect = pygame.Rect(0, 0, self.bg.get_width(), self.bg.get_height())
        bg_draw_rect = self.camera.apply_rect(bg_rect)
        self.zoom_surface.blit(self.bg, bg_draw_rect)

        # Draw all sprites considering camera
        for sprite in self.sprite_manager.all_sprites:
            # Get offset position for sprite
            camera_rect = self.camera.apply(sprite)
            # Draw sprite at offset position
            self.zoom_surface.blit(sprite.image, camera_rect)

        # Scale zoom_surface to screen dimensions
        pygame.transform.scale(self.zoom_surface,
                              (int(WINDOW_WIDTH), int(WINDOW_HEIGHT)),
                              self.window)
```

## UI Components

### Buttons

The `ImageButton` class (file `buttons.py`) implements interactive buttons with images:

```python
class ImageButton:
    """Class for image button"""
    def __init__(self, x, y, width, height, image_path, hover_image_path=None, sound_path=None, sound_volume=0.3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
            self.sound.set_volume(sound_volume)
        self.is_hovered = False
```

#### Key ImageButton Methods:

1. **Drawing Button**:
   ```python
   def draw(self, surface):
       """Draw button on surface"""
       current_image = self.hover_image if self.is_hovered else self.image
       surface.blit(current_image, (self.x, self.y))
   ```

2. **Checking Mouse Hover**:
   ```python
   def check_hover(self, mouse_pos):
       """Check if cursor is over button"""
       self.is_hovered = self.rect.collidepoint(mouse_pos)
   ```

3. **Handling Click**:
   ```python
   def handle_event(self, event):
       """Process mouse events for button"""
       if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
           if self.sound:
               self.sound.play()
           pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
   ```

### Hint System

For visual feedback on objectives, hints are used:

1. **Creating Hints**:
   ```python
   self.tip_1 = GameSprite("objects/tip_1.png", 350, 30, 10, 350)
   self.tip_2 = GameSprite("objects/tip_2.png", 350, 30, 10, 400)
   self.tip_3 = GameSprite("objects/tip_3.png", 300, 35, 10, 450)
   ```

2. **Updating Hint States**:
   ```python
   def update_tips(self, tips, surface):
       """Update hint states"""
       if self.tip_2_visible:
           self.tip_2.reset(surface)
       if self.tip_3_visible:
           self.tip_3.reset(surface)
   ```

3. **Changing Hints When Completing Objectives**:
   ```python
   # When hitting enemy
   self.tip_1.image = ResourceManager.load_image("objects/tip_1_done.png", (300, 30))
   # When picking up key
   self.tip_2.image = ResourceManager.load_image("objects/tip_2_done.png", (300, 30))
   self.tip_3_visible = True
   ```

## Resources

### Sprites

Sprites are divided into the following categories:

1. **Player Character**:
   - Running animations in all directions (8 frames per direction)
   - Attack animations to left and right (13 frames per direction)
   - Idle images for each direction

2. **Enemies**:
   - Movement animations in all directions (9 frames per direction)
   - Death animation (6 frames)

3. **Objects**:
   - Arrows (projectiles)
   - Barriers
   - Doors
   - Keys
   - Graves

### Sounds

The game includes sound effects:

1. **Menu Background Music**: Loaded and played in loop in the menu
2. **Button Click Sounds**: Played when buttons are clicked

```python
# Loading and playing background music in menu
self.background_music = pygame.mixer.Sound(MENU_MUSIC)
self.background_music.set_volume(0.5)  # Volume from 0.0 to 1.0
self.background_music.play(loops=-1)  # -1 means infinite repeat

# Sound for button
self.sound = pygame.mixer.Sound(sound_path)
self.sound.set_volume(sound_volume)
```

### Images

Various types of images used in game:

1. **Backgrounds**:
   - Main level background
   - Win and lose screen backgrounds
   - Menu background

2. **Interface Elements**:
   - Buttons in normal and hover states
   - Menu title
   - Hints and their active versions

3. **Level Objects**:
   - Barrier sprites
   - Door sprite
   - Key sprite

## Configuration

The `config.py` file contains game constants and settings:

```python
# Window dimensions
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

# Colors
BLACK = (0, 0, 0)

# Movement speeds
PLAYER_SPEED = 12

# Game settings
FPS = 15

# File paths
BG_IMAGE = "background/game.png"
WIN_IMAGE = "background/Winer.png"
LOSE_IMAGE = "background/Loser.png"
WIN_FON_IMAGE = "background/dungeon_menu.jpeg"
LOSE_FON_IMAGE = "background/pause_fon.png"

# Object sizes
PLAYER_SIZE = (1, 3)
ENEMY_SIZE = (27, 42)
BULLET_RIGHT_SIZE = (31, 5)
BULLET_LEFT_SIZE = (31, 5)

# Controls
CONTROLS = {
    'MOVE_UP': K_w,
    'MOVE_DOWN': K_s,
    'MOVE_LEFT': K_a,
    'MOVE_RIGHT': K_d,
    'ATTACK_LEFT': K_LEFT,
    'ATTACK_RIGHT': K_RIGHT
}
```

This organization allows easy modification of game parameters without changing the core code.

## Detailed File Analysis

### main.py

Entry point to the game, launches the menu:

```python
import pygame
import sys
from menu import Menu

def main():
    try:
        menu = Menu()
        menu.run()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
```

### menu.py

Key components:
- Pygame and audio subsystem initialization
- Loading background images and music
- Creating buttons
- Menu event handling
- Game launch

### game.py

Main game class. Contains:
- Game initialization (loading resources, creating character, enemies and level)
- Main game loop
- User input handling
- Game state updating
- Game world rendering with camera consideration
- Win and loss condition checking

### resources.py

Centralizes resource loading and management:
- `ResourceManager` for loading and scaling images
- Functions for loading player and enemy animations
- Functions for loading hints and other UI elements

### sprites/

Contains classes for all game entities:

- **base.py**: Base `GameSprite` class
- **player.py**: Player class with controls, animation and shooting
- **enemy.py**: Enemy class with automatic movement and animations
- **bullet.py**: Projectile class (arrow)

### sprite_manager.py

Manages sprite groups:
- Creates separate groups for different object types
- Provides interface for adding/removing sprites
- Manages drawing and updating of all sprites

### level.py

Creates and manages game level:
- Describes barrier and object placement
- Manages game objectives
- Processes projectile collisions
- Tracks key collection and door reaching

### camera.py

Implements follow camera:
- Follows the player
- Transforms world coordinates to screen coordinates
- Supports viewport scaling

### buttons.py

Implements interactive buttons for menu:
- Support for images in normal and hover states
- Sound effects on click
- Event generation on click

### config.py

Contains all game constants and settings:
- Screen dimensions
- Frame rate
- Resource paths
- Control settings
- Object sizes

## Conclusion

The "Dungeon Master" project demonstrates implementation of the following concepts:

1. **Code Structure**: Division of functionality into classes and modules
2. **Resource Management**: Centralized loading and management of resources
3. **Sprite Animation**: System for switching animation frames
4. **Collision Detection**: Various types of interactions between objects
5. **Camera**: Implementation of follow camera with scaling
6. **Controls**: Responsive control system with diagonal movement support
7. **User Interface**: Interactive buttons and hints
8. **Game States**: Management of different states (menu, game, win, loss)

These principles can be applied in the development of other 2D games on Pygame, even with completely different mechanics and visual style.