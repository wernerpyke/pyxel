
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass

import math
import random

from pyke_pyxel import GameSettings

from . import log_debug
from . import Coord

#if TYPE_CHECKING:
from .sprite import Sprite, OpenableSprite
    
@dataclass
class LOCATION_STATUS:
    FREE = 0
    BLOCKED = 1
    CLOSED = 2
    OPEN = 3

@dataclass
class MapLocation:
    status: int
    sprite: Optional[Sprite] = None

class Map:

    def __init__(self, settings: GameSettings):
        size = settings.size

        self._grid: list[ list[MapLocation] ] = []
        self._edgeLocation = MapLocation(LOCATION_STATUS.BLOCKED)
        self._width = size.window
        self._height = size.window
        self._cols = math.floor(size.window / size.tile)
        self._rows = math.floor(size.window / size.tile)

        log_debug(f"Map() {self._cols}/{self._rows}")

        for c in range(0, self._cols):
            row: list[MapLocation] = []
            for r in range(0, self._rows):
                row.append(MapLocation(LOCATION_STATUS.FREE))
            
            self._grid.append(row)

    def sprite_can_move_to(self, coord: Coord):
        status = self.location_at(coord).status
        return status == LOCATION_STATUS.FREE or status == LOCATION_STATUS.OPEN

    def mark_blocked(self, coord: Coord, sprite: Sprite):
        location = self.location_at(coord)
        location.status = LOCATION_STATUS.BLOCKED
        location.sprite = sprite

    def mark_openable(self, coord: Coord, sprite: OpenableSprite, closed: bool):
        status = LOCATION_STATUS.CLOSED if closed else LOCATION_STATUS.OPEN
        location = self.location_at(coord)
        location.status = status
        location.sprite = sprite

    def mark_closed(self, coord: Coord):
        self.location_at(coord).status = LOCATION_STATUS.CLOSED

    def mark_open(self, coord: Coord):
        self.location_at(coord).status = LOCATION_STATUS.OPEN

    def is_blocked(self, coord: Coord):
        return self.location_at(coord).status == LOCATION_STATUS.BLOCKED
    
    def is_openable(self, coord: Coord):
        location = self.location_at(coord)
        return location.status == LOCATION_STATUS.CLOSED or location.status == LOCATION_STATUS.OPEN

    def adjacent_openable(self, coord: Coord) -> Optional[OpenableSprite]:
        left = self.location_left_of(coord)
        if left:
            if left.status == LOCATION_STATUS.OPEN or left.status == LOCATION_STATUS.CLOSED:
                return left.sprite # type: ignore
        
        right = self.location_right_of(coord)
        if right:
            if right.status == LOCATION_STATUS.OPEN or right.status == LOCATION_STATUS.CLOSED:
                return right.sprite # type: ignore
            
        above = self.location_above(coord)
        if above:
            if above.status == LOCATION_STATUS.OPEN or above.status == LOCATION_STATUS.CLOSED:
                return above.sprite # type: ignore
            
        below = self.location_below(coord)
        if below:
            if below.status == LOCATION_STATUS.OPEN or below.status == LOCATION_STATUS.CLOSED:
                return below.sprite # type: ignore


    def openable_sprite_at(self, coord: Coord) -> Optional[OpenableSprite]:
        location = self.location_at(coord)
        if location.status == LOCATION_STATUS.CLOSED or location.status == LOCATION_STATUS.OPEN:
            return location.sprite # type: ignore
        
        return None
    
    def sprite_at(self, coord: Coord) -> Optional[Sprite]:
        return self.location_at(coord).sprite

    def location_at(self, coord: Coord) -> MapLocation:
        if coord._col < 1 or coord._col > self._cols or coord._row < 1 or coord._row > self._rows:
            return self._edgeLocation

        return self._grid[coord._col - 1][coord._row-1]
    
    def location_left_of(self, coord: Coord) -> Optional[MapLocation]:
        if coord._col <= 1:
            return None
        return self._grid[coord._col - 1 - 1][coord._row - 1]
    
    def location_right_of(self, coord: Coord) -> Optional[MapLocation]:
        if coord._col >= self._grid.__len__() - 1:
            return None
        return self._grid[coord._col - 1 + 1][coord._row - 1]
    
    def location_above(self, coord: Coord) -> Optional[MapLocation]:
        if coord._row <= 1:
            return None
        return self._grid[coord._col - 1][coord._row - 1 - 1]
    
    def location_below(self, coord: Coord) -> Optional[MapLocation]:
        if coord._row >= self._grid[0].__len__() - 1:
            return None
        return self._grid[coord._col - 1][coord._row - 1 + 1]
    
    def x_is_left_of_center(self, x: int) -> bool:
        return x < self._width / 2
    
    def y_is_above_center(self, y: int) -> bool:
        return y < self._height / 2
    
    def bound_to_width(self, x: int) -> int:
        if x < 0: 
            return 0
        elif x > self._width:
            return self._width
        else:
            return x
        
    def bound_to_height(self, y: int) -> int:
        if y < 0: 
            return 0
        elif y > self._height:
            return self._height
        else:
            return y

    def shortest_distance_to_sides(self, from_x: int) -> int:
        distance_to_left = from_x
        distance_to_right = self._width - from_x
        return min(distance_to_left, distance_to_right)

    def random_distance_to_right(self, from_x: int, min: int, max: int) -> int:
        distance = self._width - from_x
        if min > distance:
            x = distance
        elif max > distance:
            x = random.randint(min, distance)
        else:
            x = random.randint(min, max)
        
        if from_x + x >= 320:
            x -= 8 # 1 tile width, TODO this is messy
        return x
        
    def random_distance_to_left(self, from_x: int, min: int, max: int) -> int:
        distance = from_x
        if min > distance:
            return distance
        elif max > distance:
            return random.randint(min, distance)
        else:
            return random.randint(min, max)
        
    def random_distance_down(self, from_y: int, min: int, max: int) -> int:
        distance = self._height - from_y
        if min > distance:
            return distance
        elif max > distance:
            return random.randint(min, distance)
        else:
            return random.randint(min, max)
        
    @property
    def center_x(self) -> int:
        return self._width // 2
    
    @property
    def center_y(self) -> int:
        return self._height // 2
    
    @property
    def bottom_y(self) -> int:
        return self._height

    # @staticmethod
    # def find_nearby(sprites: list["Sprite"], for_sprite: "Sprite") -> list["Sprite"]:
    #     sprite_col = for_sprite.position._col
    #     sprite_row = for_sprite.position._row
        
    #     result: list["Sprite"] = []

    #     for s in sprites:
    #         col = s.position._col
    #         row = s.position._row

    #         if col in range(sprite_col - 2, sprite_col + 2) and row in range(sprite_row - 2, sprite_row + 2):
    #             result.append(s)

    #     return result
