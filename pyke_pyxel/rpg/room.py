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
        
        Signals.send_add_sprite(sprite)

        for c in range(0, sprite.cols):
            for r in range(0, sprite.rows):
                p = coord(col + c, row + r)
                self._map.mark_blocked(p, sprite)

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

        Signals.send_add_sprite(sprite)
        self._map.mark_openable(position, sprite, closed)

    def add_enemy(self, sprite: Enemy|MovableSprite|Callable[[], MovableSprite], speed_px_per_second: int = 0) -> Enemy:
        """
        Add an enemy to the map.

        Args:
            sprite (Enemy | MovableSprite | Callable[[], MovableSprite]): The sprite (or a callable that returns a sprite) representing the enemy.
            speed_px_per_second (int): The speed of the enemy's movements expressed as pixels per second

        Returns:
            Enemy: The initialized `Enemy` instance.
        """
        if isinstance(sprite, Enemy):
            enemy = sprite
            Signals.send_add_sprite(enemy._sprite)
        else:
            if isinstance(sprite, Callable):
                sprite = sprite()
            enemy = Enemy(sprite, speed_px_per_second)
            Signals.send_add_sprite(sprite)

        _signals._enemy_added(enemy)

        return enemy
