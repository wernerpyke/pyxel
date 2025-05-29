from typing import Optional

from .actor import MovableActor
from .signals import Signals, DIRECTION
from .sprite import Sprite, OpenableSprite, MovableSprite
from .map import Map, Coord

class Enemy(MovableActor):

    def __init__(self, sprite: MovableSprite):
        super().__init__(sprite)

    def move(self, direction: str, map: Map):
        if not super().move(direction, map):
            sprite = map.sprite_at(self._moveTo)
            if sprite:
                Signals.send(Signals.ENEMY.BLOCKED, self, sprite)