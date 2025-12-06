from ._base_types import coord, GameSettings
from .drawable._image import Image
from .drawable._effect import _Effect
from .drawable._circular_wipe_effect import _CircularWipeEffect
from pyke_pyxel.drawable._scale_effect import _ScaleEffect
from .drawable._splatter_effect import _SplatterEffect

class FX:
    """
    FX class for managing visual effects in the game, specifically circular wipe transitions that can open or close,
    transitioning between scenes or states.

    This class should be accessed through the `game` instance via `game.fx`.
    """

    def __init__(self, settings: GameSettings):
        self._settings = settings
        self._effects: list[_Effect] = []

    def circular_wipe(self, colour: int, wipe_closed: bool, completion_signal: str):
        """
        Create a full-screen circular wipe animation.

        Parameters
        ----------
        colour : int
            Colour index/value to use when rendering the wipe.
        wipe_closed : bool
            If True, the wipe is configured to close (shrink) toward the centre.
            If False, the wipe is configured to open (expand) outward.
        completion_signal : str
            Identifier of the signal/event to emit when the wipe animation finishes.
        """
        wipe = _CircularWipeEffect(colour, wipe_closed, completion_signal, self._settings)
        self._effects.append(wipe)

    def splatter(self, colour: int, position: coord):        
        """
        Create a splatter effect at the specified position. 
        The splatter effect animates within a single tile for 30 frames.

        Parameters
        ----------
        colour : int
            Colour index/value to use for the splatter.
        position : coord
            The coordinate where the splatter effect should appear.
        """
        splatter = _SplatterEffect(position, colour)
        self._effects.append(splatter)

    def scale_in(self, image: Image, duration: float = 0.5, completion_signal: str|None = None):
        scale = _ScaleEffect(image, duration, True, completion_signal)
        self._effects.append(scale)

    def _clear_all(self):
        self._effects.clear()

    def _draw(self):
        # TODO - should FX have its own separate _update() so that FX are not updated if game.pause()?
        for effect in self._effects:
            effect._draw()
            if not effect._active:
                self._effects.remove(effect)

    @property
    def is_active(self):
        return any(effect._active for effect in self._effects)
        