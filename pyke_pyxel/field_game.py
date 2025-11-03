from typing import Callable, Optional

import pyxel

from pyke_pyxel.game_settings import GameSettings

from . import GLOBAL_SETTINGS
from .game import Game
from .cell_field import CellField

class FieldGame(Game):

    def __init__(self, settings: GameSettings, title: str, resources: str):
        super().__init__(settings, title, resources)
        
        # TODO - support non-square fields
        size = GLOBAL_SETTINGS.size
        self._field = CellField(size.window, size.window)

    # Lifecycle methods

    def draw(self):
        super()._draw_background()

        self._field._draw()

        super()._draw_sprites()

        if self._hud:
            self._hud._draw(self._settings)

    # Convenience accessors

    @property
    def field(self) -> CellField:
        return self._field