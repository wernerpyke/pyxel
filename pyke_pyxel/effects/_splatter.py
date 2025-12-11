import pyxel
from pyke_pyxel import coord
from ._effect import _Effect

class _SplatterEffect(_Effect):
    def __init__(self, position: coord, colour: int):
        super().__init__(None)
        self._colour = colour
        self._position = position
        self._iteration = 0

        self._origin_x = position.mid_x
        self._origin_y = position.max_y - 2

    def _do(self):
        # Assume 60 FPS
        if self._iteration < 5:
            pyxel.pset(self._origin_x-1, self._origin_y, self._colour)
            pyxel.pset(self._origin_x, self._origin_y, self._colour)
            pyxel.pset(self._origin_x+1, self._origin_y, self._colour)
        elif self._iteration < 10:
            pyxel.pset(self._origin_x-1, self._origin_y+1, self._colour)
            pyxel.pset(self._origin_x, self._origin_y, self._colour)
            pyxel.pset(self._origin_x+1, self._origin_y+1, self._colour)
        elif self._iteration < 20:
            pyxel.pset(self._origin_x-2, self._origin_y+2, self._colour)
            pyxel.pset(self._origin_x, self._origin_y, self._colour)
            pyxel.pset(self._origin_x+2, self._origin_y+2, self._colour)
        # elif self._iteration < 40:
        #    pyxel.pset(self._origin_x-2, self._origin_y+2, self._colour)
        #    pyxel.pset(self._origin_x, self._origin_y, self._colour)
        #    pyxel.pset(self._origin_x+2, self._origin_y+2, self._colour)
        else:
            self._complete()
            return

        self._iteration += 1