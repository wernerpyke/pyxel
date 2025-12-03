# Introduction — more about `pyke_pyxel`

`pyke_pyxel` provides a small, practical toolkit for building tile-and-sprite games
on top of the Pyxel runtime. The package is intentionally lightweight but focuses on
the pieces you need day-to-day: a `Game` runner that manages the loop and screens,
a simple column/row coordinate (`coord`) and `Map` model,
`Sprite` classes and utilities for animated characters, `HUD` helpers for on-screen status, 
`FX` utilities for transient visual effects, and a `Signals` mechanism for decoupled event handling.

1) ***Game: the application shell***
--------------------------------
Start with `Game` — it provides the application lifecycle (initialization,
update, draw) and a place to register screens or states. A typical pattern is to instantiate `Game` and 
register a title screen, gameplay screen and a pause/menu screen. 
The `Game` object owns the Pyxel window and drives the tick/update loop; it will call your current screen's update and draw methods each frame. Treat `Game` as the single source of truth for game-wide
resources (loaded assets, global settings and top-level managers).

The `Game` object is configured via a `GameSettings` instance.

For example:

```
from pyke_pyxel import COLOURS, GameSettings
from pyke_pyxel.game import Game

settings = GameSettings()

settings.size.window = 320
settings.fps.game = 60

settings.colours.background = COLOURS.BLACK
settings.colours.sprite_transparency = COLOURS.BEIGE

settings.mouse_enabled = True
settings.display_smoothing_enabled = True
settings.full_screen_enabled = False

game = Game(settings=settings, 
        title="My Game", 
        resources=f"/path/to/game_assets.pyxres")

game.start()
```

2) ***Signals: decoupled messaging***
--------------------------------
`Signals` implements a simple pub/sub mechanism so parts of your game can
communicate without direct references. For example, the player sprite can emit
an "item_collected" signal with a payload, any interested HUD or inventory
manager can subscribe and update state. Signals are great for wiring UI, audio
triggers and cross-cutting behaviours without coupling modules together.

For example:

```
from pyke_pyxel.signals import Signals

# Game() configuration and creation as per above example:
# game = Game(...) etc

def game_start(game: Game):
    # Implement game start logic here
    pass

def game_update(game: Game):
    # Implement game loop update logic here
    pass

Signals.connect(Signals.GAME.WILL_START, game_star)
Signals.connect(Signals.GAME.UPDATE, game_update)

game.start()
```

You can also define your own custom signals, for example:

```
def my_handler(sent_from):
    # do something

Signals.connect("my_signal", my_handler)


# somewhere else
Signals.send("my_signal", sender_object)

def another_handler(sent_from, value:Any)
    # 'value' can be anything, e.g. a tuple or class instance


Signals.connect("another_signal", another_handler)

# somewhere else
Signals.send("another_signal", sender_object, parameter_value)

```

3) ***coord and Map: grid math and spatial queries***
-----------------------------------------------
Each game represents its world using a square grid of columns and rows.
Each column/row is represented by a `coord` which makes positioning and moving sprites simple. 
`coord` also stores an internal `x`/`y` representation including useful properties `x`, `y`, `mid_x`, `mid_y`, `min_x`, `max_x`, 
and convenience methods like `contains`, `collides_with`, `clone`, and `move_by` for simple positional math.
Use factory helpers `coord.with_center` or `coord.with_xy` when you need to translate between 
pixel coordinates and the tile grid.
The `Map` class stores the status and sprite of each `coord` in the form of a `MapLocation` with statuses such as `FREE`, `BLOCKED`, `OPEN` and `CLOSED`.
Convenience methods on `Map` make common spatial tasks easy and readable. These include `is_blocked`, `is_openable`, `location_at`, `location_left_of`, `location_right_of`, `location_above`, `location_below` and others.

For example:
```

from pyke_pyxel import coord

# Game initialisation as per above example

def game_update(game: Game):
    c = coord(col=10, row=10)

    map = game.map
    if map.is_blocked(c):
        # do something

    c2 = my_sprite.position
    c2.move_by(x=10)

    if c.collides_with(c2):
        # do something

```

