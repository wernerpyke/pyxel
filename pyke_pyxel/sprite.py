from typing import Optional, Callable
import pyxel

from pyke_pyxel import Coord

class Animation:
    """Represents a sequence of frames for a sprite animation.

    Parameters
    ----------
    start_frame : Coord
        The coordinate of the first frame in the animation strip.
    frames : int
        Number of frames in the animation.
    flip : Optional[bool]
        If True, the animation should be drawn flipped horizontally.
    """
    def __init__(self, start_frame: Coord, frames: int, flip: Optional[bool] = False):
        self._start_frame = start_frame
        self._frames = frames
        self.flip: bool = True if flip else False

        self._name: str
        self._current_frame_index:int = 0

        self._paused = False

class Sprite:
    """A drawable sprite with optional animations.

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
    """
    
    def __init__(self, name: str, default_frame: Coord, col_tile_count: int = 1, row_tile_count: int = 1, resource_image_index: int=0):
        self._id: int = 0
        self.name = name
        self.idle_frame = default_frame

        self.animations: dict[str, Animation] = { }
        self._position: Coord
        self.active_frame = self.idle_frame
        self.is_flipped: bool = False

        self._animation: Optional[Animation] = None
        self._loop_animation: bool = True
        self._on_animation_end: Optional[Callable[[int], None]] = None

        self.col_tile_count = col_tile_count
        self.row_tile_count = row_tile_count

        self._resource_image_index = resource_image_index

    def add_animation(self, name: str, animation: Animation):
        animation._name = name
        self.animations[name] = animation
        
    def activate_animation(self, name: str, loop: bool = True, on_animation_end: Optional[Callable[[int], None]] = None):
        """Start the named animation.

        If the named animation is already active this is a no-op. When
        started the animation is unpaused, flip state is applied and the
        optional `on_animation_end` callback will be invoked when a
        non-looping animation finishes.
        """
        if self._animation and self._animation._name == name:
            return

        self._animation = self.animations[name]
        self._animation._paused = False
        self.is_flipped = self._animation.flip
        self._loop_animation = loop
        self._on_animation_end = on_animation_end

        self._animation._current_frame_index = 0

    def pause_animation(self):
        """Pause the currently active animation, if any."""
        if self._animation:
            self._animation._paused = True

    def unpause_animation(self):
        """Unpause the currently active animation, if any."""
        if self._animation:
            self._animation._paused = False

    def deactivate_animations(self):
        """Stop any active animation and reset flip state."""
        if self._animation:
            self._animation._paused = False
        self._animation = None
        self.is_flipped = False

    def set_position(self, position: Coord):
        """Set the pixel/grid position where this Sprite will be drawn."""
        self._position = position

    @property
    def position(self) -> Coord:
        return self._position
    
    def __eq__(self, other):
        return isinstance(other, Sprite) and self._id == other._id

    def _update_frame(self):
        anim = self._animation

        if anim:
            if anim._current_frame_index >= anim._frames:
                if self._loop_animation:
                    anim._current_frame_index = 0
                else:
                    if self._on_animation_end:
                        id = self._id
                        self._on_animation_end(id)
                        self._on_animation_end = None
                    else:
                        self.deactivate_animations()

            col = anim._start_frame._col + (anim._current_frame_index * self.col_tile_count)
            self.active_frame = Coord(col, anim._start_frame._row)
            # print(f"Sprite.update_frame() frame:{anim._start_frame._col}+({anim._current_frame_index}*{self.col_tile_count})={col} frameCol:{self.active_frame._col} x:{self.active_frame.x}")

            anim._current_frame_index += 1
        else:
            self.active_frame = self.idle_frame

OPEN: int = 0
CLOSED: int = 1
CLOSING: int = 2
OPENING: int = 3

