from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import Sprite
from pyke_pyxel.map import Map

from pyke_pyxel import DIRECTION

class Projectile:

    def __init__(self, sprite: Sprite, movementSpeed: int, direction: str):
        self._sprite = sprite
        self._movementSpeed = movementSpeed
        self._direction = direction

        self._moveByX = 0
        self._moveByY = 0

        match direction:
            case DIRECTION.UP:
                self._moveByY = self._movementSpeed * -1
            case DIRECTION.DOWN:
                self._moveByY = self._movementSpeed
            case DIRECTION.LEFT:
                self._moveByX = self._movementSpeed * -1
            case DIRECTION.RIGHT:
                self._moveByX = self._movementSpeed

    def update(self, map: Map):
        sprite = self._sprite
        moveTo = sprite.position.clone_by(self._moveByX, self._moveByY, self._direction)

        if map.sprite_can_move_to(moveTo):
            sprite.set_position(moveTo)
            return True
        else:
            Signals._sprite_removed(sprite)
            return False
