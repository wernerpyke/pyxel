from typing import Any
from dataclasses import dataclass

import time

from pyke_pyxel._log import log_debug
from pyke_pyxel.signals import Signals

@dataclass
class _timer:
    seconds: float
    signal: str
    sender: Any|None
    repeat: bool
    last_fire_time: float
    has_fired: bool = False
    # IMPORTANT: we need to keep track of has_fired
    # This is to guard against a race condition where, within the function called
    # by the signal, a new timer with the same signal is set.
    # For example, I set a timer "abc" and then, in do_abc() I update/reset "abc"

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
        self._upsert(seconds, signal, sender, False)

    def every(self, seconds: float, signal: str, sender:Any|None = None):
        """
        Set a timer to fire repeatedly after the specified time period has passed.
        If a timer with the same signal already exists the existing timer will be replaced.

        Args:
            seconds (float): the number of seconds to wait between firing the signal
            signal (str): the signal to send
            sender (Any optional): an optional sender value to send with the signal
        """
        self._upsert(seconds, signal, sender, True)

    def _upsert(self, seconds: float, signal: str, sender:Any|None, repeat: bool):
        if self._timers.get(signal) is not None:
            t = self._timers[signal]
            t.seconds = seconds
            t.sender = sender
            t.last_fire_time = time.time()
            t.has_fired = False
            log_debug(f"Timer._upsert() UPDATE {len(self._timers)}")
        else:
            self._timers[signal] = _timer(seconds, signal, sender, repeat, time.time())
            log_debug(f"Timer._upsert() NEW {len(self._timers)}")

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
                log_debug(f"Timer.update() REMOVING {k}")
                del self._timers[k]
        self._to_remove.clear()

        now = time.time()
        for k in self._timers:
            if timer := self._timers[k]:
                delta = now - timer.last_fire_time
                # print(f"Timer {k} {delta}")
                if delta >= timer.seconds:
                    timer.has_fired = True
                    Signals.send(timer.signal, timer.sender)
                    if timer.repeat:
                        timer.last_fire_time = now
                    else:
                        if timer.has_fired: # See important note above
                            self._to_remove.append(k)

    def _clear_all(self):
        self._timers.clear()
        self._to_remove.clear()
