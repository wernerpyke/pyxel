from typing import Callable, Optional

import pyxel

from pyke_pyxel.game_settings import GameSettings

from . import game
# from .game import Game
from .cell_field import CellField

class FieldGame(game.Game):

    def __init__(self, settings: GameSettings, title: str, sprite_sheet: str):
        super().__init__(settings, title, sprite_sheet)
        
        # TODO - support non-square fields
        size = game.GLOBAL_SETTINGS.size
        self._field = CellField(size.window, size.window)

    # Lifecycle methods

    def update(self):
        self._field._update()

        super().update()

    def draw(self):
        super()._draw_background()

        self._field._draw()

    # Convenience accessors

    @property
    def field(self) -> CellField:
        return self._field