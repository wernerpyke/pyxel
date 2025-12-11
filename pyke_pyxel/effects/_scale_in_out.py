from pyke_pyxel import GameSettings
from pyke_pyxel.sprite import Sprite
from ._effect import _Effect

class _ScaleInOutEffect(_Effect):

    def __init__(self, sprite: Sprite, max_scale: float, duration: float, completion_signal: str | None):
        super().__init__(completion_signal)

        self._sprite = sprite
        self._max_scale = max_scale
        
        self._orignal_scale = sprite.scale if sprite.scale else 1.0
        self._scale = self._orignal_scale
        self._duration = duration / 2 # half each way (out / in)

        fps = GameSettings.get().fps.game
        frames = round(self._duration * fps) # number of frames each way (out / in)

        scale_delta = self._max_scale - self._orignal_scale
        self._scale_increment = scale_delta / frames

        self._scale_out = True

    def _do(self):
        if self._scale_out:
            self._scale += self._scale_increment
            self._sprite.set_scale(self._scale)
            if self._scale >= self._max_scale:
                self._scale_out = False
        else:
            self._scale -= self._scale_increment
            if self._scale <= self._orignal_scale:
                self._sprite.set_scale(self._orignal_scale)
                self._complete()
            else:
                self._sprite.set_scale(self._scale)

