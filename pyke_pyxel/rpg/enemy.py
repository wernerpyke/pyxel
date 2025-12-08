from .actor import MovableActor
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import MovableSprite
from pyke_pyxel.map import Map

class Enemy(MovableActor):

    def __init__(self, sprite: MovableSprite):
        super().__init__(sprite)

    def _move(self, map: Map):
        if not super()._move(map):
            sprite = map.sprite_at(self._move_to)
            if sprite:
                Signals.send_with(Signals.ENEMY.BLOCKED, self, sprite)