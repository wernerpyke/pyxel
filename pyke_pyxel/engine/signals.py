from dataclasses import dataclass

from typing import Callable, Optional
from blinker import signal

class Signals:
    
    @dataclass
    class PLAYER:
        BLOCKED = "player_blocked"
        INTERACT_OPENABLE = "player_interact_openable"

    @staticmethod
    def connect(name: str, listener: Callable):
        signal(name).connect(listener)

    @staticmethod
    def send(name: str, sender):
        signal(name).send(sender)

