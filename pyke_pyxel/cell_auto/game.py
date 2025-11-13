from pyke_pyxel import GameSettings

from .. import GameSettings
from ..game import Game
from .matrix import Matrix

class CellAutoGame(Game):
    """
    Specialised sub-class of `pyke_pyxel.Game` which adds a cellular automaton matrix.
        
        Attributes:
            matrix(Matrix): read-only access to the cellular automaton matrix
    """

    def __init__(self, settings: GameSettings, title: str, resources: str):
        """
        Args:
            settings (GameSettings): The game settings configuration.
            title (str): The title of the game window.
            resources (str): The path to the resources directory.
        """
        super().__init__(settings, title, resources)
        
        # TODO - support non-square fields
        size = GameSettings.get().size.window
        self._matrix = Matrix(size, size)

    # Lifecycle methods

    def draw(self):
        super()._draw_background()

        self._matrix._draw()

        super()._draw_sprites()

        if self._hud:
            self._hud._draw(self._settings)

        if self._fx and self._fx._is_active:
            self._fx._draw()

    # Convenience accessors

    @property
    def matrix(self) -> Matrix:
        return self._matrix