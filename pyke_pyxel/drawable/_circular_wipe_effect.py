
import math
import pyxel

from pyke_pyxel import GameSettings
from ._effect import _Effect


class _CircularWipeEffect(_Effect):
    def __init__(self, colour: int, wipe_closed: bool, completion_signal: str|None, settings: GameSettings):
        super().__init__(completion_signal)

        self._colour = colour
        self._wipe_closed = wipe_closed
        self._width = settings.size.window
        self._height = settings.size.window
        self._center_x = settings.size.window // 2
        self._center_y = settings.size.window // 2
        self._max_radius = math.floor(math.sqrt(self._center_x**2 + self._center_y**2))
        self._radius_step = 3
        self._current_radius = 0

        if self._wipe_closed:
            self._current_radius = self._max_radius
        else:
            self._current_radius = 0

    def _draw(self):
        for y in range(0, self._height):
            for x in range(0, self._width):
                distance = math.sqrt((x - self._center_x)**2 + (y - self._center_y)**2)
                delta = distance - self._current_radius
                if delta <= 0:
                    pass
                elif delta < 5 and (x % 2 == 0) and (y % 2 == 0):
                    pyxel.pset(x, y, self._colour)
                else:
                    pyxel.pset(x, y, self._colour)

        if self._wipe_closed:
            self._current_radius -= self._radius_step
            if self._current_radius <= 0:
                self._complete()
        else:
            self._current_radius += self._radius_step
            if self._current_radius >= self._max_radius:
               self._complete()