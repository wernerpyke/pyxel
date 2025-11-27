import pyxel
from pyke_pyxel import Coord, GameSettings
from pyke_pyxel._base_types import COLOURS


class Rect:
    def __init__(self, position: Coord, col_count: int, row_count: int) -> None:
        self._position = position
        self._col_count = col_count
        self._row_count = row_count

        self._bg_colour: int|None = None
        self._border_colour: int|None = None
        self._border_width: int|None = None
        self._id = 0

    def set_background(self, colour: int):
        self._bg_colour = colour

    def set_border(self, colour: int, width: int):
        self._border_colour = colour
        self._border_width = width

    def __eq__(self, other):
        return isinstance(other, Rect) and self._id == other._id

    def _draw(self, settings: GameSettings):
        width = settings.size.tile * self._col_count
        height = settings.size.tile * self._row_count

        position = self._position

        if not self._bg_colour == None: # can't just if self._bg_colour because a value of '0' will return False
            pyxel.rect(x=position.x,
                    y=position.y,
                    w=width,
                    h=height,
                    col=self._bg_colour)
            
        if (not self._border_colour == None) and (not self._border_width == None):
            i = 0
            while i < self._border_width:
                pyxel.rectb(x=(position.x + i),
                            y=(position.y + i),
                            w=(width-(i*2)),
                            h=(height-(i*2)),
                            col=self._border_colour)
                i += 1