class OpenableSprite(Sprite):
    """A Sprite that supports open/close states (e.g., doors, chests).

    The OpenableSprite exposes simple open/close methods and manages an
    internal status value that determines which frame is shown.
    """
    def __init__(self, name: str, openFrame: Coord, closedFrame: Coord, openingAnimation: Animation):
        super().__init__(name, openFrame)
        self._openFrame = openFrame
        self._closedFrame = closedFrame
        self._openingAnimation = openingAnimation

        self._status = OPEN

    def close(self):
        self._status = CLOSED
        self._update_frame()

    def open(self):
        self._status = OPEN
        self._update_frame()

    @property
    def is_closed(self) -> bool:
        return self._status == CLOSED
    
    @property
    def is_open(self) -> bool:
        return self._status == OPEN
    
    def _update_frame(self):
        match self._status:
            case 0: # Open
                self.active_frame = self._openFrame
                return
            
            case 1: # Closed
                self.active_frame = self._closedFrame

class MovableSprite(Sprite):
    """Sprite with movement-related configuration and convenience setters.

    MovableSprite stores a movement speed and provides helper methods to
    create simple directional animations (up/down/left/right).
    """

    def __init__(self, name: str, idleFrame: Coord, movement_speed: int):
        super().__init__(name, idleFrame)
        self.movementSpeed = movement_speed

    def set_up_animation(self, start_frame: Coord, frame_count: int, flip: Optional[bool] = False):
        self.add_animation("up", Animation(start_frame, frame_count, flip))

    def set_down_animation(self, start_frame: Coord, frame_count: int, flip: Optional[bool] = False):
        self.add_animation("down", Animation(start_frame, frame_count, flip))

    def set_left_animation(self, start_frame: Coord, frame_count: int, flip: Optional[bool] = False):
        self.add_animation("left", Animation(start_frame, frame_count, flip))

    def set_right_animation(self, start_frame: Coord, frame_count: int, flip: Optional[bool] = False):
        self.add_animation("right", Animation(start_frame, frame_count, flip))

class CompoundSprite:
    """A multi-tile sprite composed of a grid of `Coord` tiles.

    CompoundSprite manages a matrix of tile coordinates (cols x rows)
    and provides helpers to fill tiles or set individual tiles. Useful for
    larger objects built from multiple sprite tiles.
    """

    def __init__(self, name: str, cols: int, rows: int, resource_image_index: int=0):
        self.name = name
        self._id: int = 0
        self._position: Coord
        self._resource_image_index = resource_image_index

        self.cols: list[list[Coord|None]] = [[None for r in range(rows)] for c in range(cols)]
        
        #for c in range(0, cols):
        #    row: list[Coord|None] = []
        #    for r in range(0, rows):
        #        row.append(None)
        #    self.cols.append(row)

    def __eq__(self, other):
        return isinstance(other, CompoundSprite) and self._id == other._id

    def fill_tiles(self, tile: Coord):
        for c in range(0, len(self.cols)):
            row = self.cols[c]
            for r in range(0, len(row)):
                row[r] = tile

    def fill_col(self, col: int, from_row: int, to_row: int, tile_col: int, tile_rows: list[int]):
        rows = self.cols[(col-1)]
        tile_index = 0
        for r in range((from_row-1), to_row):
            rows[r] = Coord(tile_col, tile_rows[tile_index])
            tile_index += 1
            tile_index = tile_index % len(tile_rows)

    def fill_row(self, row: int, from_col: int, to_col: int, tile_row: int, tile_cols: list[int]):
        tile_index = 0
        for col_i in range((from_col-1), to_col):
            col = self.cols[col_i]
            col[(row-1)] = Coord(tile_cols[tile_index], tile_row)
            tile_index += 1
            tile_index = tile_index % len(tile_cols)

    def set_tile(self, col: int, row: int, tile: Coord):
        self.cols[(col-1)][(row-1)] = tile

    def set_position(self, position: Coord):
        self._position = position

    @property
    def position(self) -> Coord:
        return self._position

class TextSprite:
    """A simple text sprite for rendering text using a pyxel font.
    """

    def __init__(self, text: str, colour: int, font_file: str):
        self._text = text
        self._colour = colour
        self._font = pyxel.Font(font_file)

    def set_position(self, position: Coord):
        self._position = position

    @property
    def position(self) -> Coord:
        return self._position

    def set_text(self, text: str):
        self._text = text

    def set_colour(self, colour: int):
        self._colour = colour