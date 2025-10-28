from typing import Callable
from .base_types import Coord
from .map import Map
from .sprite import Sprite, OpenableSprite, MovableSprite
from .signals import Signals
from .enemy import Enemy

class Room:

    def __init__(self, map: Map) -> None:
        self._map = map

    def add_wall(self, wallType: Callable[[], Sprite], col: int, row: int):
        sprite = wallType()
        position = Coord(col, row)
        sprite.set_position(position)
        
        Signals._sprite_added(sprite)
        self._map.mark_blocked(position, sprite)

    def add_door(self, doorType: Callable[[], OpenableSprite], col: int, row: int, closed: bool = True):
        sprite = doorType()
        position = Coord(col, row)
        sprite.set_position(position)
        
        if closed:
            sprite.close()
        else:
            sprite.open()

        Signals._sprite_added(sprite)
        self._map.mark_openable(position, sprite, closed)

    def add_enemy(self, enemyType: Callable[[], MovableSprite], col: int, row: int) -> Enemy:
        sprite = enemyType()
        enemy = Enemy(sprite)
        enemy.set_position(col, row)

        Signals._sprite_added(sprite)
        Signals._enemy_added(enemy)

        return enemy
