from typing import Callable
from .coord import Coord
from .map import Map
from .sprite import Sprite, OpenableSprite

class Room:

    def __init__(self, map: Map, sprites: list[Sprite]) -> None:
        self._map = map
        self._sprites = sprites

    def add_wall(self, wallType: Callable[[], Sprite], col: int, row: int):
        sprite = wallType()
        position = Coord(col, row)
        sprite.set_position(position)
        
        self._sprites.append(sprite)
        self._map.mark_blocked(position, sprite)

    def add_door(self, doorType: Callable[[], OpenableSprite], col: int, row: int, closed: bool = True):
        sprite = doorType()
        position = Coord(col, row)
        sprite.set_position(position)
        
        if closed:
            sprite.close()
        else:
            sprite.open()

        self._sprites.append(sprite)
        self._map.mark_openable(position, sprite, closed)