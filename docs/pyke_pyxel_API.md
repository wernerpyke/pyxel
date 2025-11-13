# None

## API Reference

* [game](#pyke_pyxel.game)
  * [Game](#pyke_pyxel.game.Game)
    * [\_\_init\_\_](#pyke_pyxel.game.Game.__init__)
    * [start](#pyke_pyxel.game.Game.start)
    * [add\_sprite](#pyke_pyxel.game.Game.add_sprite)
    * [remove\_sprite](#pyke_pyxel.game.Game.remove_sprite)
    * [remove\_sprite\_by\_id](#pyke_pyxel.game.Game.remove_sprite_by_id)
    * [update](#pyke_pyxel.game.Game.update)
    * [draw](#pyke_pyxel.game.Game.draw)
* [game](#pyke_pyxel.rpg.game)
  * [RPGGame](#pyke_pyxel.rpg.game.RPGGame)
    * [\_\_init\_\_](#pyke_pyxel.rpg.game.RPGGame.__init__)
* [sprite](#pyke_pyxel.sprite)
  * [Animation](#pyke_pyxel.sprite.Animation)
  * [Sprite](#pyke_pyxel.sprite.Sprite)
    * [activate\_animation](#pyke_pyxel.sprite.Sprite.activate_animation)
    * [pause\_animation](#pyke_pyxel.sprite.Sprite.pause_animation)
    * [unpause\_animation](#pyke_pyxel.sprite.Sprite.unpause_animation)
    * [deactivate\_animations](#pyke_pyxel.sprite.Sprite.deactivate_animations)
    * [set\_position](#pyke_pyxel.sprite.Sprite.set_position)
  * [OpenableSprite](#pyke_pyxel.sprite.OpenableSprite)
  * [MovableSprite](#pyke_pyxel.sprite.MovableSprite)
  * [CompoundSprite](#pyke_pyxel.sprite.CompoundSprite)
  * [TextSprite](#pyke_pyxel.sprite.TextSprite)
* [base\_types](#pyke_pyxel.base_types)
  * [Coord](#pyke_pyxel.base_types.Coord)
    * [with\_center](#pyke_pyxel.base_types.Coord.with_center)
    * [with\_xy](#pyke_pyxel.base_types.Coord.with_xy)
    * [is\_different\_grid\_location](#pyke_pyxel.base_types.Coord.is_different_grid_location)
    * [is\_same\_grid\_location](#pyke_pyxel.base_types.Coord.is_same_grid_location)
    * [contains](#pyke_pyxel.base_types.Coord.contains)
    * [move\_by](#pyke_pyxel.base_types.Coord.move_by)
    * [clone](#pyke_pyxel.base_types.Coord.clone)
    * [clone\_by](#pyke_pyxel.base_types.Coord.clone_by)
    * [collides\_with](#pyke_pyxel.base_types.Coord.collides_with)
    * [x](#pyke_pyxel.base_types.Coord.x)
    * [y](#pyke_pyxel.base_types.Coord.y)
    * [mid\_x](#pyke_pyxel.base_types.Coord.mid_x)
    * [mid\_y](#pyke_pyxel.base_types.Coord.mid_y)
    * [min\_x](#pyke_pyxel.base_types.Coord.min_x)
    * [min\_y](#pyke_pyxel.base_types.Coord.min_y)
    * [max\_x](#pyke_pyxel.base_types.Coord.max_x)
    * [max\_y](#pyke_pyxel.base_types.Coord.max_y)
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
* [settings](#pyke_pyxel.settings)
  * [ColourSettings](#pyke_pyxel.settings.ColourSettings)
    * [sprite\_transparency](#pyke_pyxel.settings.ColourSettings.sprite_transparency)
    * [background](#pyke_pyxel.settings.ColourSettings.background)
    * [hud\_text](#pyke_pyxel.settings.ColourSettings.hud_text)
* [hud](#pyke_pyxel.hud)
  * [HUD](#pyke_pyxel.hud.HUD)
    * [add\_text](#pyke_pyxel.hud.HUD.add_text)
    * [add\_sprite](#pyke_pyxel.hud.HUD.add_sprite)
    * [remove\_sprite](#pyke_pyxel.hud.HUD.remove_sprite)
    * [add\_button](#pyke_pyxel.hud.HUD.add_button)
    * [remove\_button](#pyke_pyxel.hud.HUD.remove_button)
    * [add\_image](#pyke_pyxel.hud.HUD.add_image)
    * [remove\_image](#pyke_pyxel.hud.HUD.remove_image)

<a id="pyke_pyxel.game"></a>

# game

<a id="pyke_pyxel.game.Game"></a>

## Game Objects

```python
class Game()
```

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

<a id="pyke_pyxel.game.Game.update"></a>

#### update

```python
def update()
```

Pyxel lifecycle handler. Updates the game state for each frame.

Signals:
    - GAME.UPDATE: Sent every update.
    - MOUSE.MOVE: Sent when mouse position changes.
    - MOUSE.DOWN: Sent on left mouse button press.
    - MOUSE.UP: Sent on left mouse button release.

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

Specialised sub-class of pyke_pyxel.game which adds basic room- and actor-based RPG mechanics.

**Attributes**:

- `player` _Player_ - The player character. Use set_player() to assign the player instance.
- `room` _Room_ - The current room/map the player is in. Automatically initialized with the game map.
- `movement_tick` _bool_ - Flag indicating whether movement input should be processed this frame.
  

**Arguments**:

- `settings` _GameSettings_ - The game settings configuration.
- `title` _str_ - The title of the game window.
- `resources` _str_ - The path to the resources directory.

<a id="pyke_pyxel.sprite"></a>

# sprite

<a id="pyke_pyxel.sprite.Animation"></a>

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

<a id="pyke_pyxel.sprite.Sprite"></a>

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

<a id="pyke_pyxel.sprite.Sprite.activate_animation"></a>

#### activate\_animation

```python
def activate_animation(name: str, loop: bool = True, on_animation_end: Optional[Callable[[int], None]] = None)
```

Start the named animation.

If the named animation is already active this is a no-op. When
started the animation is unpaused, flip state is applied and the
optional `on_animation_end` callback will be invoked when a
non-looping animation finishes.

<a id="pyke_pyxel.sprite.Sprite.pause_animation"></a>

#### pause\_animation

```python
def pause_animation()
```

Pause the currently active animation, if any.

<a id="pyke_pyxel.sprite.Sprite.unpause_animation"></a>

#### unpause\_animation

```python
def unpause_animation()
```

Unpause the currently active animation, if any.

<a id="pyke_pyxel.sprite.Sprite.deactivate_animations"></a>

#### deactivate\_animations

```python
def deactivate_animations()
```

Stop any active animation and reset flip state.

<a id="pyke_pyxel.sprite.Sprite.set_position"></a>

#### set\_position

```python
def set_position(position: Coord)
```

Set the pixel/grid position where this Sprite will be drawn.

<a id="pyke_pyxel.sprite.OpenableSprite"></a>

## OpenableSprite Objects

```python
class OpenableSprite(Sprite)
```

A Sprite that supports open/close states (e.g., doors, chests).

The OpenableSprite exposes simple open/close methods and manages an
internal status value that determines which frame is shown.

<a id="pyke_pyxel.sprite.MovableSprite"></a>

## MovableSprite Objects

```python
class MovableSprite(Sprite)
```

Sprite with movement-related configuration and convenience setters.

MovableSprite stores a movement speed and provides helper methods to
create simple directional animations (up/down/left/right).

<a id="pyke_pyxel.sprite.CompoundSprite"></a>

## CompoundSprite Objects

```python
class CompoundSprite()
```

A multi-tile sprite composed of a grid of `Coord` tiles.

CompoundSprite manages a matrix of tile coordinates (cols x rows)
and provides helpers to fill tiles or set individual tiles. Useful for
larger objects built from multiple sprite tiles.

<a id="pyke_pyxel.sprite.TextSprite"></a>

## TextSprite Objects

```python
class TextSprite()
```

A simple text sprite for rendering text using a pyxel font.

<a id="pyke_pyxel.base_types"></a>

# base\_types

<a id="pyke_pyxel.base_types.Coord"></a>

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

<a id="pyke_pyxel.base_types.Coord.with_center"></a>

#### with\_center

```python
@staticmethod
def with_center(x: int, y: int, size: Optional[int] = None) -> "Coord"
```

Create a Coord where (x, y) are treated as the visual center.

The returned Coord will have its internal pixel `x, y` set so that
the tile's center is at the given coordinates. Grid column/row are
calculated from the center position.

<a id="pyke_pyxel.base_types.Coord.with_xy"></a>

#### with\_xy

```python
@staticmethod
def with_xy(x: int, y: int, size: Optional[int] = None) -> "Coord"
```

Create a Coord with the provided top-left pixel coordinates.

The provided x and y are used directly as the tile's top-left
pixel coordinates and the grid column/row are computed from them.

<a id="pyke_pyxel.base_types.Coord.is_different_grid_location"></a>

#### is\_different\_grid\_location

```python
def is_different_grid_location(coord: "Coord")
```

Return True when this Coord is on a different grid tile than `coord`.

Comparison is based on grid column and row (1-indexed), not pixel
offsets.

<a id="pyke_pyxel.base_types.Coord.is_same_grid_location"></a>

#### is\_same\_grid\_location

```python
def is_same_grid_location(coord: "Coord")
```

Return True when this Coord is on the same grid tile as `coord`.

<a id="pyke_pyxel.base_types.Coord.contains"></a>

#### contains

```python
def contains(x: int, y: int)
```

Return True if the pixel (x, y) is within this tile's bounding box.

The bounding box is inclusive on both edges (min <= value <= max).

<a id="pyke_pyxel.base_types.Coord.move_by"></a>

#### move\_by

```python
def move_by(x: int, y: int)
```

Move this Coord by (x, y) pixels and update the grid location.

This mutates the Coord in-place. Grid column/row are recalculated
from the new pixel position.

<a id="pyke_pyxel.base_types.Coord.clone"></a>

#### clone

```python
def clone()
```

Return a shallow copy of this Coord (same grid location and size).

<a id="pyke_pyxel.base_types.Coord.clone_by"></a>

#### clone\_by

```python
def clone_by(x: int, y: int, direction: Optional[str] = None)
```

Return a new Coord offset by (x, y) pixels from this one.

When a `direction` is provided ("up", "down", "left", "right")
the resulting grid column/row are adjusted so the cloned tile maps
appropriately to the direction of movement. Without a direction the
grid location is computed from the cloned midpoint.

<a id="pyke_pyxel.base_types.Coord.collides_with"></a>

#### collides\_with

```python
def collides_with(coord: "Coord")
```

Return True if this tile collides with another tile using AABB.

This uses an axis-aligned bounding box (AABB) test with a small
tolerance to reduce false positives on exact-edge overlaps.

<a id="pyke_pyxel.base_types.Coord.x"></a>

#### x

```python
@property
def x() -> int
```

Top-left pixel x coordinate for this tile.

<a id="pyke_pyxel.base_types.Coord.y"></a>

#### y

```python
@property
def y() -> int
```

Top-left pixel y coordinate for this tile.

<a id="pyke_pyxel.base_types.Coord.mid_x"></a>

#### mid\_x

```python
@property
def mid_x() -> int
```

Integer x coordinate of the visual center (midpoint) of the tile.

<a id="pyke_pyxel.base_types.Coord.mid_y"></a>

#### mid\_y

```python
@property
def mid_y() -> int
```

Integer y coordinate of the visual center (midpoint) of the tile.

<a id="pyke_pyxel.base_types.Coord.min_x"></a>

#### min\_x

```python
@property
def min_x() -> int
```

Alias for the minimum x (top-left) of the tile bounding box.

<a id="pyke_pyxel.base_types.Coord.min_y"></a>

#### min\_y

```python
@property
def min_y() -> int
```

Alias for the minimum y (top-left) of the tile bounding box.

<a id="pyke_pyxel.base_types.Coord.max_x"></a>

#### max\_x

```python
@property
def max_x() -> int
```

Maximum x (bottom-right) of the tile bounding box.

<a id="pyke_pyxel.base_types.Coord.max_y"></a>

#### max\_y

```python
@property
def max_y() -> int
```

Maximum y (bottom-right) of the tile bounding box.

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

Each position is filled with a new :class:`Cell` instance that uses
the Matrix's internal pyxel Image for fast drawing.

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
def cells_in_line(from_position: Coord, to_position: Coord) -> list[Cell]
```

Return the sequence of cells forming a discrete line between two coords.

Implements a Bresenham-like integer algorithm that handles all octants.
Coordinates outside the matrix are ignored; only in-bounds cells are
appended to the result. Iteration includes both endpoints.

<a id="pyke_pyxel.cell_auto.game"></a>

# game

<a id="pyke_pyxel.cell_auto.game.CellAutoGame"></a>

## CellAutoGame Objects

```python
class CellAutoGame(Game)
```

Specialised sub-class of pyke_pyxel.game which adds a cellular automaton matrix.

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

<a id="pyke_pyxel.settings"></a>

# settings

<a id="pyke_pyxel.settings.ColourSettings"></a>

## ColourSettings Objects

```python
@dataclass
class ColourSettings()
```

<a id="pyke_pyxel.settings.ColourSettings.sprite_transparency"></a>

#### sprite\_transparency

COLOURS.BLACK

<a id="pyke_pyxel.settings.ColourSettings.background"></a>

#### background

COLOURS.BLACK

<a id="pyke_pyxel.settings.ColourSettings.hud_text"></a>

#### hud\_text

COLOURS.WHITE

<a id="pyke_pyxel.hud"></a>

# hud

<a id="pyke_pyxel.hud.HUD"></a>

## HUD Objects

```python
class HUD()
```

HUD manages on-screen heads-up display elements for a game.
- Removal methods are safe no-ops if the element is not present.

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

