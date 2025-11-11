from dataclasses import dataclass
import math
from typing import Optional
from . import GLOBAL_SETTINGS

class Coord:
    def __init__(self, col: int, row: int, size: Optional[int] = None):
        self._col: int = col
        self._row: int = row

        if size:
            self.size = size
        else:
            self.size = GLOBAL_SETTINGS.size.tile
        
        self._x: int = (self._col - 1) * self.size
        self._y: int = (self._row - 1) * self.size

    @staticmethod
    def with_center(x: int, y: int, size: Optional[int] = None) -> "Coord":
        c = Coord(0, 0, size)
        half = math.floor(c.size / 2)
        c._x = x - half
        c._y = y - half

        c._col = round(x / c.size) + 1
        c._row = round(y / c.size) + 1

        return c
    
    @staticmethod
    def with_xy(x: int, y: int, size: Optional[int] = None) -> "Coord":
        c = Coord(0, 0, size)
        c._x = x
        c._y = y

        c._col = round(x / c.size) + 1
        c._row = round(y / c.size) + 1

        return c

    def is_different_grid_location(self, coord: "Coord"):
        return self._col != coord._col or self._row != coord._row
    
    def is_same_grid_location(self, coord: "Coord"):
        return self._col == coord._col and self._row == coord._row
    
    def contains(self, x: int, y: int):
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
        self._x += x
        self._y += y
        self._col = math.floor(self.mid_x / self.size) + 1
        self._row = math.floor(self.y / self.size) + 1

    def clone(self):
        return Coord(self._col, self._row, self.size)

    def clone_by(self, x: int, y: int, direction: Optional[str] = None):
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

    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y
    
    @property
    def mid_x(self) -> int:
        return math.floor(self._x + (self.size / 2))
    
    @property
    def mid_y(self) -> int:
        return math.floor(self._y + (self.size / 2))
    
    @property
    def min_x(self) -> int:
        return self._x
    
    @property
    def min_y(self) -> int:
        return self._y
    
    @property
    def max_x(self) -> int:
        return self._x + self.size
    
    @property
    def max_y(self) -> int:
        return self._y + self.size
    
    def __str__(self):
        return f"{self._col}/{self._row}"
    
@dataclass
class TileMap:
    resource_position: Coord
    tiles_wide: int
    tiles_high: int
    resource_index: int=0

@dataclass
class Image:
    frame: Coord
    position: Coord
    col_tile_count: int = 1
    row_tile_count: int = 1
    resource_image_index: int=0

    _id: int = 0
