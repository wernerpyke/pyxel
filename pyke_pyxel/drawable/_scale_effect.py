import pyxel
from pyke_pyxel import Coord
from pyke_pyxel._base_types import GameSettings
from ._image import Image
from ._effect import _Effect

class _ScaleEffect(_Effect):

    def __init__(self, image: Image, duration: float, scale_in: bool, completion_signal: str|None):
        super().__init__(completion_signal)
        self._image = image
        self._scale_in = scale_in

        settings = GameSettings.get()
        self._width = settings.size.tile * image.col_tile_count
        self._height = settings.size.tile * image.row_tile_count
        self._transparency = settings.colours.sprite_transparency

        self._scale: float = 0.0
        self._scale_step: float = 1.0 / (duration * settings.fps.game)

    def _draw(self):
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

        position = image._position

        # Pyxel is cool enough to transform x & y without us needing to manually recalculate
        pyxel.blt(x=position.x,
                y=position.y,
                img=image.resource_image_index,
                u=image.frame.x,
                v=image.frame.y,
                w=self._width,
                h=self._height,
                colkey=self._transparency,
                scale=self._scale)

        
        