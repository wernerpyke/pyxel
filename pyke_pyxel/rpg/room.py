from typing import Callable
from pyke_pyxel import coord
from pyke_pyxel.map import Map
from pyke_pyxel.sprite import Sprite, OpenableSprite, MovableSprite
from pyke_pyxel.signals import Signals
from .enemy import Enemy

from . import _signals

class Room:

    def __init__(self, map: Map) -> None:
        self._map = map

    def add_wall(self, sprite: Sprite|Callable[[], Sprite], col: int, row: int):
        """
        Add a wall to the map. The related map position will be marked as blocked.


        Args:
            sprite (Sprite | Callable[[], Sprite]): The sprite (or a callable that returns a sprite) representing the wall.
            col (int): The column position of the wall
            row (int): The row position of the wall
        """
        if isinstance(sprite, Callable):
            sprite = sprite()
        position = coord(col, row)
        sprite.set_position(position)
        
        Signals._sprite_added(sprite)
        self._map.mark_blocked(position, sprite)

    def add_door(self, sprite: OpenableSprite|Callable[[], OpenableSprite], col: int, row: int, closed: bool = True):
        """
        Add an openable door to the map. The related map position will be marked as either open or closed.

        Args:
            sprite (OpenableSprite | Callable[[], OpenableSprite]): The sprite (or a callable that returns a sprite) representing the door.
            col (int): The column position of the door
            row (int): The row position of the door
            closed (bool): whether the door should be closed or open by default
        """
        if isinstance(sprite, Callable):
            sprite = sprite()
        position = coord(col, row)
        sprite.set_position(position)
        
        if closed:
            sprite.close()
        else:
            sprite.open()

        Signals._sprite_added(sprite)
        self._map.mark_openable(position, sprite, closed)

    def add_enemy(self, sprite: MovableSprite|Callable[[], MovableSprite], col: int, row: int) -> Enemy:
        """
        Add an enemy to the map.

        Args:
            sprite (MovableSprite | Callable[[], MovableSprite]): The sprite (or a callable that returns a sprite) representing the enemy.
            col (int): The column position of the enemy
            row (int): The row position of the enemy

        Returns:
            Enemy: The initialized `Enemy` instance.
        """
        if isinstance(sprite, Callable):
            sprite = sprite()
        enemy = Enemy(sprite)
        enemy.set_position(col, row)

        Signals._sprite_added(sprite)
        _signals._enemy_added(enemy)

        return enemy
