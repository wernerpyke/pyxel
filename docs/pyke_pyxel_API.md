# None

## API Reference

* [signals](#pyke_pyxel.signals)
  * [Signals](#pyke_pyxel.signals.Signals)
    * [connect](#pyke_pyxel.signals.Signals.connect)
    * [send](#pyke_pyxel.signals.Signals.send)
    * [send\_with](#pyke_pyxel.signals.Signals.send_with)
* [\_button](#pyke_pyxel.drawable._button)
  * [Button](#pyke_pyxel.drawable._button.Button)
    * [contains](#pyke_pyxel.drawable._button.Button.contains)
    * [push\_down](#pyke_pyxel.drawable._button.Button.push_down)
    * [pop\_up](#pyke_pyxel.drawable._button.Button.pop_up)
    * [set\_position](#pyke_pyxel.drawable._button.Button.set_position)
    * [position](#pyke_pyxel.drawable._button.Button.position)
* [game](#pyke_pyxel.game)
  * [Game](#pyke_pyxel.game.Game)
    * [\_\_init\_\_](#pyke_pyxel.game.Game.__init__)
    * [start](#pyke_pyxel.game.Game.start)
    * [clear\_all](#pyke_pyxel.game.Game.clear_all)
    * [add\_sprite](#pyke_pyxel.game.Game.add_sprite)
    * [remove\_sprite](#pyke_pyxel.game.Game.remove_sprite)
    * [remove\_sprite\_by\_id](#pyke_pyxel.game.Game.remove_sprite_by_id)
    * [set\_tilemap](#pyke_pyxel.game.Game.set_tilemap)
    * [pause](#pyke_pyxel.game.Game.pause)
    * [unpause](#pyke_pyxel.game.Game.unpause)
    * [start\_music](#pyke_pyxel.game.Game.start_music)
    * [stop\_music](#pyke_pyxel.game.Game.stop_music)
    * [map](#pyke_pyxel.game.Game.map)
    * [hud](#pyke_pyxel.game.Game.hud)
    * [fx](#pyke_pyxel.game.Game.fx)
    * [update](#pyke_pyxel.game.Game.update)
    * [draw](#pyke_pyxel.game.Game.draw)
* [game](#pyke_pyxel.rpg.game)
  * [RPGGame](#pyke_pyxel.rpg.game.RPGGame)
    * [\_\_init\_\_](#pyke_pyxel.rpg.game.RPGGame.__init__)
* [map](#pyke_pyxel.map)
  * [Map](#pyke_pyxel.map.Map)
    * [sprite\_can\_move\_to](#pyke_pyxel.map.Map.sprite_can_move_to)
    * [mark\_blocked](#pyke_pyxel.map.Map.mark_blocked)
    * [mark\_openable](#pyke_pyxel.map.Map.mark_openable)
    * [mark\_closed](#pyke_pyxel.map.Map.mark_closed)
    * [mark\_open](#pyke_pyxel.map.Map.mark_open)
    * [is\_blocked](#pyke_pyxel.map.Map.is_blocked)
    * [is\_openable](#pyke_pyxel.map.Map.is_openable)
    * [adjacent\_openable](#pyke_pyxel.map.Map.adjacent_openable)
    * [openable\_sprite\_at](#pyke_pyxel.map.Map.openable_sprite_at)
    * [sprite\_at](#pyke_pyxel.map.Map.sprite_at)
    * [location\_at](#pyke_pyxel.map.Map.location_at)
    * [location\_left\_of](#pyke_pyxel.map.Map.location_left_of)
    * [location\_right\_of](#pyke_pyxel.map.Map.location_right_of)
    * [location\_above](#pyke_pyxel.map.Map.location_above)
    * [location\_below](#pyke_pyxel.map.Map.location_below)
    * [x\_is\_left\_of\_center](#pyke_pyxel.map.Map.x_is_left_of_center)
    * [y\_is\_above\_center](#pyke_pyxel.map.Map.y_is_above_center)
    * [bound\_to\_width](#pyke_pyxel.map.Map.bound_to_width)
    * [bound\_to\_height](#pyke_pyxel.map.Map.bound_to_height)
    * [shortest\_distance\_to\_sides](#pyke_pyxel.map.Map.shortest_distance_to_sides)
    * [random\_distance\_to\_right](#pyke_pyxel.map.Map.random_distance_to_right)
    * [random\_distance\_to\_left](#pyke_pyxel.map.Map.random_distance_to_left)
    * [random\_distance\_down](#pyke_pyxel.map.Map.random_distance_down)
    * [height](#pyke_pyxel.map.Map.height)
    * [width](#pyke_pyxel.map.Map.width)
    * [center\_x](#pyke_pyxel.map.Map.center_x)
    * [center\_y](#pyke_pyxel.map.Map.center_y)
    * [right\_x](#pyke_pyxel.map.Map.right_x)
    * [bottom\_y](#pyke_pyxel.map.Map.bottom_y)
* [matrix](#pyke_pyxel.cell_auto.matrix)
  * [Cell](#pyke_pyxel.cell_auto.matrix.Cell)
    * [reset](#pyke_pyxel.cell_auto.matrix.Cell.reset)
    * [store\_state](#pyke_pyxel.cell_auto.matrix.Cell.store_state)
    * [recall\_state](#pyke_pyxel.cell_auto.matrix.Cell.recall_state)
  * [Matrix](#pyke_pyxel.cell_auto.matrix.Matrix)
    * [clear](#pyke_pyxel.cell_auto.matrix.Matrix.clear)
    * [neighbour\_N](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_N)
    * [neighbour\_S](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_S)
    * [neighbour\_E](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_E)
    * [neighbour\_W](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_W)
    * [neighbour\_NE](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_NE)
    * [neighbour\_NW](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_NW)
    * [neighbour\_SE](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_SE)
    * [neighbour\_SW](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_SW)
    * [neighbours](#pyke_pyxel.cell_auto.matrix.Matrix.neighbours)
    * [cell\_at](#pyke_pyxel.cell_auto.matrix.Matrix.cell_at)
    * [cells\_at](#pyke_pyxel.cell_auto.matrix.Matrix.cells_at)
    * [cells\_in\_line](#pyke_pyxel.cell_auto.matrix.Matrix.cells_in_line)
* [game](#pyke_pyxel.cell_auto.game)
  * [CellAutoGame](#pyke_pyxel.cell_auto.game.CellAutoGame)
    * [\_\_init\_\_](#pyke_pyxel.cell_auto.game.CellAutoGame.__init__)
* [\_rpg\_sprites](#pyke_pyxel.sprite._rpg_sprites)
  * [OpenableSprite](#pyke_pyxel.sprite._rpg_sprites.OpenableSprite)
  * [MovableSprite](#pyke_pyxel.sprite._rpg_sprites.MovableSprite)
* [\_sprite](#pyke_pyxel.sprite._sprite)
  * [Animation](#pyke_pyxel.sprite._sprite.Animation)
  * [Sprite](#pyke_pyxel.sprite._sprite.Sprite)
    * [add\_animation](#pyke_pyxel.sprite._sprite.Sprite.add_animation)
    * [activate\_animation](#pyke_pyxel.sprite._sprite.Sprite.activate_animation)
    * [pause\_animation](#pyke_pyxel.sprite._sprite.Sprite.pause_animation)
    * [unpause\_animation](#pyke_pyxel.sprite._sprite.Sprite.unpause_animation)
    * [deactivate\_animations](#pyke_pyxel.sprite._sprite.Sprite.deactivate_animations)
    * [set\_position](#pyke_pyxel.sprite._sprite.Sprite.set_position)
    * [position](#pyke_pyxel.sprite._sprite.Sprite.position)
* [\_compound\_sprite](#pyke_pyxel.sprite._compound_sprite)
  * [CompoundSprite](#pyke_pyxel.sprite._compound_sprite.CompoundSprite)
    * [fill\_tiles](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill_tiles)
    * [fill\_col](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill_col)
    * [fill\_row](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill_row)
    * [set\_tile](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.set_tile)
    * [clear\_graphics](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.clear_graphics)
    * [graph\_rect](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.graph_rect)
    * [graph\_triangle](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.graph_triangle)
    * [set\_position](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.set_position)
    * [position](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.position)
* [\_text\_sprite](#pyke_pyxel.sprite._text_sprite)
  * [TextSprite](#pyke_pyxel.sprite._text_sprite.TextSprite)
    * [set\_position](#pyke_pyxel.sprite._text_sprite.TextSprite.set_position)
    * [position](#pyke_pyxel.sprite._text_sprite.TextSprite.position)
    * [set\_text](#pyke_pyxel.sprite._text_sprite.TextSprite.set_text)
* [hud](#pyke_pyxel.hud)
  * [HUD](#pyke_pyxel.hud.HUD)
    * [add\_text](#pyke_pyxel.hud.HUD.add_text)
    * [add\_sprite](#pyke_pyxel.hud.HUD.add_sprite)
    * [remove\_sprite](#pyke_pyxel.hud.HUD.remove_sprite)
    * [add\_button](#pyke_pyxel.hud.HUD.add_button)
    * [remove\_button](#pyke_pyxel.hud.HUD.remove_button)
    * [add\_image](#pyke_pyxel.hud.HUD.add_image)
    * [remove\_image](#pyke_pyxel.hud.HUD.remove_image)
* [fx](#pyke_pyxel.fx)
  * [FX](#pyke_pyxel.fx.FX)
    * [circular\_wipe](#pyke_pyxel.fx.FX.circular_wipe)
    * [splatter](#pyke_pyxel.fx.FX.splatter)
* [\_base\_types](#pyke_pyxel._base_types)
  * [ColourSettings](#pyke_pyxel._base_types.ColourSettings)
    * [sprite\_transparency](#pyke_pyxel._base_types.ColourSettings.sprite_transparency)
    * [background](#pyke_pyxel._base_types.ColourSettings.background)
    * [hud\_text](#pyke_pyxel._base_types.ColourSettings.hud_text)
  * [Coord](#pyke_pyxel._base_types.Coord)
    * [\_\_init\_\_](#pyke_pyxel._base_types.Coord.__init__)
    * [with\_center](#pyke_pyxel._base_types.Coord.with_center)
    * [with\_xy](#pyke_pyxel._base_types.Coord.with_xy)
    * [is\_different\_grid\_location](#pyke_pyxel._base_types.Coord.is_different_grid_location)
    * [is\_same\_grid\_location](#pyke_pyxel._base_types.Coord.is_same_grid_location)
    * [contains](#pyke_pyxel._base_types.Coord.contains)
    * [move\_by](#pyke_pyxel._base_types.Coord.move_by)
    * [clone](#pyke_pyxel._base_types.Coord.clone)
    * [clone\_by](#pyke_pyxel._base_types.Coord.clone_by)
    * [collides\_with](#pyke_pyxel._base_types.Coord.collides_with)
    * [distance\_to](#pyke_pyxel._base_types.Coord.distance_to)
    * [x](#pyke_pyxel._base_types.Coord.x)
    * [y](#pyke_pyxel._base_types.Coord.y)
    * [mid\_x](#pyke_pyxel._base_types.Coord.mid_x)
    * [mid\_y](#pyke_pyxel._base_types.Coord.mid_y)
    * [min\_x](#pyke_pyxel._base_types.Coord.min_x)
    * [min\_y](#pyke_pyxel._base_types.Coord.min_y)
    * [max\_x](#pyke_pyxel._base_types.Coord.max_x)
    * [max\_y](#pyke_pyxel._base_types.Coord.max_y)

<a id="pyke_pyxel.signals"></a>

# signals

<a id="pyke_pyxel.signals.Signals"></a>

## Signals Objects

```python
class Signals()
```

Signal management system for game events.
This class provides a centralized signal dispatching mechanism for various game events,
organizing signals into categories (GAME, MOUSE) and providing methods
to connect listeners and send signals with optional parameters.

**Attributes**:

- `GAME` - Dataclass containing game-level signal constants
  - WILL_START: Signal emitted before game initialization
  - UPDATE: Signal emitted on each game update cycle
  - SPRITE_REMOVED: Signal emitted when a sprite is removed from the game
- `MOUSE` - Dataclass containing mouse input signal constants
  - DOWN: Signal emitted on mouse button down
  - UP: Signal emitted on mouse button up
  - MOVE: Signal emitted on mouse movement
  
  RPG-Specific Attributes:
- `PLAYER` - Dataclass containing player-related signal constants
  - BLOCKED: Signal emitted when player movement is blocked
  - INTERACT_OPENABLE: Signal emitted when player can interact with openable objects
  - ATTACK: Signal emitted when player performs an attack action
- `ENEMY` - Dataclass containing enemy-related signal constants
  - BLOCKED: Signal emitted when enemy movement is blocked

<a id="pyke_pyxel.signals.Signals.connect"></a>

#### connect

```python
@staticmethod
def connect(name: str, listener: Callable)
```

Connect a listener callback to a named signal

<a id="pyke_pyxel.signals.Signals.send"></a>

#### send

```python
@staticmethod
def send(name: str, sender: Any|None)
```

Send a signal with a sender object

<a id="pyke_pyxel.signals.Signals.send_with"></a>

#### send\_with

```python
@staticmethod
def send_with(name: str, sender: Any|None, other: Optional[Any] = None)
```

Send a signal with additional optional data

<a id="pyke_pyxel.drawable._button"></a>

# \_button

<a id="pyke_pyxel.drawable._button.Button"></a>

## Button Objects

```python
class Button()
```

<a id="pyke_pyxel.drawable._button.Button.contains"></a>

#### contains

```python
def contains(x: int, y: int) -> bool
```

Checks if the given coordinates are within the bounds of the button.

**Arguments**:

- `x` _int_ - The x-coordinate to check.
- `y` _int_ - The y-coordinate to check.
  

**Returns**:

- `bool` - True if the coordinates are within the button's bounds, False otherwise.

<a id="pyke_pyxel.drawable._button.Button.push_down"></a>

#### push\_down

```python
def push_down()
```

Sets the button's state to 'down', drawing the down frame.

<a id="pyke_pyxel.drawable._button.Button.pop_up"></a>

#### pop\_up

```python
def pop_up()
```

Sets the button's state to 'up', drawing the up frame.

<a id="pyke_pyxel.drawable._button.Button.set_position"></a>

#### set\_position

```python
def set_position(position: Coord)
```

Sets the position of the button.

**Arguments**:

- `position` _Coord_ - The new coordinate for the button's top-left corner.

<a id="pyke_pyxel.drawable._button.Button.position"></a>

#### position

```python
@property
def position() -> Coord
```

Returns the current position of the button.

**Returns**:

- `Coord` - The coordinate of the button's top-left corner.

<a id="pyke_pyxel.game"></a>

# game

<a id="pyke_pyxel.game.Game"></a>

## Game Objects

```python
class Game()
```

Game class that manages the core game loop, sprite management, and rendering.
This class serves as the main controller for a Pyxel-based game, handling initialization,
sprite lifecycle management, signal connections, and the update/draw loop. It manages
game settings, sprites, tile maps, HUD, and visual effects.

Signals:
    - `GAME.WILL_START`: Emitted before the game loop begins.
    - `GAME.UPDATE`: Emitted on every update frame.
    - `MOUSE.MOVE`: Sent when mouse position changes, enabled by `GameSettings.mouse_enabled`.
    - `MOUSE.DOWN`: Sent on left mouse button press, enabled by `GameSettings.mouse_enabled`.
    - `MOUSE.UP`: Sent on left mouse button release, enabled by `GameSettings.mouse_enabled`.

<a id="pyke_pyxel.game.Game.__init__"></a>

#### \_\_init\_\_

```python
def __init__(settings: GameSettings, title: str, resources: str)
```

Initialize the Game instance.

**Arguments**:

- `settings` _GameSettings_ - Configuration object containing debug flag, window and tile sizes,
  and FPS settings (game and animation). Also used to determine whether mouse input is enabled.
- `title` _str_ - Window title passed to pyxel.init.
- `resources` _str_ - Path to a resources file that will be loaded with pyxel.load.

<a id="pyke_pyxel.game.Game.start"></a>

#### start

```python
def start()
```

Initializes and starts the game loop.

Sends a signal indicating the game is about to start, then begins the main
update and draw loop using Pyxel's run function.

Signals:
    Signals.GAME.WILL_START: Sent before the game loop starts.

<a id="pyke_pyxel.game.Game.clear_all"></a>

#### clear\_all

```python
def clear_all()
```

Clear all sprites, TileMap, HUD and FX

<a id="pyke_pyxel.game.Game.add_sprite"></a>

#### add\_sprite

```python
def add_sprite(sprite: Sprite|CompoundSprite)
```

Add a sprite to the game's sprite collection.

**Arguments**:

- `sprite` _Sprite | CompoundSprite_ - The sprite object to add to the game.
  Can be either a single Sprite or a CompoundSprite containing multiple sprites.

<a id="pyke_pyxel.game.Game.remove_sprite"></a>

#### remove\_sprite

```python
def remove_sprite(sprite: Sprite|CompoundSprite)
```

Remove a sprite from the game's active sprite collection.

**Arguments**:

  sprite : Sprite | CompoundSprite
  The sprite (or compound sprite) instance to remove from the game's internal
  sprite list.

<a id="pyke_pyxel.game.Game.remove_sprite_by_id"></a>

#### remove\_sprite\_by\_id

```python
def remove_sprite_by_id(sprite_id: int)
```

Remove the first sprite with the specified identifier from the game's sprite list.

**Arguments**:

  sprite_id : int
  The identifier of the sprite to remove.

<a id="pyke_pyxel.game.Game.set_tilemap"></a>

#### set\_tilemap

```python
def set_tilemap(resource_position: Coord, tiles_wide: int, tiles_high: int, resource_tilemap_index: int = 0)
```

Set a simplified version of standard Pyxel tilemaps as a background layer.
The tilemap is horizontally and vertically repeated to fill up the screen width/height.

For example:
`game.set_tilemap(Coord(10, 8), 4, 6)`
will fetch a tilemap starting at column 10 and row 8 of the resource sheet and
load 4 columns and 6 rows which will then be repeated to fill the screen.

**Arguments**:

  resource_position : Coord
  The col/row position of the tilemap in the loaded resource sheet
  tiles_wide : int
  The width of the tilemap on the resource sheet
  tiles_high : int
  The height of the tilemap on the resource sheet
  resource_tilemap_index : int
  The index of the tilemap in the resource bundle

<a id="pyke_pyxel.game.Game.pause"></a>

#### pause

```python
def pause()
```

Pause the game loop.
This will pause:
- Game logic update signals
- Sprite animation

But will not halt:
- Keyboard and mouse input signals
- Screen draw
- Music

<a id="pyke_pyxel.game.Game.unpause"></a>

#### unpause

```python
def unpause()
```

Unpause the game loop.

<a id="pyke_pyxel.game.Game.start_music"></a>

#### start\_music

```python
def start_music(number: int)
```

Starts the music identified by the provided number. Music loops until `stop_music` is called.

<a id="pyke_pyxel.game.Game.stop_music"></a>

#### stop\_music

```python
def stop_music()
```

Stops the currently playing music

<a id="pyke_pyxel.game.Game.map"></a>

#### map

```python
@property
def map() -> Map
```

Returns the `Map` instance for this game

<a id="pyke_pyxel.game.Game.hud"></a>

#### hud

```python
@property
def hud() -> HUD
```

Returns the `HUD` instance for this game

<a id="pyke_pyxel.game.Game.fx"></a>

#### fx

```python
@property
def fx() -> FX
```

Returns the `FX` instance for this game

<a id="pyke_pyxel.game.Game.update"></a>

#### update

```python
def update()
```

Pyxel lifecycle handler. Updates the game state for each frame.

Signals:
    - GAME.UPDATE: Sent every update.
    - MOUSE.MOVE: Emitted when mouse position changes (if mouse_enabled).
    - MOUSE.DOWN: Emitted on left mouse button press (if mouse_enabled).
    - MOUSE.UP: Emitted on left mouse button release (if mouse_enabled).

<a id="pyke_pyxel.game.Game.draw"></a>

#### draw

```python
def draw()
```

Pyxel lifecycle handler. Render the current frame by drawing all visual components in order.
Draws the background, sprites, HUD, and active visual effects.

<a id="pyke_pyxel.rpg.game"></a>

# game

<a id="pyke_pyxel.rpg.game.RPGGame"></a>

## RPGGame Objects

```python
class RPGGame(Game)
```

<a id="pyke_pyxel.rpg.game.RPGGame.__init__"></a>

#### \_\_init\_\_

```python
def __init__(settings: GameSettings, title: str, resources: str)
```

Specialised sub-class of `pyke_pyxel.Game` which adds basic room- and actor-based RPG mechanics.

Keyboard:
- Direction arrows: movement up, down, left, right
- Z-key: player attack (e.g. projectile)
- X-key: player interaction (e.g. open door)

**Attributes**:

- `player` _Player_ - The player character. Use set_player() to assign the player instance.
- `room` _Room_ - The current room/map the player is in. Automatically initialized with the game map.
  

**Arguments**:

- `settings` _GameSettings_ - The game settings configuration.
- `title` _str_ - The title of the game window.
- `resources` _str_ - The path to the resources directory.

<a id="pyke_pyxel.map"></a>

# map

<a id="pyke_pyxel.map.Map"></a>

## Map Objects

```python
class Map()
```

<a id="pyke_pyxel.map.Map.sprite_can_move_to"></a>

#### sprite\_can\_move\_to

```python
def sprite_can_move_to(coord: Coord) -> bool
```

Determine if a sprite can move to the specified coordinate.

Checks the status of the location at the given coordinate and returns True
if the sprite is able to move there (i.e., the location is either `FREE` or `OPEN`).

**Arguments**:

- `coord` _Coord_ - The coordinate to check for sprite movement.
  

**Returns**:

- `bool` - True if the location is `FREE` or `OPEN`, False otherwise.

<a id="pyke_pyxel.map.Map.mark_blocked"></a>

#### mark\_blocked

```python
def mark_blocked(coord: Coord, sprite: Sprite)
```

Mark the location at the given coordinate as blocked and attach a sprite.

This updates the Location object returned by self.location_at(coord) by:
- setting its status to `LOCATION_STATUS.BLOCKED`
- assigning the provided sprite to its sprite attribute

**Arguments**:

- `coord` _Coord_ - The coordinate of the location to mark as blocked.
- `sprite` _Sprite_ - The sprite to place on the blocked location (e.g. an obstacle graphic).

<a id="pyke_pyxel.map.Map.mark_openable"></a>

#### mark\_openable

```python
def mark_openable(coord: Coord, sprite: OpenableSprite, closed: bool)
```

Mark a location as an openable object with the specified status.

**Arguments**:

- `coord` _Coord_ - The coordinate of the location to mark.
- `sprite` _OpenableSprite_ - The sprite to assign to the openable object.
- `closed` _bool_ - Whether the openable object is closed (True) or open (False).

<a id="pyke_pyxel.map.Map.mark_closed"></a>

#### mark\_closed

```python
def mark_closed(coord: Coord)
```

Mark a location as closed.

<a id="pyke_pyxel.map.Map.mark_open"></a>

#### mark\_open

```python
def mark_open(coord: Coord)
```

Mark a location as open.

<a id="pyke_pyxel.map.Map.is_blocked"></a>

#### is\_blocked

```python
def is_blocked(coord: Coord) -> bool
```

Check if a location is blocked

<a id="pyke_pyxel.map.Map.is_openable"></a>

#### is\_openable

```python
def is_openable(coord: Coord) -> bool
```

Check if a location is openable

<a id="pyke_pyxel.map.Map.adjacent_openable"></a>

#### adjacent\_openable

```python
def adjacent_openable(coord: Coord) -> Optional[OpenableSprite]
```

Check if a location adjacent(UP, DOWN, LEFT, RIGHT) to the provided coordinate is openable

<a id="pyke_pyxel.map.Map.openable_sprite_at"></a>

#### openable\_sprite\_at

```python
def openable_sprite_at(coord: Coord) -> Optional[OpenableSprite]
```

Return the `OpenableSprite` at a coordinate

<a id="pyke_pyxel.map.Map.sprite_at"></a>

#### sprite\_at

```python
def sprite_at(coord: Coord) -> Optional[Sprite]
```

Return the `Sprite` at a coordinate

<a id="pyke_pyxel.map.Map.location_at"></a>

#### location\_at

```python
def location_at(coord: Coord) -> MapLocation
```

Return the `MapLocation` at a coordinate

<a id="pyke_pyxel.map.Map.location_left_of"></a>

#### location\_left\_of

```python
def location_left_of(coord: Coord) -> Optional[MapLocation]
```

Return the location LEFT of the coordinate

<a id="pyke_pyxel.map.Map.location_right_of"></a>

#### location\_right\_of

```python
def location_right_of(coord: Coord) -> Optional[MapLocation]
```

Return the location RIGHT of the coordinate

<a id="pyke_pyxel.map.Map.location_above"></a>

#### location\_above

```python
def location_above(coord: Coord) -> Optional[MapLocation]
```

Return the location UP from of the coordinate

<a id="pyke_pyxel.map.Map.location_below"></a>

#### location\_below

```python
def location_below(coord: Coord) -> Optional[MapLocation]
```

Return the location DOWN from of the coordinate

<a id="pyke_pyxel.map.Map.x_is_left_of_center"></a>

#### x\_is\_left\_of\_center

```python
def x_is_left_of_center(x: int) -> bool
```

Return true if `x` is to the left of the center of the map

<a id="pyke_pyxel.map.Map.y_is_above_center"></a>

#### y\_is\_above\_center

```python
def y_is_above_center(y: int) -> bool
```

Return true if `y` is above the center of the map

<a id="pyke_pyxel.map.Map.bound_to_width"></a>

#### bound\_to\_width

```python
def bound_to_width(x: int) -> int
```

Check that `x` falls into the bounds of the map and return a safe value (max x of the map) if it does not

<a id="pyke_pyxel.map.Map.bound_to_height"></a>

#### bound\_to\_height

```python
def bound_to_height(y: int) -> int
```

Check that `y` falls into the bounds of the map and return a safe value (max y of the map) if it does not

<a id="pyke_pyxel.map.Map.shortest_distance_to_sides"></a>

#### shortest\_distance\_to\_sides

```python
def shortest_distance_to_sides(from_x: int) -> int
```

Return the shortest distance to the sides of the map (either left or right)

<a id="pyke_pyxel.map.Map.random_distance_to_right"></a>

#### random\_distance\_to\_right

```python
def random_distance_to_right(from_x: int, min: int, max: int) -> int
```

Generate a random distance to the right of `from_x` where the random distance falls between `min` and `max` without exceeding the bounds of the map.

<a id="pyke_pyxel.map.Map.random_distance_to_left"></a>

#### random\_distance\_to\_left

```python
def random_distance_to_left(from_x: int, min: int, max: int) -> int
```

Generate a random distance to the left of `from_x` where the random distance falls between `min` and `max` without exceeding the bounds of the map.

<a id="pyke_pyxel.map.Map.random_distance_down"></a>

#### random\_distance\_down

```python
def random_distance_down(from_y: int, min: int, max: int) -> int
```

Generate a random distance down of `from_y` where the random distance falls between `min` and `max` without exceeding the bounds of the map.

<a id="pyke_pyxel.map.Map.height"></a>

#### height

```python
@property
def height() -> int
```

Height of the map

<a id="pyke_pyxel.map.Map.width"></a>

#### width

```python
@property
def width() -> int
```

Width of the map

<a id="pyke_pyxel.map.Map.center_x"></a>

#### center\_x

```python
@property
def center_x() -> int
```

Horizontal center point of the map

<a id="pyke_pyxel.map.Map.center_y"></a>

#### center\_y

```python
@property
def center_y() -> int
```

Vertical center point of the map

<a id="pyke_pyxel.map.Map.right_x"></a>

#### right\_x

```python
@property
def right_x() -> int
```

Right-most `x` point of the map

<a id="pyke_pyxel.map.Map.bottom_y"></a>

#### bottom\_y

```python
@property
def bottom_y() -> int
```

Bottom-most `y` point of the map

<a id="pyke_pyxel.cell_auto.matrix"></a>

# matrix

<a id="pyke_pyxel.cell_auto.matrix.Cell"></a>

## Cell Objects

```python
class Cell()
```

A Cell represents a single unit in a cellular automaton grid.
Each cell has a position (x, y) in a 2D grid and maintains both current and stored state.
The cell can be rendered to a pyxel Image and tracks properties like type, color, propagation,
and power for use in cellular automaton simulations.

**Attributes**:

- `x` _int_ - The x-coordinate of the cell in the grid.
- `y` _int_ - The y-coordinate of the cell in the grid.
- `type` _str_ - The current type/state of the cell (default: "empty").
- `colour` _int_ - The current color value of the cell (default: 0).
- `can_propogate` _bool_ - Whether this cell can propagate its state (default: False).
- `power` _float_ - A power or intensity value for the cell (default: 0).
- `tag` _Any_ - An optional tag for custom data association (default: None).

<a id="pyke_pyxel.cell_auto.matrix.Cell.reset"></a>

#### reset

```python
def reset()
```

Reset this Cell to the default empty state and store it.

This clears type, colour, propagation flag, power and tag, and
then calls :meth:`store_state` to snapshot the cleared state.

<a id="pyke_pyxel.cell_auto.matrix.Cell.store_state"></a>

#### store\_state

```python
def store_state()
```

Save the current live state into the cell's stored-state slots.

Stored values are used by :meth:`recall_state` to restore a
previously saved state.

<a id="pyke_pyxel.cell_auto.matrix.Cell.recall_state"></a>

#### recall\_state

```python
def recall_state()
```

Restore the cell's live state from previously stored values.

After restoring, the stored slots are cleared to their default
'empty' values.

<a id="pyke_pyxel.cell_auto.matrix.Matrix"></a>

## Matrix Objects

```python
class Matrix()
```

Matrix(width: int = 0, height: int = 0)
A rectangular grid container that manages Cell objects and provides
utility methods for neighbour lookup, region queries and line tracing.

Parameters
----------
width : int, optional
    Number of columns in the matrix (x dimension). Defaults to 0.
height : int, optional
    Number of rows in the matrix (y dimension). Defaults to 0.

Threading / concurrency
-----------------------
- Not thread-safe: mutating methods (clear / direct Cell mutation) can
  invalidate caches and should be synchronised in multithreaded
  contexts.

Examples
--------
- Typical usage:
    m = Matrix(80, 60)
    c = m.cell_at(10, 5)
    neighs = m.neighbours(c)
    line = m.cells_in_line(Coord(0, 0), Coord(10, 5))

<a id="pyke_pyxel.cell_auto.matrix.Matrix.clear"></a>

#### clear

```python
def clear()
```

Re-initialise internal cell grid to a fresh width-by-height matrix.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_N"></a>

#### neighbour\_N

```python
def neighbour_N(cell: Cell) -> Cell|None
```

Return the northern neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_S"></a>

#### neighbour\_S

```python
def neighbour_S(cell: Cell) -> Cell|None
```

Return the southern neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_E"></a>

#### neighbour\_E

```python
def neighbour_E(cell: Cell) -> Cell|None
```

Return the eastern neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_W"></a>

#### neighbour\_W

```python
def neighbour_W(cell: Cell) -> Cell|None
```

Return the western neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_NE"></a>

#### neighbour\_NE

```python
def neighbour_NE(cell: Cell) -> Cell|None
```

Return the north-east neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_NW"></a>

#### neighbour\_NW

```python
def neighbour_NW(cell: Cell) -> Cell|None
```

Return the north-west neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_SE"></a>

#### neighbour\_SE

```python
def neighbour_SE(cell: Cell) -> Cell|None
```

Return the south-east neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_SW"></a>

#### neighbour\_SW

```python
def neighbour_SW(cell: Cell) -> Cell|None
```

Return the south-west neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbours"></a>

#### neighbours

```python
def neighbours(cell: Cell, filter_for_type: Optional[str] = None) -> list[Cell]
```

Return the 8-connected neighbours of ``cell``.

The neighbour list is cached on the :class:`Cell` object as
``cell._neighbours`` and is only populated once; subsequent calls
return a copy of that list so callers may mutate the result without
affecting the cache. If ``filter_for_type`` is provided the result
is filtered by each neighbour's ``type`` attribute.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.cell_at"></a>

#### cell\_at

```python
def cell_at(x: int, y: int) -> Cell|None
```

Safe indexed access to the cell at grid coordinates (x, y).

Returns ``None`` if the coordinates are out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.cells_at"></a>

#### cells\_at

```python
def cells_at(position: Coord, include_empty: bool = False) -> list[Cell]
```

Return cells within the rectangular region described by ``position``.

``position`` is expected to expose ``min_x``, ``min_y``, ``max_x``
and ``max_y`` attributes. The method performs bounds-clipping so
the returned list contains only in-bounds cells. By default empty
cells (where ``c.is_empty`` is True) are excluded unless
``include_empty`` is True.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.cells_in_line"></a>

#### cells\_in\_line

```python
def cells_in_line(from_position: Coord, to_position: Coord, extend_to_matrix_end: bool = False) -> list[Cell]
```

Return the sequence of cells forming a discrete line between two coords.

The result includes both endpoints.

<a id="pyke_pyxel.cell_auto.game"></a>

# game

<a id="pyke_pyxel.cell_auto.game.CellAutoGame"></a>

## CellAutoGame Objects

```python
class CellAutoGame(Game)
```

Specialised sub-class of `pyke_pyxel.Game` which adds a cellular automaton matrix.

**Attributes**:

- `matrix(Matrix)` - read-only access to the cellular automaton matrix

<a id="pyke_pyxel.cell_auto.game.CellAutoGame.__init__"></a>

#### \_\_init\_\_

```python
def __init__(settings: GameSettings, title: str, resources: str)
```

**Arguments**:

- `settings` _GameSettings_ - The game settings configuration.
- `title` _str_ - The title of the game window.
- `resources` _str_ - The path to the resources directory.

<a id="pyke_pyxel.sprite._rpg_sprites"></a>

# \_rpg\_sprites

<a id="pyke_pyxel.sprite._rpg_sprites.OpenableSprite"></a>

## OpenableSprite Objects

```python
class OpenableSprite(Sprite)
```

A Sprite that supports open/close states (e.g., doors, chests).

The OpenableSprite exposes simple open/close methods and manages an
internal status value that determines which frame is shown.

<a id="pyke_pyxel.sprite._rpg_sprites.MovableSprite"></a>

## MovableSprite Objects

```python
class MovableSprite(Sprite)
```

Sprite with movement-related configuration and convenience setters.

MovableSprite stores a movement speed and provides helper methods to
create simple directional animations (up/down/left/right).

<a id="pyke_pyxel.sprite._sprite"></a>

# \_sprite

<a id="pyke_pyxel.sprite._sprite.Animation"></a>

## Animation Objects

```python
class Animation()
```

Represents a sequence of frames for a sprite animation.

Parameters
----------
start_frame : Coord
    The coordinate of the first frame in the animation strip.
frames : int
    Number of frames in the animation.
flip : Optional[bool]
    If True, the animation should be drawn flipped horizontally.

<a id="pyke_pyxel.sprite._sprite.Sprite"></a>

## Sprite Objects

```python
class Sprite()
```

A drawable sprite with optional animations.

A Sprite contains a set of named Animation objects, a current
active_frame to draw, and a position. Animations may be started,
paused, resumed and looped. Sprites are lightweight containers for
animation state and drawing metadata.

Parameters
----------
name : str
    Logical name for the sprite.
default_frame : Coord
    The frame to use when no animation is active (idle frame).
col_tile_count, row_tile_count : int
    Width/height in tiles for framed sprites (used when advancing frames).
resource_image_index : int
    Index of the image resource (if multiple images are used).

<a id="pyke_pyxel.sprite._sprite.Sprite.add_animation"></a>

#### add\_animation

```python
def add_animation(name: str, animation: Animation)
```

Add an animation to the sprite.

Parameters
----------
name : str
    The name to associate with the animation.
animation : Animation
    The Animation object to add.

<a id="pyke_pyxel.sprite._sprite.Sprite.activate_animation"></a>

#### activate\_animation

```python
def activate_animation(name: str, loop: bool = True, on_animation_end: Optional[Callable[[int], None]] = None)
```

Start the named animation.

If the named animation is already active this is a no-op. When
started the animation is unpaused, flip state is applied and the
optional `on_animation_end` callback will be invoked when a
non-looping animation finishes.

<a id="pyke_pyxel.sprite._sprite.Sprite.pause_animation"></a>

#### pause\_animation

```python
def pause_animation()
```

Pause the currently active animation, if any.

<a id="pyke_pyxel.sprite._sprite.Sprite.unpause_animation"></a>

#### unpause\_animation

```python
def unpause_animation()
```

Unpause the currently active animation, if any.

<a id="pyke_pyxel.sprite._sprite.Sprite.deactivate_animations"></a>

#### deactivate\_animations

```python
def deactivate_animations()
```

Stop any active animation and reset flip state.

<a id="pyke_pyxel.sprite._sprite.Sprite.set_position"></a>

#### set\_position

```python
def set_position(position: Coord)
```

Sets the position of the sprite.

**Arguments**:

- `position` _Coord_ - The new coordinate for the sprite's top-left corner.

<a id="pyke_pyxel.sprite._sprite.Sprite.position"></a>

#### position

```python
@property
def position() -> Coord
```

Returns the current position of the sprite.

**Returns**:

- `Coord` - The coordinate of the sprite's top-left corner.

<a id="pyke_pyxel.sprite._compound_sprite"></a>

# \_compound\_sprite

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite"></a>

## CompoundSprite Objects

```python
class CompoundSprite()
```

A multi-tile sprite composed of a grid of `Coord` tiles with optional overlay graphics.

CompoundSprite manages a matrix of tile coordinates (cols x rows)
and provides helpers to fill tiles or set individual tiles. Useful for
larger objects built from multiple sprite tiles.

The class also provides a graphics buffer allowing geometric shapes to be drawn over the sprite tiles

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill_tiles"></a>

#### fill\_tiles

```python
def fill_tiles(tile: Coord)
```

Fill the sprite with a tile

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill_col"></a>

#### fill\_col

```python
def fill_col(col: int, from_row: int, to_row: int, tile_col: int, tile_rows: list[int])
```

Fill one column (all rows) of a sprite with a sequence of tiles

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill_row"></a>

#### fill\_row

```python
def fill_row(row: int, from_col: int, to_col: int, tile_row: int, tile_cols: list[int])
```

Fill one row (all columns) of a sprite with a sequence of tiles

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.set_tile"></a>

#### set\_tile

```python
def set_tile(col: int, row: int, tile: Coord)
```

Set one tile in the sprite

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.clear_graphics"></a>

#### clear\_graphics

```python
def clear_graphics()
```

Clear the graphics buffer

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.graph_rect"></a>

#### graph\_rect

```python
def graph_rect(x: int, y: int, width_px: int, height_px: int, colour: int)
```

Draw a rectangle to the graphics buffer

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.graph_triangle"></a>

#### graph\_triangle

```python
def graph_triangle(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, colour: int)
```

Draw a triangle to the graphics buffer

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.set_position"></a>

#### set\_position

```python
def set_position(position: Coord)
```

Sets the position of the sprite.

**Arguments**:

- `position` _Coord_ - The new coordinate for the sprite's top-left corner.

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.position"></a>

#### position

```python
@property
def position() -> Coord
```

Returns the current position of the sprite.

**Returns**:

- `Coord` - The coordinate of the sprite's top-left corner.

<a id="pyke_pyxel.sprite._text_sprite"></a>

# \_text\_sprite

<a id="pyke_pyxel.sprite._text_sprite.TextSprite"></a>

## TextSprite Objects

```python
class TextSprite()
```

A simple text sprite for rendering text using a pyxel font.

<a id="pyke_pyxel.sprite._text_sprite.TextSprite.set_position"></a>

#### set\_position

```python
def set_position(position: Coord)
```

Sets the position of the sprite.

**Arguments**:

- `position` _Coord_ - The new coordinate for the sprite's top-left corner.

<a id="pyke_pyxel.sprite._text_sprite.TextSprite.position"></a>

#### position

```python
@property
def position() -> Coord
```

Returns the current position of the sprite.

**Returns**:

- `Coord` - The coordinate of the sprite's top-left corner.

<a id="pyke_pyxel.sprite._text_sprite.TextSprite.set_text"></a>

#### set\_text

```python
def set_text(text: str)
```

Sets the text content of the sprite.

**Arguments**:

- `text` _str_ - The new text content.

<a id="pyke_pyxel.hud"></a>

# hud

<a id="pyke_pyxel.hud.HUD"></a>

## HUD Objects

```python
class HUD()
```

HUD manages on-screen heads-up display elements for a game.

This class should be accessed through the `game` instance via `game.hud`.

<a id="pyke_pyxel.hud.HUD.add_text"></a>

#### add\_text

```python
def add_text(text: TextSprite)
```

Add a TextSprite to the HUD.

<a id="pyke_pyxel.hud.HUD.add_sprite"></a>

#### add\_sprite

```python
def add_sprite(sprite: Sprite|CompoundSprite)
```

Add a Sprite or CompoundSprite to the HUD and assign a unique ID.

<a id="pyke_pyxel.hud.HUD.remove_sprite"></a>

#### remove\_sprite

```python
def remove_sprite(sprite: Sprite)
```

Remove a Sprite or CompoundSprite from the HUD.

Behavior:
- If the provided sprite is present in the _sprites list, it is removed.
- If the sprite is not present, the method does nothing (no exception raised).

<a id="pyke_pyxel.hud.HUD.add_button"></a>

#### add\_button

```python
def add_button(button: Button)
```

Add a Button to the HUD and assign a unique ID.

<a id="pyke_pyxel.hud.HUD.remove_button"></a>

#### remove\_button

```python
def remove_button(button: Button)
```

Remove a Button from the HUD.

Behavior:
- If the button is not present, the method does nothing (no exception raised).

<a id="pyke_pyxel.hud.HUD.add_image"></a>

#### add\_image

```python
def add_image(image: Image)
```

Add an Image to the HUD and assign a unique ID.

<a id="pyke_pyxel.hud.HUD.remove_image"></a>

#### remove\_image

```python
def remove_image(image: Image)
```

Remove an Image from the HUD.

Behavior:
- If the image is not present, the method does nothing (no exception raised).

<a id="pyke_pyxel.fx"></a>

# fx

<a id="pyke_pyxel.fx.FX"></a>

## FX Objects

```python
class FX()
```

FX class for managing visual effects in the game, specifically circular wipe transitions that can open or close,
transitioning between scenes or states.

This class should be accessed through the `game` instance via `game.fx`.

<a id="pyke_pyxel.fx.FX.circular_wipe"></a>

#### circular\_wipe

```python
def circular_wipe(colour: int, wipe_closed: bool, completion_signal: str)
```

Create a full-screen circular wipe animation.

Parameters
----------
colour : int
    Colour index/value to use when rendering the wipe.
wipe_closed : bool
    If True, the wipe is configured to close (shrink) toward the centre.
    If False, the wipe is configured to open (expand) outward.
completion_signal : str
    Identifier of the signal/event to emit when the wipe animation finishes.

<a id="pyke_pyxel.fx.FX.splatter"></a>

#### splatter

```python
def splatter(colour: int, position: Coord)
```

Create a splatter effect at the specified position. 
The splatter effect animates within a single tile for 30 frames.

Parameters
----------
colour : int
    Colour index/value to use for the splatter.
position : Coord
    The coordinate where the splatter effect should appear.

<a id="pyke_pyxel._base_types"></a>

# \_base\_types

<a id="pyke_pyxel._base_types.ColourSettings"></a>

## ColourSettings Objects

```python
@dataclass
class ColourSettings()
```

<a id="pyke_pyxel._base_types.ColourSettings.sprite_transparency"></a>

#### sprite\_transparency

COLOURS.BLACK

<a id="pyke_pyxel._base_types.ColourSettings.background"></a>

#### background

COLOURS.BLACK

<a id="pyke_pyxel._base_types.ColourSettings.hud_text"></a>

#### hud\_text

COLOURS.WHITE

<a id="pyke_pyxel._base_types.Coord"></a>

## Coord Objects

```python
class Coord()
```

A grid-aware coordinate representing a tile and its pixel position.

Coord stores both a grid location (column and row, 1-indexed) and the
corresponding top-left pixel coordinates (x, y) for a square tile of
a given size. It provides helpers for creating coordinates from pixel
centers or raw x/y, testing containment/collision, cloning and moving
in pixel space, and deriving mid/min/max bounding values.

<a id="pyke_pyxel._base_types.Coord.__init__"></a>

#### \_\_init\_\_

```python
def __init__(col: int, row: int, size: Optional[int] = None)
```

Create a Coord where col and row are 1-indexed

**Arguments**:

  - col (int): column
  - row (int): row
  - size (int): optionally, the size in pixels of the tile

<a id="pyke_pyxel._base_types.Coord.with_center"></a>

#### with\_center

```python
@staticmethod
def with_center(x: int, y: int, size: Optional[int] = None) -> "Coord"
```

Create a Coord where (x, y) are treated as the visual center.

The returned Coord will have its internal pixel `x, y` set so that
the tile's center is at the given coordinates. Grid column/row are
calculated from the center position.

<a id="pyke_pyxel._base_types.Coord.with_xy"></a>

#### with\_xy

```python
@staticmethod
def with_xy(x: int, y: int, size: Optional[int] = None) -> "Coord"
```

Create a Coord with the provided top-left pixel coordinates.

The provided x and y are used directly as the tile's top-left
pixel coordinates and the grid column/row are computed from them.

<a id="pyke_pyxel._base_types.Coord.is_different_grid_location"></a>

#### is\_different\_grid\_location

```python
def is_different_grid_location(coord: "Coord")
```

Return True when this Coord is on a different grid tile than `coord`.

Comparison is based on grid column and row (1-indexed), not pixel
offsets.

<a id="pyke_pyxel._base_types.Coord.is_same_grid_location"></a>

#### is\_same\_grid\_location

```python
def is_same_grid_location(coord: "Coord")
```

Return True when this Coord is on the same grid tile as `coord`.

<a id="pyke_pyxel._base_types.Coord.contains"></a>

#### contains

```python
def contains(x: int, y: int)
```

Return True if the pixel (x, y) is within this tile's bounding box.

The bounding box is inclusive on both edges (min <= value <= max).

<a id="pyke_pyxel._base_types.Coord.move_by"></a>

#### move\_by

```python
def move_by(x: int, y: int)
```

Move this Coord by (x, y) pixels and update the grid location.

This mutates the Coord in-place. Grid column/row are recalculated
from the new pixel position.

<a id="pyke_pyxel._base_types.Coord.clone"></a>

#### clone

```python
def clone()
```

Return a shallow copy of this Coord (same grid location and size).

<a id="pyke_pyxel._base_types.Coord.clone_by"></a>

#### clone\_by

```python
def clone_by(x: int, y: int, direction: Optional[str] = None)
```

Return a new Coord offset by (x, y) pixels from this one.

When a `direction` is provided ("up", "down", "left", "right")
the resulting grid column/row are adjusted so the cloned tile maps
appropriately to the direction of movement. Without a direction the
grid location is computed from the cloned midpoint.

<a id="pyke_pyxel._base_types.Coord.collides_with"></a>

#### collides\_with

```python
def collides_with(coord: "Coord")
```

Return True if this tile collides with another tile using AABB.

This uses an axis-aligned bounding box (AABB) test with a small
tolerance to reduce false positives on exact-edge overlaps.

<a id="pyke_pyxel._base_types.Coord.distance_to"></a>

#### distance\_to

```python
def distance_to(coord: "Coord") -> float
```

Return the distance between this Coord and the provided Coord

<a id="pyke_pyxel._base_types.Coord.x"></a>

#### x

```python
@property
def x() -> int
```

Top-left pixel x coordinate for this tile.

<a id="pyke_pyxel._base_types.Coord.y"></a>

#### y

```python
@property
def y() -> int
```

Top-left pixel y coordinate for this tile.

<a id="pyke_pyxel._base_types.Coord.mid_x"></a>

#### mid\_x

```python
@property
def mid_x() -> int
```

Integer x coordinate of the visual center (midpoint) of the tile.

<a id="pyke_pyxel._base_types.Coord.mid_y"></a>

#### mid\_y

```python
@property
def mid_y() -> int
```

Integer y coordinate of the visual center (midpoint) of the tile.

<a id="pyke_pyxel._base_types.Coord.min_x"></a>

#### min\_x

```python
@property
def min_x() -> int
```

Alias for the minimum x (top-left) of the tile bounding box.

<a id="pyke_pyxel._base_types.Coord.min_y"></a>

#### min\_y

```python
@property
def min_y() -> int
```

Alias for the minimum y (top-left) of the tile bounding box.

<a id="pyke_pyxel._base_types.Coord.max_x"></a>

#### max\_x

```python
@property
def max_x() -> int
```

Maximum x (bottom-right) of the tile bounding box.

<a id="pyke_pyxel._base_types.Coord.max_y"></a>

#### max\_y

```python
@property
def max_y() -> int
```

Maximum y (bottom-right) of the tile bounding box.

