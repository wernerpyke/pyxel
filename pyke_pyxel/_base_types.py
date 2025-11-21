import math
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
    hud_text: int = 7 # COLOURS.WHITE

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

@dataclass
class DIRECTION:
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

class Coord:
    """A grid-aware coordinate representing a tile and its pixel position.

    Coord stores both a grid location (column and row, 1-indexed) and the
    corresponding top-left pixel coordinates (x, y) for a square tile of
    a given size. It provides helpers for creating coordinates from pixel
    centers or raw x/y, testing containment/collision, cloning and moving
    in pixel space, and deriving mid/min/max bounding values.
    """

    def __init__(self, col: int, row: int, size: Optional[int] = None):
        """Create a Coord where col and row are 1-indexed
        Parameters:
        - col (int): column
        - row (int): row
        - size (int): optionally, the size in pixels of the tile
        """

        if col < 1:
            raise ValueError("Coord() col values must be >= 1")
        if row < 1:
            raise ValueError("Coord() row values must be >= 1")

        self._col: int = col
        self._row: int = row

        if size:
            self.size = size
        else:
            self.size = GameSettings.get().size.tile

        self._x: int = (self._col - 1) * self.size
        self._y: int = (self._row - 1) * self.size

    @staticmethod
    def with_center(x: int, y: int, size: Optional[int] = None) -> "Coord":
        """Create a Coord where (x, y) are treated as the visual center.

        The returned Coord will have its internal pixel `x, y` set so that
        the tile's center is at the given coordinates. Grid column/row are
        calculated from the center position.
        """

        c = Coord(1, 1, size)
        half = math.floor(c.size / 2)
        c._x = x - half
        c._y = y - half

        c._col = round(x / c.size) + 1
        c._row = round(y / c.size) + 1

        return c

    @staticmethod
    def with_xy(x: int, y: int, size: Optional[int] = None) -> "Coord":
        """Create a Coord with the provided top-left pixel coordinates.

        The provided x and y are used directly as the tile's top-left
        pixel coordinates and the grid column/row are computed from them.
        """

        c = Coord(1, 1, size)
        c._x = x
        c._y = y

        c._col = round(x / c.size) + 1
        c._row = round(y / c.size) + 1

        return c

    def is_different_grid_location(self, coord: "Coord"):
        """Return True when this Coord is on a different grid tile than `coord`.

        Comparison is based on grid column and row (1-indexed), not pixel
        offsets.
        """

        return self._col != coord._col or self._row != coord._row

    def is_same_grid_location(self, coord: "Coord"):
        """Return True when this Coord is on the same grid tile as `coord`."""

        return self._col == coord._col and self._row == coord._row

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

    def move_by(self, x: int, y: int):
        """Move this Coord by (x, y) pixels and update the grid location.

        This mutates the Coord in-place. Grid column/row are recalculated
        from the new pixel position.
        """

        self._x += x
        self._y += y
        self._col = math.floor(self.mid_x / self.size) + 1
        self._row = math.floor(self.y / self.size) + 1

    def clone(self):
        """Return a shallow copy of this Coord (same grid location and size)."""

        return Coord(self._col, self._row, self.size)

    def clone_by(self, x: int, y: int, direction: Optional[str] = None):
        """Return a new Coord offset by (x, y) pixels from this one.

        When a `direction` is provided ("up", "down", "left", "right")
        the resulting grid column/row are adjusted so the cloned tile maps
        appropriately to the direction of movement. Without a direction the
        grid location is computed from the cloned midpoint.
        """

        cloned = Coord(self._col, self._row)
        cloned._x = self._x + x
        cloned._y = self._y + y
        cloned.size = self.size

        match direction:
            case "up":
                cloned._col = math.floor(self.mid_x / self.size) + 1
                cloned._row = math.floor(cloned.y / self.size) + 1
            case "down":
                cloned._col = math.floor(self.mid_x / self.size) + 1
                cloned._row = math.floor((cloned.y + self.size) / self.size) + 1
            case "left":
                cloned._col = math.floor(cloned.x / self.size) + 1
                cloned._row = math.floor(self.mid_y / self.size) + 1
            case "right":
                cloned._col = math.floor((cloned.x + self.size) / self.size) + 1
                cloned._row = math.floor(self.mid_y / self.size) + 1
            case _:
                cloned._col = math.floor(cloned.mid_x / self.size) + 1
                cloned._row = math.floor(cloned.y / self.size) + 1

        return cloned

    def collides_with(self, coord: "Coord"):

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

    def distance_to(self, coord: "Coord") -> float:
        """Return the distance between this Coord and the provided Coord"""
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
    
@dataclass
class Image:
    frame: Coord
    position: Coord
    col_tile_count: int = 1
    row_tile_count: int = 1
    resource_image_index: int=0
    _id: int = 0