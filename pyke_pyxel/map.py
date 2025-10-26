from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass

import math

from . import game
from .coord import Coord

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

    def __init__(self):
        sizes = game.GLOBAL_SETTINGS.size

        self._grid: list[ list[MapLocation] ] = []
        self._edgeLocation = MapLocation(LOCATION_STATUS.BLOCKED)
        self._cols = math.floor(sizes.window / sizes.tile)
        self._rows = math.floor(sizes.window / sizes.tile)

        print(f"Map() {self._cols}/{self._rows}")

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