4) ***Sprite: characters, objects and animations***
---------------------------------------------
`Sprite` is the primary building block for visible entities. Sprites hold a
current frame and a dictionary of named `Animation` objects. Use `add_animation`
to register walk, attack, or idle animations, and `activate_animation` to start
them (optionally looping or invoking a callback when complete). `MovableSprite`
provides helpers for directional animations and a movement speed; `OpenableSprite`
models objects with open/closed states (doors, chests).

Typical usage:
- create a `Sprite` with an idle frame (a `coord` into a resource sheet),
- add animations (start frame and frame count),
- set the sprite's `position` to a `coord` (grid-aware)

For example:
```
from pyke_pyxel.sprite import Sprite

# the default frame of the sprite is located at col 1, row 1 of the image resource sheet
default_frame = coord(1, 1) 
my_sprite = Sprite("player", default_frame)

# The walk animation starts at col 2, row 1 and has four frames
walk = Animation(coord(2, 1), frames=4)
my_sprite.add_animation("walk", walk)

def game_start(game: Game):
    my_sprite.set_position(coord.with_xy(100, 40))
    game.add_sprite(my_sprite)

def game_update(game: Game):
    my_sprite.activate_animation("walk")
    
    # Move down one pixel per update (@ 60 FPS)
    my_sprite.position.c2.move_by(y=1)
```

6) ***HUD & UI: present game state to the player***
----------------------------------------
The `HUD` utilities make it easy to display player health, inventory, scores and
other overlays. A HUD is typically updated from the same game state that drives
your logic and drawn last so it appears above world sprites. 

UI-related classes are provided in `Image`, `Button` and `Rect`.
- `Image` draws an image from a resouce image sheet
- `Button` uses `Image` instances to represent `up` and `down` states and offers support for icon and text overlays.
- `Rect` provides the ability to draw rectangles with/without borders.

Keep HUD code
separate from game logic: write small presenter functions that turn internal
state into text/tiles and hand them to the HUD renderer each frame.

For example:
```
from pyke_pyxel.drawable import ImageFactory, Image, Button

def game_started(game: Game):

    logo = Image(frame=coord(1, 1), 
                cols=24, 
                rows=10, 
                image_index=1)
    game.hud.add_bg(logo)

    imgs = ImageFactory(cols=16, rows=4, image_index=1)
    start_button = Button(name="start_button", 
                    up=imgs.at(coord(1, 11)), 
                    down=imgs.at(coord(17, 11)))
    start_button.set_position(coord(12, 24))
    game.hud.add_button(start_button)

```

7) ***Mouse Input***
---------------------------------

Setting `mouse_enabled = True` in `GameSettings` will cause the game to emit the following signals: `Signals.MOUSE.MOVE`, `Signals.MOUSE.DOWN` and `Signals.MOUSE.UP`. These can be received by connecting to the relevant signals.

For example:
```

# Remember to set mouse_enabled = True in GameSettings

def mouse_move(game: Game, value: tuple[int, int]):
    x, y = value[0], value[1]
    # do something

def mouse_down(game: Game, value: tuple[int, int]):
    x, y = value[0], value[1]
    # do something

def mouse_up(game: Game):
    # do something

Signals.connect(Signals.MOUSE.MOVE, mouse_move)
Signals.connect(Signals.MOUSE.DOWN, mouse_down)
Signals.connect(Signals.MOUSE.UP, mouse_up)

```

1) ***FX: short-lived visual effects***
---------------------------------
Use `FX` helpers for transient effects and animated overlays. FX objects are lightweight and intended to be created
on-the-fly by gameplay events (e.g. an sprite collision spawns a splatter FX instance which lives
for its duration and then disappears).

A given FX may emit a provided signal when it completes to allow the implementation to react to the end of the effect.

For example
```
def start_button_mouse_clicked(game: Game):
    game.fx.circular_wipe(colour=COLOURS.BLUE_DARK, 
                            wipe_closed=True, completion_signal="ui_game_screen_fade_in_complete")

```