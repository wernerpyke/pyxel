import pyxel
from pyke_pyxel._base_types import GameSettings
from ._image import Image
from ._effect import _Effect

class _ScaleEffect(_Effect):

    def __init__(self, image: Image, duration: float, scale_in: bool, completion_signal: str|None):
        super().__init__(completion_signal)
        self._image = image
        self._scale_in = scale_in

        settings = GameSettings.get()
        self._transparency = settings.colours.sprite_transparency

        self._scale: float = 0.0
        self._scale_step: float = 1.0 / (duration * settings.fps.game)

    def _do(self):
        if self._scale_in:
            self._scale += self._scale_step
            if self._scale >= 1:
                self._complete()
                return
        else:
            self._scale -= self._scale_step
            if self._scale <= 0:
                self._complete()
                return

        image = self._image

        position = image.position

        # Pyxel is cool enough to transform x & y without us needing to manually recalculate
        pyxel.blt(x=position.x,
                y=position.y,
                img=image.image_index,
                u=image.frame.x,
                v=image.frame.y,
                w=image.width,
                h=image.height,
                colkey=self._transparency,
                scale=self._scale)

        
        