from pyke_pyxel.drawable._camera_shake_effect import _CameraShakeEffect
from ._base_types import coord, GameSettings, DIRECTION
from .drawable._image import Image
from .drawable._effect import _Effect
from .drawable._circular_wipe_effect import _CircularWipeEffect
from .drawable._scale_effect import _ScaleEffect
from .drawable._splatter_effect import _SplatterEffect
from .drawable._scale_in_out_effect import _ScaleInOutEffect
from .sprite import Sprite


class FX:
    """
    FX class for managing visual effects in the game, specifically circular wipe transitions that can open or close,
    transitioning between scenes or states.

    This class should be accessed through the `game` instance via `game.fx`.
    """

    def __init__(self, settings: GameSettings):
        self._settings = settings
        self._updates: list[_Effect] = []
        self._drawables: list[_Effect] = []

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
        self._drawables.append(wipe)

    def splatter(self, colour: int, position: coord):        
        """
        Create a splatter effect at the specified position. 
        The splatter effect animates within a single tile for 30 frames.

        Args:
            colour (int): Colour index/value to use for the splatter.
            position (coord): The coordinate where the splatter effect should appear.
        """
        splatter = _SplatterEffect(position, colour)
        self._drawables.append(splatter)

    def scale_in(self, image: Image, duration: float = 0.5, completion_signal: str|None = None):
        """
        Scale (zoom) an image in over a specified duration. 
        The image will be drawn as part of the FX.

        Args:
            image (Image): the image to scale/zoom in
            duration (float): the duration in seconds over which to scale the image in
            completion_signal (str|None): an optional signal to send once the scale animation is complete
        """
        scale = _ScaleEffect(image, duration, True, completion_signal)
        self._drawables.append(scale)

    def scale_in_out(self, sprite: Sprite, to_scale:float, duration: float = 0.5, completion_signal: str|None = None):
        """
        Scale (zoom) a sprite in and back out over the specified duration.
        The sprite will be scaled from its current scale to `to_scale` and back to its current scale.
        The sprite has to already be added to the game, it will not be added as part of the FX, only its scale updated.

        Args:
            sprite (Sprite): the sprite to scale/zoom in and out
            duration (float): the duration in seconds over which to scale the sprite in
            completion_signal (str|None): an optional signal to send once the scale animation is complete
        """
        effect = _ScaleInOutEffect(sprite, to_scale, duration, completion_signal)
        self._updates.append(effect)

    def camera_shake(self, duration: float, direction: DIRECTION, completion_signal: str|None = None):
        """
        Apply camera shake in the specified direction for the specified duration.

        Args:
            duration (float): the duration in seconds over which to shake the camera
            direction (DIRECTION): the direction to shake the camera in
            completion_signal (str|None): an optional signal to send once the effect is complete
        """
        effect = _CameraShakeEffect(duration, direction, completion_signal)
        self._updates.append(effect)

    def _clear_all(self):
        self._drawables.clear()
        self._updates.clear()

    def _update(self):
        for effect in self._updates:
            effect._do()
            if not effect._active:
                self._updates.remove(effect)

    def _draw(self):
        # TODO - should FX have its own separate _update() so that FX are not updated if game.pause()?
        for effect in self._drawables:
            effect._do()
            if not effect._active:
                self._drawables.remove(effect)

    @property
    def requires_draw(self) -> bool:
        return any(effect._active for effect in self._drawables) is not None

    @property
    def requires_update(self) -> bool:
        return any(effect._active for effect in self._updates) is not None

        