from pyke_pyxel.signals import Signals

class _Effect:    
    def __init__(self, completion_signal: str|None):
        self._completion_signal: str | None = completion_signal
        self._active = True

    def _complete(self):
        self._active = False
        if signal := self._completion_signal:
            Signals.send(signal, self)
            self._completion_signal = None

    def _draw(self):
        raise NotImplementedError("Effect._draw() not implemented")