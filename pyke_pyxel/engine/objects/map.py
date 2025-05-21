import math
from dataclasses import dataclass
import constants

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .sprite import Sprite

class Coord:
    def __init__(self, col: int, row: int):
        self._col = col
        self._row = row

        self._x = (self._col - 1) * constants.SIZE.TILE
        self._y = (self._row - 1) * constants.SIZE.TILE

        # print(f"Coord() col:{self._col} row:{self._row} x:{self._x} y:{self._y}")

    def move(self, x: int, y: int):
        self._x += x
        self._y += y

        self._col = math.floor(self._x / constants.SIZE.TILE) + 1
        self._row = math.floor(self._y / constants.SIZE.TILE) + 1

        # print(f"Coord.move() x:{self._x} y:{self._y} col:{self._col} row:{self._row}")

    def clone_by(self, x: int, y: int):
        new_x = self._x + x
        new_y = self._y + y
        new_col = math.floor(new_x / constants.SIZE.TILE) + 1
        new_row = math.floor(new_y / constants.SIZE.TILE) + 1
        cloned = Coord(new_col, new_row)
        cloned._x = new_x
        cloned._y = new_y
        return cloned
    
    def collides_with(self, coord: "Coord"):
        # AABB detection
        #    if self.pos_x < obj.pos_x+obj.width and self.pos_x+self.width > obj.pos_x:
        #        if self.pos_y < obj.pos_y+obj.height and self.pos_y+self.height > obj.pos_y:

        collide_x = coord._x
        collide_y = coord._y
        sprite_x = self._x
        sprite_y = self._y
        
        w = constants.SIZE.TILE
        h = constants.SIZE.TILE
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
    
class Map:

    @staticmethod
    def find_nearby(sprites: list["Sprite"], for_sprite: "Sprite") -> list["Sprite"]:
        sprite_col = for_sprite.position._col
        sprite_row = for_sprite.position._row
        
        result: list["Sprite"] = []

        for s in sprites:
            col = s.position._col
            row = s.position._row

            if col in range(sprite_col - 2, sprite_col + 2) and row in range(sprite_row - 2, sprite_row + 2):
                result.append(s)

        return result
