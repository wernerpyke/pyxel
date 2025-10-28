from dataclasses import dataclass
import math
from . import GLOBAL_SETTINGS

class Coord:
    def __init__(self, col: int, row: int):
        self._col = col
        self._row = row

        tile_size = GLOBAL_SETTINGS.size.tile
        self._x = (self._col - 1) * tile_size
        self._y = (self._row - 1) * tile_size

    def is_different_grid_location(self, coord: "Coord"):
        return self._col != coord._col or self._row != coord._row
    
    def is_same_grid_location(self, coord: "Coord"):
        return self._col == coord._col and self._row == coord._row

    def clone_by(self, x: int, y: int, direction: str):
        cloned = Coord(self._col, self._row)
        cloned._x = self._x + x
        cloned._y = self._y + y

        tile_size = GLOBAL_SETTINGS.size.tile

        match direction:
            case "up":
                cloned._col = math.floor(self.mid_x / tile_size) + 1
                cloned._row = math.floor(cloned.y / tile_size) + 1
            case "down":
                cloned._col = math.floor(self.mid_x / tile_size) + 1
                cloned._row = math.floor((cloned.y + tile_size) / tile_size) + 1
            case "left":
                cloned._col = math.floor(cloned.x / tile_size) + 1
                cloned._row = math.floor(self.mid_y / tile_size) + 1
            case "right":
                cloned._col = math.floor((cloned.x + tile_size) / tile_size) + 1
                cloned._row = math.floor(self.mid_y / tile_size) + 1

        return cloned
    
    def collides_with(self, coord: "Coord"):
        # AABB detection
        #    if self.pos_x < obj.pos_x+obj.width and self.pos_x+self.width > obj.pos_x:
        #        if self.pos_y < obj.pos_y+obj.height and self.pos_y+self.height > obj.pos_y:

        collide_x = coord._x
        collide_y = coord._y
        sprite_x = self._x
        sprite_y = self._y

        tile_size = GLOBAL_SETTINGS.size.tile        
        w = tile_size
        h = tile_size
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
        tile_size = GLOBAL_SETTINGS.size.tile
        return math.floor(self._x + (tile_size / 2))
    
    @property
    def mid_y(self) -> int:
        tile_size = GLOBAL_SETTINGS.size.tile
        return math.floor(self._y + (tile_size / 2))
    
    def __str__(self):
        return f"{self._col}/{self._row}"
    
@dataclass
class TileMap:
    resource_position: Coord
    tiles_wide: int
    tiles_high: int