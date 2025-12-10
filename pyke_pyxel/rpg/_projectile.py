from pyke_pyxel import GameSettings, DIRECTION
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import Sprite
from pyke_pyxel.map import Map

class Projectile:

    def __init__(self, sprite: Sprite, speed_px_per_second: int, direction: DIRECTION):
        self._sprite = sprite
        self._movement_speed = speed_px_per_second
        self._direction = direction

        self._px_per_frame: float = speed_px_per_second / GameSettings.get().fps.game
        self._px_counter = 0

        self._direction = direction
        self._move_by_x = 0
        self._move_by_y = 0

        match direction:
            case DIRECTION.UP:
                self._move_by_y = -1
            case DIRECTION.DOWN:
                self._move_by_y = 1
            case DIRECTION.LEFT:
                self._move_by_x = -1
            case DIRECTION.RIGHT:
                self._move_by_x = 1

    def _update(self, map: Map):
        self._px_counter += self._px_per_frame
        if self._px_counter < 1:
            return
        self._px_counter = 0

        distance = round(self._px_per_frame) if self._px_per_frame > 1 else 1

        by_x = distance * self._move_by_x
        by_y = distance * self._move_by_y

        sprite = self._sprite
        move_to = sprite.position.clone_by(by_x, by_y, self._direction)

        if map.sprite_can_move_to(move_to):
            sprite.set_position(move_to)
            return True
        else:
            Signals.send_remove_sprite(sprite)
            return False
