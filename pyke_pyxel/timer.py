from typing import Any
from dataclasses import dataclass

import time

from pyke_pyxel.signals import Signals

@dataclass
class _timer:
    seconds: float
    signal: str
    multiple: bool
    sender: Any|None = None
    last_fire_time: float = time.time()

class Timer:
    """
    A centralised timer single (`after`) and multiple (`every`) support.
    Individual timers are uniquely identifed by the signals that they send

    This class should be accessed through the `Game` instance via `game.timer`.
    """
    def __init__(self) -> None:
        self._timers: dict[str, _timer] = {}
        self._to_remove: list[str] = []

    def after(self, seconds: float, signal: str, sender:Any|None = None):
        """
        Set a timer to fire once after the specified time period has passed.
        If a timer with the same signal already exists the existing timer will be replaced.

        Args:
            seconds (float): the number of seconds to wait until firing the signal
            signal (str): the signal to send
            sender (Any optional): an optional sender value to send with the signal
        """
        self._timers[signal] = _timer(seconds, signal, False, sender)

    def every(self, seconds: float, signal: str, sender:Any|None = None):
        """
        Set a timer to fire repeatedly after the specified time period has passed.
        If a timer with the same signal already exists the existing timer will be replaced.

        Args:
            seconds (float): the number of seconds to wait between firing the signal
            signal (str): the signal to send
            sender (Any optional): an optional sender value to send with the signal
        """
        self._timers[signal] = _timer(seconds, signal, True, sender)

    def cancel(self, signal: str):
        """
        Cancel a previously set timer. No-op is the timer does not exist.

        Args:
            signal (str): the signal that identifies the timer
        """
        if self._timers.get(signal) is not None:
            self._to_remove.append(signal)

    def has_timer(self, signal: str) -> bool:
        """Return `True` if a timer is registered for the provided signal"""
        return self._timers.get(signal) is not None

    def _update(self):
        for k in self._to_remove:
            if self._timers[k]:
                del self._timers[k]
        self._to_remove.clear()

        now = time.time()
        for k in self._timers:
            if timer := self._timers[k]:
                delta = now - timer.last_fire_time
                if delta >= timer.seconds:
                    Signals.send(timer.signal, timer.sender)
                    if timer.multiple:
                        timer.last_fire_time = now
                    else:
                        self._to_remove.append(k)

    def _clear_all(self):
        self._timers.clear()
        self._to_remove.clear()
