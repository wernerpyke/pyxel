import math
import constants

class Coord:
    def __init__(self, col: int, row: int):
        self._col = col
        self._row = row

        self._x = (self._col - 1) * constants.SIZE.TILE
        self._y = (self._row - 1) * constants.SIZE.TILE

    def is_different_grid_location(self, coord: "Coord"):
        return self._col != coord._col or self._row != coord._row
    
    def is_same_grid_location(self, coord: "Coord"):
        return self._col == coord._col and self._row == coord._row

    def clone_by(self, x: int, y: int, direction: str):
        cloned = Coord(self._col, self._row)
        cloned._x = self._x + x
        cloned._y = self._y + y

        match direction:
            case "up":
                cloned._col = math.floor(self.mid_x / constants.SIZE.TILE) + 1
                cloned._row = math.floor(cloned.y / constants.SIZE.TILE) + 1
            case "down":
                cloned._col = math.floor(self.mid_x / constants.SIZE.TILE) + 1
                cloned._row = math.floor((cloned.y + constants.SIZE.TILE) / constants.SIZE.TILE) + 1
            case "left":
                cloned._col = math.floor(cloned.x / constants.SIZE.TILE) + 1
                cloned._row = math.floor(self.mid_y / constants.SIZE.TILE) + 1
            case "right":
                cloned._col = math.floor((cloned.x + constants.SIZE.TILE) / constants.SIZE.TILE) + 1
                cloned._row = math.floor(self.mid_y / constants.SIZE.TILE) + 1

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
    
    @property
    def mid_x(self) -> int:
        return math.floor(self._x + (constants.SIZE.TILE / 2))
    
    @property
    def mid_y(self) -> int:
        return math.floor(self._y + (constants.SIZE.TILE / 2))
    
    def __str__(self):
        return f"{self._col}/{self._row}"