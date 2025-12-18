
from typing import Optional
from dataclasses import dataclass

import math
import random
import pyxel

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from ._log import log_debug, log_error
from ._base_types import COLOURS, GameSettings, coord
from .sprite import Sprite, OpenableSprite
    
@dataclass
class LOCATION_STATUS:
    FREE = 0
    BLOCKED = 1
    CLOSED = 2
    OPEN = 3

@dataclass
class PATH_STATUS:
    WALKABLE = 1
    UNWALKABLE = 0

@dataclass
class MapLocation:
    status: int
    sprite: Sprite|None = None
    is_edge: bool = False

class Map:

    def __init__(self, settings: GameSettings):
        size = settings.size

        self._grid: list[ list[MapLocation] ] = []
        self._path_grid: list [list [int] ] = []

        self._edgeLocation = MapLocation(LOCATION_STATUS.BLOCKED, is_edge=True)
        self._width = size.window
        self._height = size.window
        self._cols = math.floor(size.window / size.tile)
        self._rows = math.floor(size.window / size.tile)

        for c in range(0, self._cols):
            row: list[MapLocation] = []
            path_row: list[int] = []
            for r in range(0, self._rows):
                row.append(MapLocation(LOCATION_STATUS.FREE))
                path_row.append(PATH_STATUS.WALKABLE)
            
            self._path_grid.append(path_row)
            self._grid.append(row)

    def sprite_can_move_to(self, coord: coord) -> bool:
        """
        Determine if a sprite can move to the specified coordinate.
        
        Checks the status of the location at the given coordinate and returns True
        if the sprite is able to move there (i.e., the location is either `FREE` or `OPEN`).
        
        Args:
            coord (coord): The coordinate to check for sprite movement.
        
        Returns:
            bool: True if the location is `FREE` or `OPEN`, False otherwise.
        """
        status = self.location_at(coord).status
        return status == LOCATION_STATUS.FREE or status == LOCATION_STATUS.OPEN

    def mark_blocked(self, coord: coord, sprite: Sprite):
        """
        Mark the location at the given coordinate as blocked and attach a sprite.

        This updates the Location object returned by self.location_at(coord) by:
        - setting its status to `LOCATION_STATUS.BLOCKED`
        - assigning the provided sprite to its sprite attribute

        Args:
            coord (coord): The coordinate of the location to mark as blocked.
            sprite (Sprite): The sprite to place on the blocked location (e.g. an obstacle graphic).
        """
        location = self.location_at(coord)
        if location.is_edge:
            log_error(f"Map.mark_blocked() cannot mark edge location at {coord}")
            return

        location.status = LOCATION_STATUS.BLOCKED
        self._path_status(coord, PATH_STATUS.UNWALKABLE)
        location.sprite = sprite

    def mark_openable(self, coord: coord, sprite: OpenableSprite, closed: bool):
        """
        Mark a location as an openable object with the specified status.
        
        Args:
            coord (coord): The coordinate of the location to mark.
            sprite (OpenableSprite): The sprite to assign to the openable object.
            closed (bool): Whether the openable object is closed (True) or open (False).
        """
        
        location = self.location_at(coord)
        if location.is_edge:
            log_error(f"Map.mark_openable() cannot mark edge location at {coord}")
            return
        
        location.sprite = sprite
        if closed:
            self.mark_closed(coord)
        else:
            self.mark_open(coord)

    def mark_closed(self, coord: coord):
        """Mark a location as closed."""
        location = self.location_at(coord)
        if location.is_edge:
            log_error(f"Map.mark_closed() cannot mark edge location at {coord}")
            return
        
        location.status = LOCATION_STATUS.CLOSED
        self._path_status(coord, PATH_STATUS.UNWALKABLE)

    def mark_open(self, coord: coord):
        """Mark a location as open."""
        location = self.location_at(coord)
        if location.is_edge:
            log_error(f"Map.mark_open() cannot mark edge location at {coord}")
            return
        
        location.status = LOCATION_STATUS.OPEN
        self._path_status(coord, PATH_STATUS.WALKABLE)

    def is_blocked(self, coord: coord) -> bool:
        """Check if a location is blocked"""
        return self.location_at(coord).status == LOCATION_STATUS.BLOCKED
    
    def is_openable(self, coord: coord) -> bool:
        """Check if a location is openable"""
        location = self.location_at(coord)
        return location.status == LOCATION_STATUS.CLOSED or location.status == LOCATION_STATUS.OPEN

    def adjacent_openable(self, coord: coord) -> Optional[OpenableSprite]:
        """Check if a location adjacent(UP, DOWN, LEFT, RIGHT) to the provided coordinate is openable"""
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


    def openable_sprite_at(self, coord: coord) -> Optional[OpenableSprite]:
        """Return the `OpenableSprite` at a coordinate"""
        location = self.location_at(coord)
        if location.status == LOCATION_STATUS.CLOSED or location.status == LOCATION_STATUS.OPEN:
            return location.sprite # type: ignore
        
        return None
    
    def sprite_at(self, coord: coord) -> Sprite|None:
        """Return the `Sprite` at a coordinate"""
        return self.location_at(coord).sprite

    def location_at(self, coord: coord) -> MapLocation:
        """Return the `MapLocation` at a coordinate"""
        if coord._col < 1 or coord._col > self._cols or coord._row < 1 or coord._row > self._rows:
            return self._edgeLocation

        return self._grid[coord._col - 1][coord._row-1]
    
    def location_left_of(self, coord: coord) -> MapLocation|None:
        """Return the location LEFT of the coordinate"""
        if coord._col <= 1:
            return None
        return self._grid[coord._col - 1 - 1][coord._row - 1]
    
    def location_right_of(self, coord: coord) -> MapLocation|None:
        """Return the location RIGHT of the coordinate"""
        if coord._col >= self._grid.__len__() - 1:
            return None
        return self._grid[coord._col - 1 + 1][coord._row - 1]
    
    def location_above(self, coord: coord) -> MapLocation|None:
        """Return the location UP from of the coordinate"""
        if coord._row <= 1:
            return None
        return self._grid[coord._col - 1][coord._row - 1 - 1]
    
    def location_below(self, coord: coord) -> MapLocation|None:
        """Return the location DOWN from of the coordinate"""
        if coord._row >= self._grid[0].__len__() - 1:
            return None
        return self._grid[coord._col - 1][coord._row - 1 + 1]
    
    def x_is_left_of_center(self, x: int) -> bool:
        """Return true if `x` is to the left of the center of the map"""
        return x < self._width / 2
    
    def y_is_above_center(self, y: int) -> bool:
        """Return true if `y` is above the center of the map"""
        return y < self._height / 2
    
    def bound_to_width(self, x: int) -> int:
        """Check that `x` falls into the bounds of the map and return a safe value (max x of the map) if it does not"""
        if x < 0: 
            return 0
        elif x > self._width:
            return self._width
        else:
            return x
        
    def bound_to_height(self, y: int) -> int:
        """Check that `y` falls into the bounds of the map and return a safe value (max y of the map) if it does not"""
        if y < 0: 
            return 0
        elif y > self._height:
            return self._height
        else:
            return y

    def shortest_distance_to_sides(self, from_x: int) -> int:
        """Return the shortest distance to the sides of the map (either left or right)"""
        distance_to_left = from_x
        distance_to_right = self._width - from_x
        return min(distance_to_left, distance_to_right)

    def random_distance_to_right(self, from_x: int, min: int, max: int) -> int:
        """Generate a random distance to the right of `from_x` where the random distance falls between `min` and `max` without exceeding the bounds of the map."""
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
        """Generate a random distance to the left of `from_x` where the random distance falls between `min` and `max` without exceeding the bounds of the map."""
        distance = from_x
        if min > distance:
            return distance
        elif max > distance:
            return random.randint(min, distance)
        else:
            return random.randint(min, max)
        
    def random_distance_down(self, from_y: int, min: int, max: int) -> int:
        """Generate a random distance down of `from_y` where the random distance falls between `min` and `max` without exceeding the bounds of the map."""
        distance = self._height - from_y
        if min > distance:
            return distance
        elif max > distance:
            return random.randint(min, distance)
        else:
            return random.randint(min, max)
    
    def find_path(self, frm: coord, to: coord, allow_diagonal: bool = True) -> list[coord]|None:
        """ 
            Find a path between two locations

            Args:
                frm (coord): The starting location
                to (coord): The ending location
                allow_diagonal (bool, optional): Whether to allow diagonal movement. Defaults to True.

            Returns:
                list[coord]: A list of coordinates representing the path or `None` if no path exists.
        """
        if self.is_blocked(frm):
            log_error(f"Map.find_path() cannot find path from blocked location {frm}")
            return None
        
        if self.is_blocked(to):
            log_error(f"Map.find_path() cannot find path to blocked location {to}")
            return None

        grid = Grid(matrix=self._path_grid)
        
        start = grid.node(frm._col - 1, frm._row - 1)
        end = grid.node(to._col - 1, to._row - 1)

        diagonal = DiagonalMovement.always if allow_diagonal else DiagonalMovement.never
        finder = AStarFinder(diagonal_movement=diagonal)
        path, _ = finder.find_path(start, end, grid)

        # print(grid.grid_str(path=path, start=start, end=end))

        if path and len(path) > 0:
            return [coord(p.x + 1, p.y + 1) for p in path]
        else:
            return None

    @property
    def height(self) -> int:
        "Height of the map"
        return self._height
    
    @property
    def width(self) -> int:
        "Width of the map"
        return self._width

    @property
    def center_x(self) -> int:
        """Horizontal center point of the map"""
        return self._width // 2
    
    @property
    def center_y(self) -> int:
        """Vertical center point of the map"""
        return self._height // 2
    
    @property
    def right_x(self) -> int:
        """Right-most `x` point of the map"""
        return self._width
    
    @property
    def bottom_y(self) -> int:
        """Bottom-most `y` point of the map"""
        return self._height
    
    def _path_status(self, coord: coord, status: int):
        # import pathfinding is whack? x/y are switched around
        self._path_grid[coord._row - 1][coord._col - 1] = status

    def _draw_debug(self, settings: GameSettings):
        size = settings.size.tile

        for c in range(0, self._cols):
            x = c * size
            pyxel.text(x, 0, str(c+1), COLOURS.RED)

            for r in range(0, self._rows):
                location = self._grid[c][r]
                if location.status == LOCATION_STATUS.BLOCKED:
                    
                    y = r * size
                    pyxel.rectb(x, y, size, size, COLOURS.RED)

        for r in range(0, self._rows):
            y = r * size
            pyxel.text(0, y, str(r+1), COLOURS.RED)


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
