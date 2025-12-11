import pyxel

from pyke_pyxel import GameSettings, DIRECTION
from ._effect import _Effect

class _CameraShakeEffect(_Effect):

    def __init__(self, duration: float, direction: DIRECTION, completion_signal: str|None = None):
        super().__init__(completion_signal)

        fps = GameSettings.get().fps.game
        self._frames = round(duration * fps)
        self._frame_counter = 0

        self._shake_x = 0
        self._shake_y = 0

        match direction:
            case DIRECTION.LEFT:
                self._shake_x = -2
            case DIRECTION.RIGHT:
                self._shake_x = 2
            case DIRECTION.UP:
                self._shake_y = -2
            case DIRECTION.DOWN:
                self._shake_y = 2

    def _do(self):
        pyxel.camera(self._shake_x, self._shake_y)
        self._shake_x *= -1
        self._shake_y *= -1

        self._frame_counter += 1
        if self._frame_counter >= self._frames:
            pyxel.camera()
            self._complete()