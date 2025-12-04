import pyxel

from .signals import Signals

class Keyboard:
    """
    Access keyboard events and status.
    
    In order to use the correct pyxel key mapping it is necessary to import pyxel.
    For example:
    >>> import pyxel
    >>>
    >>> if game.keyboard.was_pressed(pyxel.KEY_UP):
    >>>     print("UP")
    """

    def __init__(self) -> None:
        self.signals: dict[int, tuple[str, bool]] = {}

    def was_pressed(self, key: int) -> bool:
        """
        Return True if the provided key was pressed down this frame.
        
        Args:
            key(int): The `pyxel.KEY_*` value of the key to check
        """
        return pyxel.btnp(key)
    
    def is_down(self, key: int) -> bool:
        """
        Return True if the provided key is pressed and held down this frame.

        Args:
            key(int): The `pyxel.KEY_*` value of the key to check
        """
        return pyxel.btn(key)
    
    def send_signal_for_key(self, key: int, signal: str):
        """
        Send a signal when a key is pressed. If the key is pressed down the signal will be emitted once
        and then only emitted again if the key is pressed again.

        Args:
            key(int): The `pyxel.KEY_*` value of the key to connect the signal to
            signal(str): The name of the signal to emit when the key is pressed down
        """
        self.signals[key] = (signal, False)

    def remove_signal_for_key(self, key: int):
        """
        Disconnect a signal from a key press.

        Args:
            key(int): The `pyxel.KEY_*` value of the key to disconnect the signal from
        """
        if self.signals.get(key):
            del self.signals[key]

    def _update(self, game):
        for k in self.signals:
            v = self.signals[k]
            signal = v[0]
            has_been_sent = v[1]
            if has_been_sent:
                if pyxel.btnr(k):
                    self.signals[k] = (signal, False) # reset the signal
            else:
                if pyxel.btnp(k):
                    Signals.send(signal, game)
                    self.signals[k] = (signal, True) # flag the signal as sent
                    
            


