from .actor import MovableActor
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import MovableSprite
from pyke_pyxel.map import Map

class Enemy(MovableActor):

    def __init__(self, sprite: MovableSprite, speed_px_per_second: int):
        """
        Args:
            sprite (MovableSprite): the sprite that represents this enemy
            speed_px_per_second (int): The speed of the enemy's movements expressed as pixels per second
        """
        super().__init__(sprite, speed_px_per_second)

    def _move(self, map: Map) -> bool:
        if super()._move(map):
            return True
        else:
            if to := self._blocked_by:
                sprite = map.sprite_at(to)
                if sprite:
                    Signals.send_with(Signals.ENEMY.BLOCKED, self, sprite)
            return False