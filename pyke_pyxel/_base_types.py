import math
import enum

from dataclasses import dataclass
from typing import Optional

@dataclass
class FpsSettings:
    game: int = 30
    animation: int = 8

@dataclass
class SizeSettings:
    window:int  = 160
    tile: int = 8

@dataclass
class ColourSettings:
    sprite_transparency: int = 0 # COLOURS.BLACK
    background:int = 0 # COLOURS.BLACK

class GameSettings:
    _instance = None

    def __init__(self) -> None:
        self.debug: bool = False
        self.fps = FpsSettings()
        self.size = SizeSettings()
        self.colours = ColourSettings()
        self.display_smoothing_enabled = False
        self.full_screen_enabled = False
        self.mouse_enabled = False

    @classmethod
    def get(cls) -> "GameSettings":
        if not cls._instance:
            cls._instance = GameSettings()
        return cls._instance


class DIRECTION(enum.Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

@dataclass
class COLOURS:
    BLACK = 0
    BLUE_DARK = 1
    PURPLE = 2
    GREEN = 3
    BROWN = 4
    BLUE = 5
    BLUE_SKY = 6
    WHITE = 7
    RED = 8
    ORANGE = 9
    YELLOW = 10
    GREEN_MINT = 11
    BLUE_LIGHT = 12    
    GREY = 13
    PINK = 14
    BEIGE = 15

class coord:
    """A grid-aware coordinate representing a tile and its pixel position.

    coord stores both a grid location (column and row, 1-indexed) and the
    corresponding top-left pixel coordinates (x, y) for a square tile of
    a given size. It provides helpers for creating coordinates from pixel
    centers or raw x/y, testing containment/collision, cloning and moving
    in pixel space, and deriving mid/min/max bounding values.
    """

    def __init__(self, col: int, row: int, size: Optional[int] = None):
        """Create a coord where col and row are 1-indexed
        Parameters:
        - col (int): column
        - row (int): row
        - size (int): optionally, the size in pixels of the tile
        """

        if col < 1:
            raise ValueError("coord() col values must be >= 1")
        if row < 1:
            raise ValueError("coord() row values must be >= 1")

        self._col: int = col
        self._row: int = row

        if size:
            self.size = size
        else:
            self.size = GameSettings.get().size.tile

        self._x: int = (self._col - 1) * self.size
        self._y: int = (self._row - 1) * self.size

    @staticmethod
    def with_center(x: int, y: int, size: Optional[int] = None) -> "coord":
        """Create a coord where (x, y) are treated as the visual center.

        The returned coord will have its internal pixel `x, y` set so that
        the tile's center is at the given coordinates. Grid column/row are
        calculated from the center position.
        """

        c = coord(1, 1, size)
        half = math.floor(c.size / 2)
        c._x = x - half
        c._y = y - half

        c._col = round(x / c.size) + 1
        c._row = round(y / c.size) + 1

        return c

    @staticmethod
    def with_xy(x: int, y: int, size: Optional[int] = None) -> "coord":
        """Create a coord with the provided top-left pixel coordinates.

        The provided x and y are used directly as the tile's top-left
        pixel coordinates and the grid column/row are computed from them.
        """

        c = coord(1, 1, size)
        c._x = x
        c._y = y

        c._col = round(x / c.size) + 1
        c._row = round(y / c.size) + 1

        return c

    def is_different_grid_location(self, coord: "coord"):
        """Return True when this coord is on a different grid tile than `coord`.

        Comparison is based on grid column and row (1-indexed), not pixel
        offsets.
        """

        return self._col != coord._col or self._row != coord._row

    def is_same_grid_location(self, coord: "coord"):
        """Return True when this coord is on the same grid tile as `coord`."""

        return self._col == coord._col and self._row == coord._row

    def is_at(self, coord: "coord"):
        """Return true if this coord is at exactly the same (x,y) location as `coord`"""
        return self._x == coord._x and self._y == coord._y

    def is_above(self, coord: "coord"):
        """Return true if this coord is above `coord`"""
        return self._y < coord._y
    
    def is_below(self, coord: "coord"):
        """Return true if this coord is below `coord`"""
        return self._y > coord._y
    
    def is_left_of(self, coord: "coord"):
        """Return true if this coord is to the left of `coord`"""
        return self._x < coord._x
    
    def is_right_of(self, coord: "coord"):
        """Return true if this coord is to the right of `coord`"""
        return self._x > coord._x

    def contains(self, x: int, y: int):
        """Return True if the pixel (x, y) is within this tile's bounding box.

        The bounding box is inclusive on both edges (min <= value <= max).
        """

        min_x = self._x
        max_x = self._x + self.size
        if x < min_x or x > max_x:
            return False

        min_y = self._y
        max_y = self._y + self.size
        if y < min_y or y > max_y:
            return False

        return True

    def move_by(self, x: int = 0, y: int = 0):
        """Move this coord by (x, y) pixels and update the grid location.

        This mutates the coord in-place. Grid column/row are recalculated
        from the new pixel position.
        """

        self._x += x
        self._y += y
        self._col = math.floor(self.mid_x / self.size) + 1
        self._row = math.floor(self.y / self.size) + 1

    def clone(self):
        """Return a shallow copy of this coord (same grid location and size)."""
        # Use self._x/_y rather than self._col/_row
        # to avoid prior rounding of _col/_row
        return coord.with_xy(self._x, self._y, self.size)

    def clone_by(self, x: int, y: int, direction: DIRECTION|None = None):
        """Return a new coord offset by (x, y) pixels from this one.

        When a `direction` is provided ("up", "down", "left", "right")
        the resulting grid column/row are adjusted so the cloned tile maps
        appropriately to the direction of movement. Without a direction the
        grid location is computed from the cloned midpoint.
        """

        cloned = coord.with_xy(self._x + x, self._y + y, self.size)
        match direction:
            case DIRECTION.UP:
                cloned._col = math.floor(self.mid_x / self.size) + 1
                cloned._row = math.floor(cloned.y / self.size) + 1
            case DIRECTION.DOWN:
                cloned._col = math.floor(self.mid_x / self.size) + 1
                cloned._row = math.floor((cloned.y + self.size) / self.size) + 1
            case DIRECTION.LEFT:
                cloned._col = math.floor(cloned.x / self.size) + 1
                cloned._row = math.floor(self.mid_y / self.size) + 1
            case DIRECTION.RIGHT:
                cloned._col = math.floor((cloned.x + self.size) / self.size) + 1
                cloned._row = math.floor(self.mid_y / self.size) + 1
            case _:
                cloned._col = math.floor(cloned.mid_x / self.size) + 1
                cloned._row = math.floor(cloned.y / self.size) + 1

        return cloned

    def collides_with(self, coord: "coord"):

        """Return True if this tile collides with another tile using AABB.

        This uses an axis-aligned bounding box (AABB) test with a small
        tolerance to reduce false positives on exact-edge overlaps.
        """

        # AABB detection
        #    if self.pos_x < obj.pos_x+obj.width and self.pos_x+self.width > obj.pos_x:
        #        if self.pos_y < obj.pos_y+obj.height and self.pos_y+self.height > obj.pos_y:

        collide_x = coord._x
        collide_y = coord._y
        sprite_x = self._x
        sprite_y = self._y

        w = h = self.size
        tolerance = 1

        return (
            collide_x < (sprite_x + w - tolerance) and
            collide_x + w > (sprite_x + tolerance) and
            collide_y < (sprite_y + h - tolerance) and
            collide_y + h > (sprite_y + tolerance)
        )

    def distance_to(self, coord: "coord") -> float:
        """Return the distance between this coord and the provided coord"""
        delta_x = self._x - coord._x
        delta_y = self._y - coord._y
        
        # Apply the distance formula
        distance = math.sqrt(delta_x**2 + delta_y**2)
        return distance

    @property
    def x(self) -> int:
        """Top-left pixel x coordinate for this tile."""
        return self._x

    @property
    def y(self) -> int:
        """Top-left pixel y coordinate for this tile."""
        return self._y

    @property
    def mid_x(self) -> int:
        """Integer x coordinate of the visual center (midpoint) of the tile."""
        return math.floor(self._x + (self.size / 2))

    @property
    def mid_y(self) -> int:
        """Integer y coordinate of the visual center (midpoint) of the tile."""
        return math.floor(self._y + (self.size / 2))

    @property
    def min_x(self) -> int:
        """Alias for the minimum x (top-left) of the tile bounding box."""
        return self._x

    @property
    def min_y(self) -> int:
        """Alias for the minimum y (top-left) of the tile bounding box."""
        return self._y

    @property
    def max_x(self) -> int:
        """Maximum x (bottom-right) of the tile bounding box."""
        return self._x + self.size

    @property
    def max_y(self) -> int:
        """Maximum y (bottom-right) of the tile bounding box."""
        return self._y + self.size

    def __str__(self):
        return f"{self._col}/{self._row}"
